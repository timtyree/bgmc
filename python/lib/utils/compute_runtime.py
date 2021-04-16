#!/usr/bin/env python3
import datetime, os, dask.bag as db, time
import dateutil.parser as dp
def parse_runtime(input_fn):
    seconds_in_day = 24 * 60 * 60
    seconds_in_year = seconds_in_day * 365
    with open(input_fn) as f:
        line_first = f.readline()
        for n, line in enumerate(f):
            line_last = f.readline()
    # import dateutil.tz as tz
    time_start = dp.parse(line_first[:-1], ignoretz=True)
    time_end = dp.parse(line_last[:-1], ignoretz=True)
    difference = time_end - time_start
    # divmod(difference.days * seconds_in_day + difference.seconds, 60)#(min,sec)
    seconds = difference.days * seconds_in_day + difference.seconds
    years = seconds / seconds_in_year
    return years

def get_files_in_folder(folder,trgt):
    '''gets all files in a given folder that contain a target string, trgt'''
    os.chdir(folder)
    fn_lst=os.listdir()
    ifl=[]
    for fn in fn_lst:
        if fn.find(trgt)!=-1:
            ifl.append(fn)
    return ifl

def compute_runtime_for_folder(folder):
    '''returns the total runtime in years for all output files in folder.'''
    input_fn_lst=get_files_in_folder(folder,trgt='.out.')
    print(f"computing runtime for {len(input_fn_lst)} files...")
    def routine(input_fn):
        try:
            return parse_runtime(input_fn)
        except Exception as e:
            return 0.
    b = db.from_sequence(input_fn_lst, npartitions=11).map(routine)
    start = time.time()
    runtime_lst = list(b)
    print(f"the run time for computing runtimes was: {time.time()-start:.2f} seconds.")
    return sum(runtime_lst)

if __name__=='__main__':
    nb_dir='/home/timothytyree/Documents/GitHub/bgmc/python'
    data_dir=f"{nb_dir}/data/osg_output/Log"
    runtime=compute_runtime_for_folder(folder=data_dir)
    print(f"the total recorded runtime was {runtime:.3f} years.")
    beep = lambda x: os.system("echo -n '\\a';sleep 0.2;" * x)
    beep(3)
