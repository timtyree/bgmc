import pandas as pd, os, numpy as np
##################################
# For Mean Results
##################################
def parse_iolines(input_fn, printing=False):
    n_input=-9999
    n_output=-9999
    with open(input_fn) as f:
        trgt1='Printing Inputs...\n'
        trgt2='Printing Outputs...\n'
        for n,line in enumerate(f):
            if trgt1 == line:
                if printing:
                    print(f'found inputs starting after line {n}')
                n_input=n
            if trgt2 == line:
                if printing:
                    print(f'found outputs starting after line {n}')
                n_output=n
    return n_input,n_output

def parse_inputs(input_fn,n_input,n_output,printing=False):
    if n_input==-9999:
        if printing:
            print(f"Warning: n_input not found for input_fn={input_fn}.\nreturning None...")
        return None
    with open(input_fn) as f:
        inputs=f.readlines()[n_input+1:n_output-1]
    col_name_lst=[]
    col_value_lst=[]
    for line in inputs:
        string=line.split(' ')[-1]
        eid=string.find('=')
        if eid!=-1:
            col_name=string[:eid]
            # try:
            col_value=eval(string[eid+1:-1])
            # except Exception as e:
            #     print (string)
            #     col_value=string[eid+1:-1]
            col_name_lst.append(col_name)
            col_value_lst.append(col_value)
    return col_name_lst, col_value_lst

def parse_outputs(input_fn, n_output):
    with open(input_fn) as f:
        for n,line in enumerate(f):
            if n == n_output+1:
                line_N = line
            if n == n_output+2:
                line_CollTime =line
    N_values=np.array([eval(s) for s in line_N[:-2].split(',')])
    CollTime_values=np.array([eval(s) for s in line_CollTime[:-2].split(',')])
    # CollTime_values=np.array([eval(s) for s in line_CollTime[:-1].split(',')])
    df=pd.DataFrame({
        'N':N_values,
        'CollTime':CollTime_values
    })
    df=df.loc[df.CollTime!=-9999]
    df.reset_index(inplace=True,drop=True)
    return df

def parse_log(input_fn,qfoo,include_inputs=True,printing=False):
    n_input,n_output=parse_iolines(input_fn, printing=False)
    if n_input==-9999:
        if printing:
            print(f"Warning: n_input not found for input_fn={input_fn}.\nreturning None...")
        return None

    col_name_lst, col_value_lst=parse_inputs(input_fn,n_input,n_output,printing=printing)
    dict_inputs=dict(zip(col_name_lst,col_value_lst))
    if not qfoo(dict_inputs):
        return None
    df=parse_outputs(input_fn, n_output)
    #augment df with input parameters
    if include_inputs:
        if printing:
            print("input parameters were:")
            print(col_name_lst)
            print(col_value_lst)
            print("returning outputs as pandas.DataFrame instance")
        for name,value in zip ( col_name_lst, col_value_lst):
            df[name]=value
    # df.drop(columns=['dt','reflect','set_second'],inplace=True)
    return df

# ##################################
# # (General) Parse Runtime
# ##################################
# import datetime, os, time
# import dateutil.parser as dp
# def parse_runtime(input_fn):
#     seconds_in_day = 24 * 60 * 60
#     seconds_in_year = seconds_in_day * 365
#     with open(input_fn) as f:
#         line_first = f.readline()
#         for n, line in enumerate(f):
#             line_last = f.readline()
#     # import dateutil.tz as tz
#     time_start = dp.parse(line_first[:-1], ignoretz=True)
#     time_end = dp.parse(line_last[:-1], ignoretz=True)
#     difference = time_end - time_start
#     # divmod(difference.days * seconds_in_day + difference.seconds, 60)#(min,sec)
#     seconds = difference.days * seconds_in_day + difference.seconds
#     years = seconds / seconds_in_year
#     return years

