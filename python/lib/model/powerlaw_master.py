# powerlaw_master.py
#Programmer: Tim Tyree
#Date: 10.7.2022
import numpy as np

def comp_powerlaw_intersection(Mp,nup,Mm,num,xv=None,use_next=False,**kwargs):
    """
    Example Usage:
xv = np.arange(0.02, 1,0.01)
qstar,wstar = comp_powerlaw_intersection(Mp,nup,Mm,num,xv=xv)
    """
    if xv is None:
        xv = np.arange(0.02, 1,0.01)
    # evaluate powerlaw fits of birth rates wjr
    yv_birth = Mp*xv**nup
    yv_death = Mm*xv**num

    #compute the intersection point for both of the full models
    # index = np.argmin(np.log(yv_birth/yv_death)**2)
    index = np.argmin(np.exp(np.log(yv_birth/yv_death)**2))
    if use_next:
        index+=1
    qstar = xv[index]
    wstar = yv_birth[index]
    return qstar,wstar


def get_comp_W(A,nu,M):
    """
    Example Usage:
comp_Wp = get_comp_W(A,nup,Mp)
comp_Wm = get_comp_W(A,num,Mm)
    """
    MA = M*A
    def comp_W(n):
        return MA * (n/A) **nu
    return comp_W

def comp_quasistatic_distrib_paired_bdrates(comp_Wm,comp_Wp,num_iter=20,freq_prev=1.,**kwargs):
    """
    Parameters:
    - comp_Wm,comp_Wp: returned by get_comp_W
    - num_iter: max number of particles considered divided by two.
    - freq_prev: arbitrary postive value for the frequency of base case.

    Example Usage:
comp_Wp = get_comp_W(A,nup,Mp)
comp_Wm = get_comp_W(A,num,Mm)
n_qs,prob_qs = comp_quasistatic_distrib_paired_bdrates(comp_Wm,comp_Wp,num_iter=20)
    """
    #base case
    freq_cur = ((comp_Wm(2)+comp_Wp(2))/comp_Wm(4))*freq_prev
    n_lst=[2,4]
    freq_lst=[freq_prev,freq_cur]

    #next case
    n=4 #current number of particles
    for step in range(num_iter-2):
        freq_next = (comp_Wp(n) + comp_Wm(n))*freq_cur - comp_Wp(n-2)*freq_prev
        freq_next /= comp_Wm(n+2)
        #update next to current
        n+=2
        freq_prev = freq_cur
        freq_cur  = freq_next
        #record
        n_lst.append(n)
        freq_lst.append(freq_cur)
        #print(f"{n=}: {freq_cur=:.4f}")

    n_qs = np.array(n_lst)
    prob_qs = np.array(freq_lst)
    #normalize the quasistationary distribution
    prob_qs /=np.sum(prob_qs)
    return n_qs,prob_qs


#################################
# variational analysis of action
#################################
#TODO: move to models
#DONE: implement each action variables
def get_phi(comp_Wm,comp_Wp):
    """

    Example Usage:
phi = get_phi(comp_Wm,comp_Wp)
    """
    def phi(k):
        product=1.
        for i in range(int(k/2)):
            #print(f"{k=}: {i=}  <-- does that look reasonable?")
            #i start with zero and end with int(k/2)-1. ==> anwswer: yes.
            ii=i+1 #correct for 0 indexing
#             product *= comp_Wm(2*ii) + comp_Wp(2*ii) #A
#             product *= comp_Wm(2*ii)                 #B
            product *= comp_Wm(2*ii)                 #C
#             product *= comp_Wp(2*ii)                 #D
#             product /= comp_Wp(2*ii)                 #A
#             product /= comp_Wm(2*ii) + comp_Wp(2*ii) #B
            product /= comp_Wp(2*ii)                 #C
#             product /= comp_Wm(2*ii) + comp_Wp(2*ii) #D
        return product
    return phi

#DONE: dev map from eval_tau_expression to eval_tau
def get_eval_tau(eval_tau_expression):
    def eval_tau(n_qs, prob_qs, phi, comp_Wm, comp_Wp, printing=True,**kwargs):
        """
        Example Usage:
phi = get_phi(comp_Wm,comp_Wp)
eval_tau= get_eval_tau(eval_tau_expression)
tau = eval_tau(n_qs, prob_qs, phi, comp_Wm, comp_Wp, printing=True,**kwargs)
        """
        #evaluate tau_qs
        num_vals=n_qs.shape[0]
        tau_qs=np.zeros(num_vals)
        maxinf_num_inner_sum = n_qs[-1]
        # maxinf_num_inner_sum = int(n_qs[-1]/2)  #5 second run time
        for i,n in enumerate(n_qs):
            n_over_2 = int(n/2)
            assert n_over_2<=maxinf_num_inner_sum#
            tau_qs[i]=eval_tau_expression(n_over_2 ,phi, comp_Wm, comp_Wp,
                                          maxinf_num_inner_sum=maxinf_num_inner_sum,
                                          printing=printing)
        #average tau_qs over n_qs,prob_qs
        tau = np.sum(tau_qs*prob_qs)
        #does nothing for properly normalized qs. comfirmed to 5 sig. figs.
        tau/= np.sum(prob_qs)
        return tau
    return eval_tau

#DONE: implement the hypotheses
def eval_tau_expression(n_over_2, phi, comp_Wm, comp_Wp, maxinf_num_inner_sum=20,printing=True, **kwargs):
    """compute mean first passage time conditioned on initial number of particles.
    phi, comp_Wm, comp_Wp evaluate to the action variable, death rate, and birth rate, respectively.

    Example Usage:
n_over_2 = int(np.floor(n/2))
tau = eval_tau_expression(n_over_2,phi, comp_Wm, comp_Wp, maxinf_num_inner_sum=20)
    """
    assert n_over_2<=maxinf_num_inner_sum#
    outer_sum=0.
    for k in range(n_over_2):
        kk = k+1 #correct for 1 indexing
        inner_sum=0.
        # for j in range(k,maxinf_num_inner_sum):
        for j in range(kk,maxinf_num_inner_sum):
            #jj = j+1 #correct for 1 indexing
            summand = 1.
            summand/= phi(2*j)*comp_Wp(2*j)  #1b
            # summand/= phi(2*jj)*comp_Wp(2*jj)  #1
            # #summand/= phi(2*jj)*comp_Wm(2*(jj-1))  #2
            #print(f"{k=}: {j=}: {summand=}\r")
            inner_sum += summand
        # inner_sum *= phi(2*(kk-1))
        inner_sum *= phi(2*k)
        #inner_sum *= phi(2*(k-1))
        outer_sum += inner_sum
        if printing:
            print(f"{k=}: {j=}: {outer_sum=:.4f}, {inner_sum=:.4f}")
            #print(f"{k=}: {j=}: {outer_sum=:.4f} from {inner_sum=:.4f}\r")
    return outer_sum
