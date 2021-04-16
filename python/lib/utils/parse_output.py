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
        input_folder=f"../data"
        input_fn='example.log'
        os.chdir(input_folder)
        assert (os.path.exists(input_fn))
        df=parse_output_log(input_fn, include_inputs=False, printing=True)
        print(f"is this a pandas.Dataframe? {type(df)}")

        # Test compute_runtime_for_folder
        nb_dir='/home/timothytyree/Documents/GitHub/bgmc/python/'
        data_dir=f"{nb_dir}/data/osg_output/Log"
        runtime=compute_runtime_for_folder(folder=data_dir)
        print(f"the total recorded runtime was {runtime:.3f} years.")

        # Test parse_iolines
        data_dir=f"{nb_dir}/data/osg_output/Log"
        os.chdir(data_dir)
        input_fn_lst=os.listdir()
        input_fn=input_fn_lst[0]
        n_input,n_output=parse_iolines(input_fn, printing=False)
        print (f"parse_iolines returned (n_input,n_output)={(n_input,n_output)}")
