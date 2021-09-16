import yaml
#forked from article:
# https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started

def read_yaml(input_fn):
    '''returns dict instance.  input_fn is a string locating a yaml file.'''
    stream = open(input_fn, 'r')
    dictionary = yaml.load(stream)
    return dictionary
    # for key, value in dictionary.items():
    # print (key + " : " + str(value))


if __name__ == '__main__':
    stream = open("foo.yaml", 'r')
    dictionary = yaml.safe_load_all(stream)

    for doc in dictionary:
        print("New document:")
        for key, value in doc.items():
            print(key + " : " + str(value))
            if type(value) is list:
                print(str(len(value)))
