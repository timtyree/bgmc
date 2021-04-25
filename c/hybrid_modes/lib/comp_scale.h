
doube pi=3.141592653589793;

double[2] comp_M_tilde(m){
    '''non-quadratic trend is guessed to make bounds'''
    val_lst=[]
    val_lst.append(np.pi**(m-1)/m)
    val_lst.append(np.pi**(m-1)/2)
    val_lst.append(np.pi/2)
    val_lst.append((np.pi/2)**(m-1))
    mn=np.min(val_lst)
    mx=np.max(val_lst)
    return mn,mx
}

double[2] comp_kappa(){
  // returns a min/max estimate for kappa using the emergent universal law
  return (kappa_mx, kappa_mn)
}

def comp_kappa(M,m,r):
    '''returns a min/max estimate for kappa using the emergent universal law'''

    mn,mx=comp_M_tilde(m)
    kappa_mn=r**(-2*(m-1))*M/mx
    kappa_mx=r**(-2*(m-1))*M/mn
    return kappa_mn,kappa_mx
