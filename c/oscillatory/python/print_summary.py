import pandas as pd
#TODO: move the following to an executable routine!
def print_summary(df_sum,input_fn):
    df_sum=pd.read_csv(sum_fn,index_col="N")
    #compute Tavg
    df_sum['Tavg']=df_sum['CollTime']/df_sum['count']
    # print(df_sum.head())

    # print(parse_runtime(input_fn))
    trgt='Printing Outputs...'
    with open(input_fn,'r') as f:
        triggered=False
        for line in f:
            if line[:len(trgt)]==trgt:
                triggered=True
            if triggered is False:
                print(line[:-1])
    #reconstruct my preexisting output print after Printing Outputs...
    print(trgt)
    strng=''
    for val in df_sum.index.values:
        strng=strng+f"{val:d},"
    print(strng)
    strng=''
    for val in df_sum.Tavg.values:
        strng=strng+f"{val:.6f},"
    print(strng)

if __name__=='__main__':
    import sys
    input_fn=sys.argv[1]
    sum_fn=sys.argv[2]
    # sum_fn='sum.csv'
    # input_fn='../Log/example-output.txt'
    df_sum=pd.read_csv(sum_fn,index_col="N")
    # boo_sum=df_sum.CollTime!=-9999
    print_summary(df_sum,input_fn)