import yaml,os
#forked from article:
# https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started

def read_yaml(input_fn):
    '''returns dict instance.  input_fn is a string locating a yaml file.

    Example Usage:
dictionary = read_yaml(input_fn)
    '''
    stream = open(input_fn, 'r')
    # dictionary = yaml.load(stream)
    dictionary = yaml.safe_load(stream)
    return dictionary
    # for key, value in dictionary.items():
    # print (key + " : " + str(value))

def load_from_yaml(input_fn):
    '''returns dict instance.  input_fn is a string locating a yaml file.

    Example Usage:
dictionary = load_from_yaml(input_fn)
    '''
    return read_yaml(input_fn)

def save_to_yaml(save_fn,mdict):
    '''saves dict instance to .yaml.

    Example Usage:
documents = save_to_yaml(input_fn,mdict)
    '''
    with open(save_fn, 'w') as file:
        documents = yaml.dump(mdict, file)
        return documents
        #return os.path.abspath(input_fn)

if __name__ == '__main__':
    stream = open("foo.yaml", 'r')
    dictionary = yaml.safe_load_all(stream)

    for doc in dictionary:
        print("New document:")
        for key, value in doc.items():
            print(key + " : " + str(value))
            if type(value) is list:
                print(str(len(value)))
