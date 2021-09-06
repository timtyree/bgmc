from ..my_initialization import *
from .. import *
# from . import *
# import random,scipy

def gener_bluf_q_vs_w_for_csv_folder(input_fn):
    text_left =("(left column) the mean annihilation rate, $w$, versus the particle number density, $q$, for (blue) the Fenton-Karma model, (orange) the Luo-Rudy model, and (red) the particle model.  The parameters of the particle models were selected as the critical points found in the $(r,a)$ plane with $D$ and $\kappa$ fixed.")
    text_right=("(right column) the disagreement of the mean annihilation rate of the particle model with that of the full model.  Error bars represent the 95% confidence intervals for the particle model, supposing there is zero uncertainty from the full model.")
    wjr=recall_powerlaw_fits_to_full_models()
    #copy/paste of Example Usage in bluf.py
    modname=os.path.basename(os.path.dirname(input_fn))
    save_folder=os.path.dirname(os.path.dirname(input_fn))
    # save_folder=f"{nb_dir}/../fig"
    bluf_dir = save_folder+f"/{modname}_plotted.pdf"
    # bluf_dir = f"{nb_dir}/Figures/{modname}_plotted.pdf"

    # settings from lib
    # nb_dir=os.path.dirname(os.path.dirname(os.getcwd()))
    #find all files matching pattern
    # input_fn_lst=get_all_files_matching_pattern(file=input_fn,trgt='')
    input_fn_lst=os.listdir(os.path.dirname(input_fn))
    # input_fn_lst=os.listdir(os.path.dirname(input_fn))
    os.chdir(os.path.dirname(input_fn))
    #define the lists of plotter tasks
    task_lst = [
        (text_plotter_function,text_left),
        (text_plotter_function,text_right)
    ]
    for fn in input_fn_lst:
        task_lst.append((q_vs_w_plotter_function, os.path.abspath(fn)))
        task_lst.append((q_vs_Delta_w_plotter_function, os.path.abspath(fn)))

    print(f'saving .pdf to\n{bluf_dir}...')
    gener_bluf(task_lst, bluf_dir, save_tight=True)
    return bluf_dir


if __name__=="__main__":
    #the full bluf routine start to finish
    # input_fn=search_for_file()
    input_fn="/home/timothytyree/Documents/GitHub/bgmc/python/data/osg_output/run_16_all/job.out.14688026.0"
    gener_bluf_q_vs_w_for_csv_folder(input_fn)
    # gener_bluf(task_lst, bluf_dir, bbox_inches='tight', save_tight=True)
    beep(3)

    #open the outputed .pdf automatically
    import webbrowser
    webbrowser.open_new(r'file://' + bluf_dir);
