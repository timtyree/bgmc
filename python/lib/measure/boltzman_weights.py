import numpy as np

#TODO: wrap this
def comp_boltzman_weighted_weights(output_disagreement_values,**kwargs):
    mean_free_energy=np.mean(0.5*output_disagreement_values**2)
    weight_values=np.exp(-output_disagreement_values/mean_free_energy)
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
