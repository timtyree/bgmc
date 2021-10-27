from .. import *
from ..lib_care.measure.level_sets import compute_self_consistent_astar_rstar

def routine_locate_star_settings(df,wjr):
  #compute the contour values for fk_pbc and lr_pbc and record the intersections in df_star
  x1_col='r'
  x2_col='varkappa'
  nsamples=1000
  navg=50
  mode='spline'#'linear'
  printing=False
  # D=2
  # D_lst=[2,0.7,14]
  D_lst=sorted(set(df.D.values))[::-1]
  print(f"D_lst={D_lst}")
  kappa_lst=sorted(set(df.kappa.values))[::-1]
  print(f"iterating over kappa_lst={kappa_lst} and the PBC full model results...")
  dict_out_lst=[]
  #FK model
  model_name='fk_pbc'
  for D in D_lst:
      for kappa in kappa_lst:
          query = (df['D']==D)
          query&= (df['kappa']==kappa)
          query&= query_template
          X=df.loc[query,[x1_col,x2_col]].values

          #computation of level set curves set to powerlaw fits from the full models
          if printing:
              print(f"for the {model_name} model, when kappa={kappa:.0f} Hz and D={D:.2f} cm^2/s...")
          output_col='m'
          m=float(wjr[model_name][output_col])
          y=df.loc[query,output_col].values
          try:
              contour_m_values=comp_longest_level_set_and_smooth(X,y,level=m,navg=navg)
          except AssertionError as e:#assert(num_contours>0)
              contour_m_values=None
          output_col='M'
          M=float(wjr[model_name][output_col])
          y=df.loc[query,output_col].values
          try:
              contour_M_values=comp_longest_level_set_and_smooth(X,y,level=M,navg=navg)
          except AssertionError as e:#assert(num_contours>0)
              contour_M_values=None

          if (contour_m_values is not None) and (contour_M_values is not None):
              contour_m_values_LR=contour_m_values.copy()
              contour_M_values_LR=contour_M_values.copy()

              try:
                  #compute the self-consistent intersection points
                  rstar,astar=compute_self_consistent_astar_rstar(contour_m_values,contour_M_values)
              except AssertionError as e:#assert (x1star_values.shape[0]>0)
                  rstar=np.nan
                  astar=np.nan
          else:
              rstar=np.nan
              astar=np.nan

          #collect results into a dictionary
          dict_out={
              'model_name':model_name,
              'rstar':rstar,
              'astar':astar,
              'kappa':kappa,
              'D':D,
              'm':m,
              'M':M
          }
          # append that dict to list
          dict_out_lst.append(dict_out)
  #LR model
  model_name='lr_pbc'
  for D in D_lst:
      for kappa in kappa_lst:
          query = (df['D']==D)
          query&= (df['kappa']==kappa)
          query&= query_template
          X=df.loc[query,[x1_col,x2_col]].values

          if printing:
              print(f"for the {model_name} model, when kappa={kappa:.0f} Hz and D={D:.2f} cm^2/s...")

          output_col='m'
          m=float(wjr[model_name][output_col])
          y=df.loc[query,output_col].values
          try:
              contour_m_values=comp_longest_level_set_and_smooth(X,y,level=m,navg=navg)
          except AssertionError as e:#assert(num_contours>0)
              contour_m_values=None
          output_col='M'
          M=float(wjr[model_name][output_col])
          y=df.loc[query,output_col].values
          try:
              contour_M_values=comp_longest_level_set_and_smooth(X,y,level=M,navg=navg)
          except AssertionError as e:#assert(num_contours>0)
              contour_M_values=None

          if (contour_m_values is not None) and (contour_M_values is not None):
              contour_m_values_LR=contour_m_values.copy()
              contour_M_values_LR=contour_M_values.copy()

              try:
                  #compute the self-consistent intersection points
                  rstar,astar=compute_self_consistent_astar_rstar(contour_m_values,contour_M_values)
              except AssertionError as e:#assert (x1star_values.shape[0]>0)
                  rstar=np.nan
                  astar=np.nan
          else:
              rstar=np.nan
              astar=np.nan
          #collect results into a dictionary
          dict_out={
              'model_name':model_name,
              'rstar':rstar,
              'astar':astar,
              'kappa':kappa,
              'D':D,
              'm':m,
              'M':M
          }
          # append that dict to list
          dict_out_lst.append(dict_out)

  df_star=pd.DataFrame(dict_out_lst)
  return df_star
