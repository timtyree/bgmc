#dict_func.py
#Programmer: Tim Tyree
#Date: 9.13.2022

def dict_compare(d1, d2):
    """dict_compare returns a tuple of sets containing keys to dict1 or dict2.

    Example Usage:
added, removed, modified, same = dict_compare(d1=dict(a=1, b=2), d2=dict(a=2, b=2))
added, removed, modified, same
"""
    d1_keys  = set(d1.keys())
    d2_keys  = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added    = d1_keys - d2_keys
    removed  = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    same = set(o for o in shared_keys if d1[o] == d2[o])
    return added, removed, modified, same
