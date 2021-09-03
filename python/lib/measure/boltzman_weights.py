import numpy as np
from ..model.recall_fits import recall_powerlaw_fits_to_full_models

#TODO: wrap this
def comp_boltzman_weighted_weights(output_disagreement_values,**kwargs):
    energy_values=0.5*output_disagreement_values**2
    mean_free_energy=np.mean(energy_values)
    weight_values=np.exp(-energy_values/mean_free_energy)
    the_partition_function=np.sum(weight_values)
    weight_values/=the_partition_function
    return weight_values

def comp_boltzman_weighted_mean(output_disagreement_values,**kwargs):
    '''compute the boltzman weighted average of these K elite members'''
    weight_values=comp_boltzman_weighted_weights(output_disagreement_values,**kwargs)
    result_values=output_disagreement_values*weight_values
    mean_value=np.mean(result_values)
    return mean_value
#     print(f"the sum of the weights is {sum(weight_values)}") # one

def return_top_k_trials(df,output_col,ytrgt,k=6,**kwargs):
    """returns k rows that are have an absolute value of df[output_col] closest to ytrgt
    k=<the number of top trials to return>
    Example Usage:
    smallest_deviations=return_top_k_trials(df,output_col,ytrgt,k=k)
    """
    unsorted_series=np.abs(df[output_col]-ytrgt)
    indices_of_sorted=unsorted_series.argsort()
    smallest_deviations=indices_of_sorted.loc[:k].values
    return smallest_deviations

def compute_boltzman_defect_weighted_mean_for_top_k(df,input_cols=['r','kappa', 'D', 'varkappa'],output_col_lst=['m','M'],model_name_lst=None,k=6,printing=False,**kwargs):
    '''df=df_input[query] is a pandas.DataFrame instance assumed to have a unique trial
    for any unique combination of fields indicated by input_col
    #TODO: dev compute pca / correlation matrix about the mean
    #TDOO: use ^this correlation matrix to inspire random sampling clouds between the bwm of the top k trials for (i) m and (ii) M.

    Example Usage:
    df_bwm=pd.DataFrame(compute_boltzman_defect_weighted_mean_for_top_k(df=dg))
    df_bwm.head()
    '''
    df=df.reindex().copy()
    cols=list(input_cols)
    cols.extend(output_col_lst)

    wjr=recall_powerlaw_fits_to_full_models()
    if printing:
        print(f"recalled from lib the powerlaw fits for full models:")
        print(*wjr)

    if model_name_lst is None:
        model_name_lst=list(wjr.keys())

    m1avg_lst=[]
    M2avg_lst=[]
    dict_bwm={} #dictiionary of boltzmann weighted mean values
    dict_pca={}
    smallest_deviations_lst=[]
    #for 2-dimensional target space, such as m,M
    for model_name in model_name_lst:
        Ytrgt=(wjr[model_name][output_col_lst[0]],wjr[model_name][output_col_lst[1]])
        #for m
        ytrgt=Ytrgt[0]
        output_col=output_col_lst[0]
#         print(f"\nprinting the {k} indices closest to {output_col}={ytrgt} using Ytrgt={Ytrgt}")
        unsorted_series=np.abs(df[output_col]-ytrgt)
        indices_of_sorted=unsorted_series.argsort()
        smallest_deviations=indices_of_sorted.loc[:k-1].values
#         boo=unsorted_series.index.values==unsorted_series.loc[smallest_deviations[0]].values[0]
#         for sd in smallest_deviations[1:]:
#             sdd=unsorted_series.iloc[sd].values[0]
#             boo|=unsorted_series.index.values==sdd
    #     print(df.loc[smallest_deviations,cols])
        #compute the boltzmann weighted mean m
        output_disagreement_values=unsorted_series.iloc[indices_of_sorted].values[:k-1]#df.loc[boo,output_col].values
        boltzman_weighted_mean=comp_boltzman_weighted_mean(output_disagreement_values,**kwargs)
    #     print(f"the boltzman_weighted_mean for the K={k} elite members was {boltzman_weighted_mean}")
        M2avg_lst.append(boltzman_weighted_mean)

        #compute the boltzmann weighted average w.r.t. m
        weight_values=comp_boltzman_weighted_weights(output_disagreement_values,**kwargs)
#         elite_parameter_values=df.loc[boo].values#,cols]
        elite_parameter_values=df.iloc[indices_of_sorted].values[:k-1]
        dict_out=dict(zip(list(df.columns),np.sum(weight_values*elite_parameter_values.T,axis=1)))
        dict_out['top_trial_index']=int(smallest_deviations[0])
        dict_bwm[model_name+f'_{output_col}']=dict_out
        if printing:
            print(f"the boltzman_weighted mean parameter for the K={k} elite members was {dict_out}")

        #TODO: compute the correlation matrix/PCA on the mean squared differences?/just take random linear combinations in the interpolating space and take the max value

        #for M
        ytrgt=Ytrgt[1]
        output_col=output_col_lst[1]
    #     print(f"\nprinting the {k} indices closest to M={ytrgt}")
        unsorted_series=np.abs(df[output_col]-ytrgt)
        indices_of_sorted=unsorted_series.argsort()
        smallest_deviations=indices_of_sorted.loc[:k-1].values
#         boo=unsorted_series.index.values==unsorted_series.loc[smallest_deviations[0]].values[0]
#         for sd in smallest_deviations[1:]:
#             sdd=unsorted_series.iloc[sd].values[0]
#             boo|=unsorted_series.index.values==sdd
    #     print(df.loc[smallest_deviations,cols])
        #compute the boltzmann weighted mean m
        output_disagreement_values=unsorted_series.iloc[indices_of_sorted].values[:k-1]#df.loc[boo,output_col].values
        boltzman_weighted_mean=comp_boltzman_weighted_mean(output_disagreement_values,**kwargs)
    #     print(f"the boltzman_weighted_mean for the K={k} elite members was {boltzman_weighted_mean}")
        M2avg_lst.append(boltzman_weighted_mean)

        #compute the boltzmann weighted average w.r.t. m
        weight_values=comp_boltzman_weighted_weights(output_disagreement_values,**kwargs)
#         elite_parameter_values=df.loc[boo].values#,cols]
        elite_parameter_values=df.iloc[indices_of_sorted].values[:k-1]
        dict_out=dict(zip(list(df.columns),np.sum(weight_values*elite_parameter_values.T,axis=1)))
        dict_out['top_trial_index']=int(smallest_deviations[0])
        dict_bwm[model_name+f'_{output_col}']=dict_out
    #     print(f"the boltzman_weighted mean parameter for the K={k} elite members was {dict_out}")
    return dict_bwm #,smallest_deviations_lst
