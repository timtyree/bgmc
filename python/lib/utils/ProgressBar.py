#!/bin/env python3
# def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = u'\u2764', printEnd = "\r"):
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Prints iteration progress.  Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    # if iteration == total:
    #     print(u'\n\u2764')

## Example Usage:
# import time
# # A List of Items
# items = list(range(0, 57))
# l = len(items)
# # Initial call to print 0% progress
# printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
# for i, item in enumerate(items):
#     # Do stuff...
#     time.sleep(0.1)
#     # Update Progress Bar
#     printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)


import sys
def progressbar(it, prefix="", size=60,
        char=u"█",#"#",
        out=sys.stdout):
    """
    for python 3.3+,


    Example Usage:
import time
for i in progressbar(range(15), "Computing: ", 40):
    time.sleep(0.1) # any code you need
    """
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, char*x, "."*(size-x), j, count),
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)