##################################
# For Dense Results
##################################
def parse_output_log(input_fn,include_inputs=True, printing=False):
    '''For Dense Results'''
    n_input=-9999
    with open(input_fn) as f:
        trgt1='Printing Inputs...\n'
        trgt2='Printing Outputs...\n'
        for n,line in enumerate(f):
            if trgt1 == line:
                if printing:
                    print(f'found inputs starting after line {n}')
                n_input=n
            if trgt2 == line:
                if printing:
                    print(f'found outputs starting after line {n}')
                n_output=n
    if n_input==-9999:
        if printing:
            print(f"Warning: n_input not found for input_fn={input_fn}.\nreturning None...")
        return None
    with open(input_fn) as f:
        inputs=f.readlines()[n_input+1:n_output-1]
    col_name_lst=[]
    col_value_lst=[]
    for line in inputs:
        string=line.split(' ')[-1]
        eid=string.find('=')
        if eid!=-1:
            col_name=string[:eid]
            # try:
            col_value=eval(string[eid+1:-1])
            # except Exception as e:
            #     print (string)
            #     col_value=string[eid+1:-1]
            col_name_lst.append(col_name)
            col_value_lst.append(col_value)
    df=pd.read_csv(input_fn,header=n_output-2)
    #drop that 'Unammed: {Nmax}' column
    df.drop(columns=[df.columns[-1]], inplace=True)
    if include_inputs:
        if printing:
            print("input parameters were:")
            print(col_name_lst)
            print(col_value_lst)
            print("returning outputs as pandas.DataFrame instance")
        for name,value in zip ( col_name_lst, col_value_lst):
            df[name]=value
    return df

if __name__=='__main__':
    import sys
    input_fn=sys.argv[1]
    sum_fn=sys.argv[2]
    # input_folder=f"../data"
    # os.chdir(input_folder)
    # input_fn='../Log/example-output.txt'
    assert (os.path.exists(input_fn))
    assert (os.path.exists(sum_fn))
    n_input,n_output=parse_iolines(input_fn, printing=False)
    df=parse_outputs(input_fn, n_output)
    df.set_index('N',inplace=True,drop=True)
    # df=parse_output_log(input_fn, include_inputs=False, printing=True)
    # print(f"is this a pandas.Dataframe? {type(df)}") Yes
    print(df.head())

    #TODO(later): argument parse for seed (the original)
    # seed  =1234
    # sum_fn=f"sum.csv"
    boo=df.CollTime!=-9999
    if not os.path.exists(sum_fn):
        #save initial sum/summary
        count=0
        df['count']=0
        if count==0:
            df.loc[boo,'CollTime']=df[boo]['CollTime']+df[boo]['CollTime']
            df.loc[boo,'count']+=1
            df.to_csv(sum_fn)
        # print(df.head())
    else:
        #appendd initial sum/summary:
        df_sum=pd.read_csv(sum_fn,index_col="N")
        boo_sum=df_sum.CollTime!=-9999
        df_sum.loc[boo_sum,'CollTime']=df_sum[boo_sum]['CollTime']+df[boo]['CollTime']
        df_sum.loc[boo_sum,'count']=1+df_sum.loc[boo_sum,'count']
        df_sum.to_csv(sum_fn)


    #reconstruct my preexisting input
    #TODO: read input_fn
    #TODO: print each line in input_fn up until n_output
    #TODO: load and sum an input file with sum_fn,
    #TODO: save df to sum_fn

    # # Test compute_runtime_for_folder
    # nb_dir='/home/timothytyree/Documents/GitHub/bgmc/python/'
    # data_dir=f"{nb_dir}/data/osg_output/Log"
    # runtime=compute_runtime_for_folder(folder=data_dir)
    # print(f"the total recorded runtime was {runtime:.3f} years.")

    # # Test parse_iolines
    # data_dir=f"{nb_dir}/data/osg_output/Log"
    # os.chdir(data_dir)
    # input_fn_lst=os.listdir()
    # input_fn=input_fn_lst[0]
    # n_input,n_output=parse_iolines(input_fn, printing=False)
    # print (f"parse_iolines returned (n_input,n_output)={(n_input,n_output)}")
