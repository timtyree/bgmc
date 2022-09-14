import pandas as pd, numpy as np

###################################
# full models involved only
###################################
def recall_powerlaw_fits_to_full_models():
    """fits may be recomputed by evaluating the .ipynb associated with fitting powerlaws to the full models.
    here, w=M*q**m, and Delta_X is the maximum disagreement one could expect to observe with 95% confidence.
    here, we observe Delta_X concerns disagreements between statistically independent measurements of X.

    fits considered all values available

    Example Usage:
    wjr=recall_powerlaw_fits_to_full_models()
    print(*wjr)
    """
    # Recall powerlaw fits to full models
    # Fenton-Karma(PBC)
    # Luo-Rudy(PBC)

    #extra results for non conducting boundary conditions
    # Fenton-Karma(NCBC)
    # Luo-Rudy(NCBC)

    wjr = {
        'fk_pbc': {
            'm': 1.8772341309722325,
            'Delta_m': 0.02498750277237229,
            'M': 5.572315674840435,
            'Delta_M': 0.3053120355191732,
            'b': 1.665608066257863,
            'Delta_b': 0.029341409948945123
        },
        'lr_pbc': {
            'm': 1.6375562704001745,
            'Delta_m': 0.017190912126700632,
            'M': 16.73559858353835,
            'Delta_M': 0.8465090320196467,
            'b': 2.86877101880514,
            'Delta_b': 0.0311865277365552
        },
        'fk_ncbc': {
            'm': 1.854156794480594,
            'Delta_m': 0.024531267275222507,
            'b': 1.9249840368187936,
            'Delta_b': 0.033016842409840354,
            'Rsquared': 0.9960514654423748,
            'M': 7.135532649256891,
            'Delta_M': 0.4454472504725109
        },
        'lr_ncbc': {
            'm': 1.6611400039209039,
            'Delta_m': 0.026856157147378743,
            'b': 2.8636688985503183,
            'Delta_b': 0.055411463888674725,
            'Rsquared': 0.9873700703980065,
            'M': 16.75061667963681,
            'Delta_M': 1.2837944679833377
        }
    }
    return wjr

def recall_ncbc_powerlaw_fits():
    '''recall computation of birth rates for periodic boundary conditions
    compute w_lr and w_fk using a linear regression of a log-log plot
    Example Usage:
    ncbc=recall_ncbc_powerlaw_fits()
    '''
    ncbc = {
    'vidmar_rappel_fk_ncbc_w_-1': {
        'm': 0.9340032462691172,
        'Delta_m': 0.015405370185614163,
        'b': 0.5850078242378686,
        'Delta_b': 0.02380452732524641,
        'Rsquared': 0.9941565646923121,
        'M': 1.9098118080372346,
        'Delta_M': 0.07539284586139772
    },
    'vidmar_rappel_fk_ncbc_w_-2': {
        'm': 1.854156794480594,
        'Delta_m': 0.024531267275222507,
        'b': 1.9249840368187936,
        'Delta_b': 0.033016842409840354,
        'Rsquared': 0.9960514654423748,
        'M': 7.135532649256891,
        'Delta_M': 0.4454472504725109
    },
    'vidmar_rappel_fk_ncbc_w_1': {
        'm': 0.5537402145281756,
        'Delta_m': 0.025024289053941558,
        'b': -0.3447396643290329,
        'Delta_b': 0.04154280193734214,
        'Rsquared': 0.9646163261938806,
        'M': 0.7125880348532382,
        'Delta_M': 0.01571958815921015
    },
    'vidmar_rappel_fk_ncbc_w_2': {
        'm': 0.3660928979356132,
        'Delta_m': 0.00978377356513277,
        'b': 0.018131862295372836,
        'Delta_b': 0.015514091551474226,
        'Rsquared': 0.9848034263677132,
        'M': 1.0253626214778782,
        'Delta_M': 0.0200678350403789
    },
    'vidmar_rappel_lr_ncbc_w_-1': {
        'm': 1.0114623421424107,
        'Delta_m': 0.012683393484321563,
        'b': 1.9441221699252598,
        'Delta_b': 0.02874450593918872,
        'Rsquared': 0.9924845526364886,
        'M': 7.265560880659328,
        'Delta_M': 0.37047457235692693
    },
    'vidmar_rappel_lr_ncbc_w_-2': {
        'm': 1.6611400039209039,
        'Delta_m': 0.026856157147378743,
        'b': 2.8636688985503183,
        'Delta_b': 0.055411463888674725,
        'Rsquared': 0.9873700703980065,
        'M': 16.75061667963681,
        'Delta_M': 1.2837944679833377
    },
    'vidmar_rappel_lr_ncbc_w_1': {
        'm': 0.7706123216022909,
        'Delta_m': 0.03230010260685688,
        'b': 0.18915951129694153,
        'Delta_b': 0.07390920800200297,
        'Rsquared': 0.9334083117011656,
        'M': 1.1929319438876482,
        'Delta_M': 0.06997149338088682
    },
    'vidmar_rappel_lr_ncbc_w_2': {
        'm': 0.752730079269041,
        'Delta_m': 0.010445660898945816,
        'b': 1.1435455614126926,
        'Delta_b': 0.023860003093298793,
        'Rsquared': 0.9907623058081242,
        'M': 2.9883550824886997,
        'Delta_M': 0.10873027967246784
    }}
    return ncbc


