import matplotlib.backends.backend_pdf, matplotlib.pyplot as plt,random, os

def save_fig(fig, name, dpi=400):
    pp = PdfPages(name)
    pp.savefig(fig, bbox_inches='tight', pad_inches=0, dpi=dpi)
    pp.close()

def format_plot(ax=None,xlabel=None,ylabel=None,fontsize=20,use_loglog=False,xlim=None,ylim=None,use_bigticks=True,**kwargs):
    '''format plot formats the matplotlib axis instance, ax,
    performing routine formatting to the plot,
    labeling the x axis by the string, xlabel and
    labeling the y axis by the string, ylabel
    '''
    if not ax:
        ax=plt.gca()
    if use_loglog:
        ax.set_xscale('log')
        ax.set_yscale('log')
    if xlabel:
        ax.set_xlabel(xlabel,fontsize=fontsize,**kwargs)
    if ylabel:
        ax.set_ylabel(ylabel,fontsize=fontsize,**kwargs)
    if use_bigticks:
        ax.tick_params(axis='both', which='major', labelsize=fontsize,**kwargs)
        ax.tick_params(axis='both', which='minor', labelsize=0,**kwargs)
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_xlim(ylim)
    return True

def set_size(w,h, ax=None):
    """ w, h: width, height in inches """
    if not ax: ax=plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw, figh)

def chunks(l, n):
    """yields successive n-sized chunks from l.
    chunks can divide l into chunks"""
    for i in range(0, len(l), n):
        yield l[i:i + n]
