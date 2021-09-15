from ..my_initialization import *
from .. import *
from ..viewer.gener_q_vs_w_for_df import *
def return_best_trial_parameters(input_fn,model_name_full='fk_pbc',num_points=25,sortby_col='rmse_full',input_cols=None,**kwargs):
    '''returns the best_trial_parameters according to RMSE of full model indicated by model_name_full
    input_fn locates a .csv with all powerlaw fits in it
    model_name_full is from {'fk_pbc','lr_pbc'}

    Example Usage:
    input_fn=f"/home/timothytyree/Documents/GitHub/bgmc/python/data/osg_output/run_18_all_powerlaw_fits.csv"
    dict_best=return_best_trial_parameters(input_fn,model_name_full='fk_pbc',num_points=25)
    '''
    df_fits=pd.read_csv(input_fn)
    #define constant parameters
    reflect=0
    force_code=2
    set_second=0
    neighbor=0
    no_attraction=0
    no_repulsion=0
    # kappa=100
    L=10

    #template query for the DataFrame
    df=df_fits.copy()
    query =(df.set_second==set_second)
    query&=(df.no_repulsion==no_repulsion)&(df.no_attraction==no_attraction)
    query&=(df.neighbor==neighbor)&(df.force_code==force_code)
    # query&=df.r==r
    # query&=df.kappa==kappa
    # query&=df.D==D
    query&=df.L==L
    query_template=query.copy()

    #select only the desired trials for the FK model
    # model_name_full='fk_pbc'#'lr_pbc'
    # model_name_full='lr_pbc'

    # c_col='rmse_full'
    # fontsize=16
    # x1lim=[0,15]
    # x2lim=[50,750]
    # # x1lim=[5,10]
    # # x2lim=[50,350]

    if input_cols is None:
        input_cols=['r','kappa','D','varkappa','x0', 'L', 'force_code', 'neighbor', 'reflect', 'set_second',
           'no_repulsion', 'no_attraction']

    query=query_template.copy()
    query&=(df.reflect==reflect)
    query&=(df.model_name_full==model_name_full)
    # query&=df.varkappa==varkappa
    # query&=df.x0==x0

    if model_name_full=='fk_pbc':
        modelname='Fenton-Karma'
    elif model_name_full=='lr_pbc':
        modelname='Luo-Rudy'
    else:
        raise(f'Not Yet Implemented! {model_name_full}')
    dg=df[query].sort_values(by=sortby_col).copy()
    # #extract the data
    # r_values=dg.head(num_points)['r'].values
    # kappa_values=dg.head(num_points)['kappa'].values
    # c_values=dg.head(num_points)[c_col].values

    #get the list of best parameter values
    dict_best_parameter_values_sorted=dict(zip(input_cols,dg[input_cols].values[:num_points].T))
    dict_best=dict_best_parameter_values_sorted
    return dict_best

def gener_bluf_q_vs_w_for_top_powerlaw_fits(input_fn,model_name_full='fk_pbc',num_points=25,sortby_col='rmse_full',input_cols=None,bluf_dir=None,**kwargs):
    text_left =("(left column) the mean annihilation rate, $w$, versus the particle number density, $q$, for (blue) the Fenton-Karma model, (orange) the Luo-Rudy model, and (red) the particle model.  The parameters of the particle models were selected as the critical points found in the $(r,a)$ plane with $D$ and $\kappa$ fixed.")
    text_right=("(right column) the disagreement of the mean annihilation rate of the particle model with that of the full model.  Error bars represent the 95% confidence intervals for the particle model, supposing there is zero uncertainty from the full model.")
    wjr=recall_powerlaw_fits_to_full_models()
    #copy/paste of Example Usage in bluf.py
    modname=os.path.basename(input_fn)
    save_folder=os.path.dirname(input_fn)
    # save_folder=f"{nb_dir}/../fig"
    if bluf_dir is None:
        bluf_dir = save_folder+f"/{modname}_top_{num_points}_plotted_{model_name_full}.pdf"
    # bluf_dir = f"{nb_dir}/Figures/{modname}_plotted.pdf"
    #########################
    # initialize the task_lst
    #########################
    # settings from lib
    # nb_dir=os.path.dirname(os.path.dirname(os.getcwd()))
    #find all files matching pattern
    # input_fn_lst=get_all_files_matching_pattern(file=input_fn,trgt='')
#     input_fn_lst=os.listdir(os.path.dirname(input_fn))
    # input_fn_lst=os.listdir(os.path.dirname(input_fn))
    os.chdir(os.path.dirname(input_fn))

#     #limit to the maximum number of trials
#     if max_num_trials is not None:
#         if len(input_fn_lst)>int(max_num_trials):
#             input_fn_lst=input_fn_lst[:max_num_trials]

    #define the lists of plotter tasks
    task_lst = [
        (text_plotter_function,text_left),
        (text_plotter_function,text_right)
    ]

    #####################
    # plot the top trials
    #####################
    dict_best=return_best_trial_parameters(input_fn,model_name_full=model_name_full,num_points=num_points)
    #load the collection of all such rates
    raw_data_dir=input_fn.replace('_powerlaw_fits.csv','.csv')
    df_raw=pd.read_csv(raw_data_dir)
    df=df_raw
    df['A']=df['L']**2
    df['q']=df['N']/df['A'] #number of tips per square centimeter
    df['w']=df['CollRate']/df['A'] #[mHz?]/cm^2

    #define constant parameters
    reflect=0
    force_code=2
    set_second=0
    neighbor=0
    no_attraction=0
    no_repulsion=0
    x0=0
    L=10

    #template query for the DataFrame
    df=df_raw.copy()
    query =(df.set_second==set_second)
    query&=(df.no_repulsion==no_repulsion)&(df.no_attraction==no_attraction)
    query&=(df.neighbor==neighbor)&(df.force_code==force_code)
    query&=df.L==L
    query&=df.x0==x0
    query&=(df.reflect==reflect)
    query_template=query.copy()

    #DONE: initialize task list as in the previous bluf routine
    for r,kappa,varkappa,D in zip(dict_best['r'],dict_best['kappa'],dict_best['varkappa'],dict_best['D']):
        #query for the xy values for the top model
        query=query_template.copy()
        query&=df.r==r
        query&=df.kappa==kappa
        query&=df.varkappa==varkappa
        query&=df.D==D
        dg=df[query].copy()

        #append to task_lst
        task_lst.append((q_vs_w_plotter_function_from_df, dg))
        task_lst.append((q_vs_Delta_w_plotter_function_from_df, dg))


    print(f'saving .pdf to\n{bluf_dir}...')
    gener_bluf(task_lst, bluf_dir, save_tight=True)
    return bluf_dir

if __name__=="__main__":
    #the full bluf routine start to finish
    # input_fn=search_for_file()
    input_fn=f"/home/timothytyree/Documents/GitHub/bgmc/python/data/osg_output/run_18_all_powerlaw_fits.csv"
    bluf_dir=gener_bluf_q_vs_w_for_top_powerlaw_fits(input_fn,model_name_full='fk_pbc',num_points=25)
    bluf_dir=gener_bluf_q_vs_w_for_top_powerlaw_fits(input_fn,model_name_full='lr_pbc',num_points=25)
    bluf_dir=gener_bluf_q_vs_w_for_top_powerlaw_fits(input_fn,model_name_full='fk_pbc',num_points=250)
    bluf_dir=gener_bluf_q_vs_w_for_top_powerlaw_fits(input_fn,model_name_full='lr_pbc',num_points=250)
    #open the outputed .pdf automatically
    import webbrowser
    webbrowser.open_new(r'file://' + bluf_dir);
