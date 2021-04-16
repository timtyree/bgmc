#!/usr/bin/env python3
import pandas as pd, os, dask.bag as db, time
# parse_output.py
# from .parse_output import *
import parse_output as po
# from . import parse_output as po

def get_files_in_folder(folder,trgt):
    '''gets all files in a given folder that contain a target string, trgt'''
    os.chdir(folder)
    fn_lst=os.listdir()
    ifl=[]
    for fn in fn_lst:
        if fn.find(trgt)!=-1:
            ifl.append(fn)
    return ifl

def filter_log(input_fn,save_folder,qfoo=None):
    cwd=os.getcwd()
    if qfoo==None:
        qfoo_pbc=lambda dict_inputs:dict_inputs['reflect']==0 #periodic bc
        qfoo_rbc=lambda dict_inputs:dict_inputs['reflect']==1 #reflecting bc
        # pick a general query function...
        qfoo=qfoo_rbc
    df=po.parse_log(input_fn,qfoo,include_inputs=True,printing=False)
    if df is None:
        return None
    os.chdir(save_folder)
    save_fn=os.path.basename(input_fn)
    df.to_csv(save_fn,index=False)
    os.chdir(cwd)
    return save_fn

def filter_folder(folder,qfoo,save_folder):
    '''filters Log and returns a merged pandas.Dataframe as *.csv
    returns the total runtime in years for all output files in folder.'''
    input_fn_lst=get_files_in_folder(folder,trgt='.out.')
    print(f"searching {len(input_fn_lst)} files...")
    def routine(input_fn):
        try:
            return filter_log(input_fn,save_folder,qfoo)
        except Exception as e:
            return None
    bag = db.from_sequence(input_fn_lst, npartitions=10).map(routine)
    start = time.time()
    retval_lst = list(bag)
    print(f"the run time for filtering files was {time.time()-start:.2f} seconds.")
    return retval_lst

if __name__=='__main__':
    #input qfoo
    # TODO(later): prompt user for input_query_function=lambda df: foo(df)
    #get folder
    qfoo=eval(input('Please enter a query function of the form "lambda dict_inputs:dict_inputs["reflect"]==0": \n'))
    # prompt user for save_fn
    save_fn = str(input("Please enter save folder name: \n"))
    nb_dir='/home/timothytyree/Documents/GitHub/bgmc/python'
    data_dir=f"{nb_dir}/data/osg_output/Log"
    save_folder=f"{nb_dir}/data/osg_output/{save_fn}"
    try:
        os.mkdir(save_folder)
    except Exception as e:
        pass
    #get df
    retval_lst=filter_folder(folder=data_dir,qfoo=qfoo, save_folder=save_folder)
    # df=pd.concat(df_lst).reset_index(drop=True)
    # df.to_csv(save_dir,index=False)
    print(f"the total number of trials matching query was {len(retval_lst)}")
    # print(f"final DataFrame stored in {save_dir}")
    beep = lambda x: os.system("echo -n '\\a';sleep 1.2;" * x)
    beep(3)
    print("Nota Bene: the output is currently not performing the average over logs (6x compression advisable...)")