###################################
# particle model involved
###################################
def recall_particle_parameter_fits(mode):
    '''modes are supported for mode in {'luorudy','fentonkarma'}.

    Example Usage:
    a,D,r,kappa,rmse=recall_particle_parameter_fits('luorudy')
    '''
    if mode=='luorudy':
        a=8.595; D=0.586055; r=0.10413888309470609; kappa=559.500160485693; rmse=0.028075538795257697
    elif mode=='fentonkarma':
        a=1.604153; D=0.365238; r=0.06045948522530842; kappa=495.2658318951493; rmse=0.006797222653889483
    return a,D,r,kappa,rmse

def recall_particle_parameter_measurements():
    """returns a tuple of measurements I made from the kinematics of the full models using ordinairy least squares. see main manuscript for details.

    Example Usage:
a_hat_FK, D_hat_FK, a_hat_FK_long, a_hat_FK_vlong, a_hat_LR, D_hat_LR, a_hat_LR_long=recall_particle_parameter_measurements()
    """
    #apparent measurements
    # #FK (a_hat short timescale, D_hat long timescale)
    a_hat_FK=1.65037#7.3923;
    D_hat_FK=0.365238#;num_pairs=25;tavg_step=5;tavg1_max=15;tavg2_max=15

    a_hat_FK_long = 1.509282#+/-0.178827 cm^2/s, tmax=90
    a_hat_FK_vlong = 1.604153#+/-0.040173 cm^2/s
    # tavg2=14 ms, num_samples=19087, tmin=0, tmax=300 ms

    #LR (a_hat short timescale, D_hat long timescale)
    a_hat_LR=9.60637#8.595
    D_hat_LR=0.586055#;num_pairs=25;tavg_step=5;tavg1_max=15;tavg2_max=15
    a_hat_LR_long = 3.535902#+/-0.312245 cm^2/s, tmax=60
    return a_hat_FK, D_hat_FK, a_hat_FK_long, a_hat_FK_vlong, a_hat_LR, D_hat_LR, a_hat_LR_long


def recall_death_rates_vidmar_rappel(data_fk_dir='/home/timothytyree/Documents/GitHub/bgmc/python/data/full_results/data_fig4_vidmar_fk_tt.csv',
                                     data_lr_dir='/home/timothytyree/Documents/GitHub/bgmc/python/data/full_results/data_fig4_vidmar_lr_tt.csv',**kwargs):
    """
    Example Usage:
dict_wjr = recall_death_rates_vidmar_rappel()
print(*dict_wjr)
model_str = 'fk_pbc'
# model_str = 'lr_pbc'
print_dict(dict_wjr['wjr'][model_str])
    """
    #recall powerlaw fits to full
    wjr=recall_powerlaw_fits_to_full_models()
    # #recall annihilation rate results from vidmar and rappel (2019)
    fk=pd.read_csv(data_fk_dir)
    fk['N']=fk['No2']*2
    fk['q']=fk['N']/fk['A'] #number of tips per square centimeter
    fk['w']=fk['rate']/fk['A']*10**3 #Hz/cm^2
    lr=pd.read_csv(data_lr_dir)
    lr['N']=lr['No2']*2
    lr['q']=lr['N']/lr['A'] #number of tips per square centimeter
    lr['w']=lr['rate']/lr['A']*10**3 #Hz/cm^2

    #evaluate min/max particle density observed
    qlim_fk =  [np.min(fk['q']),np.max(fk['q'])]
    qlim_lr =  [np.min(lr['q']),np.max(lr['q'])]
    dict_wjr=dict(wjr=wjr,fk=fk,lr=lr,qlim_fk=qlim_fk,qlim_lr=qlim_lr)
    return dict_wjr
