import pandas as pd, os
def parse_output_log(input_fn,include_inputs=True, printing=False):
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

    with open(input_fn) as f:
        inputs=f.readlines()[n_input+1:n_output-1]
    col_name_lst=[]
    col_value_lst=[]
    for line in inputs:
        string=line.split(' ')[-1]
        eid=string.find('=')
        if eid!=-1:
            col_name=string[:eid]
            col_value=eval(string[eid+1:-2])
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
        df.head()