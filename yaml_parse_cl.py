import yaml
import pydoc
import typing

def find_absolute(yamld, path_string):
    """
    User-frendly version of find_absolute_h function
    """
    return find_absolute_h(yamld, path_string.split("."))



def find_absolute_h(yamld, path_list) :
    """
    Absolute path is the location of the key in the yaml file 
    e.g spec.template.metadata.labels.app
    """
    if isinstance(yamld, list):
        return list(map(lambda x: find_absolute_h(x, path_list),yamld))
    if len(path_list) == 0:
        return yamld
    #for 3.x python
    #head, *tail = path_list
    head, tail = path_list[0], path_list[1:]
    if isinstance(yamld, dict):
        if head in yamld.keys(): 
            return find_absolute_h(yamld[head],tail)
    return []


def yaml_to_dict (filename):
    """
    Parse valid .yaml file to dict
    """
    with open(filename) as f:
        try:
            content = yaml.safe_load(f)
            return content
        except:
            print("yaml_to_dict: Parser Error. The YAML file isn't valid")



def find_all_keys(yamld: dict, target: str) -> list:
    """
    Find all {key:value} in dictionary by target key.
    Insensible to the level of nesting.
    """
    found=[]
    for (k,v) in yamld.items():
        if k == target:
            found += [{k:v}]
        if isinstance(v, dict):
            found += find_all_keys(v, target)
        if isinstance(v, list):
            for i in v:
                if isinstance(i,dict):
                    found += find_all_keys(i, target)
    return found


def concat_list(l):
    """
    Concat lists of different nesting levels into one "flat" list
    """
    if isinstance(l,str):
        return l
    if len(l) == 0:
        return []
    if isinstance(l[0],list):
        #calling function on the head and tail sublists
        return list(concat_list(l[0])) + concat_list(l[1:])
    #by default concat list of one head element with rest elements
    return [l[0]] + concat_list(l[1:])

def none_filter(l: list) -> list:
    """
    Filter all None elements in the list
    """
    if isinstance(l,list):
        return list(filter(lambda x: not x is None,l))  

def flat_keys(prefix,yamld):
    """
    Flattening of all dictionary keys. Deep Crawl.
    Example: {key1:{key2: value2},key3:value3, key4:[value41, value42]} -> [key1.key2, key3, key4]
    """
    depth = []
    if isinstance(yamld,str):
        return prefix 
    if isinstance(yamld,dict):
        for (k,v) in yamld.items():
            depth.append(flat_keys(prefix+"."+k,v))
    if isinstance(yamld,list):
        depth=list(map(lambda x: flat_keys(prefix,x),yamld))
    return depth


test=flat_keys("",yaml_to_dict("pod.yaml"))


def flat_values(prefix,yamld):
    """
    Flattening of all dictionary values. Deep Crawl.
    Example: {key1:{key2: value2},key3:value3, key4:[value41, value42]} -> [key1.key2.value2, key3.value3 key4.value41, key4.value42]
    """
    depth = []
    if isinstance(yamld,str):
        return prefix +"."+ yamld
    if isinstance(yamld,dict):
        for (k,v) in yamld.items():
            depth.append(flat_values(prefix+"."+k,v))
    if isinstance(yamld,list):
        depth=list(map(lambda x: flat_values(prefix,x),yamld))
    return depth

def drop_lead_ch(l):
    """
    Erase head element in every member of the list
    """
    if isinstance(l,list):
        return list(map(lambda x: x[1:],l))


def isaccepteble_yaml (patternfile: str, verifiedfile: str) -> bool:
    """
    Checking whether the YAML-parameters in the pattern file are equal to YAML-parameters in the verified file.
    Additional keys in the verified file are ignored.
    Sensitive to the order of arguments.
    """
    #try:
    pattern       = yaml_to_dict(patternfile)
    verified      = yaml_to_dict(verifiedfile)
    return isaccepteble(pattern, verified)
    #except:
    #     print("isaccepteble_yaml: Verify error")

def isaccepteble (pattern: dict, verified: dict) -> bool:
    if isinstance(pattern, dict) and isinstance(verified, dict):
        flat_pattern  = drop_lead_ch(none_filter(concat_list(flat_keys("",pattern))))
        founded_keys  = list(map(
                            lambda x: (x,concat_list(find_absolute(verified,x)))
                                ,flat_pattern))
        expected_keys = list(map(
                            lambda x: (x,concat_list(find_absolute(pattern,x)))
                                ,flat_pattern))
        #not_founded_keys = list(filter(lambda x: len(x[1])==0,founded_keys))
        return founded_keys==expected_keys
    else: return False

            

def main():
    return ("Insert your code there") 
    #content = yaml_to_dict("pod.yaml")
    #found = find_all_keys(content,"ports")
    #print(found)
    #found = find_all_keys(content,"stage")
    #print(found)
    #found = find_all_keys(content,"namespace")
    #print(found)
    #found = concat_list(find_absolute(content,"spec.containers.ports"))
    #print(found)
    #print(found)
    #found = concat_list(find_absolute(content,"metadata.name"))
    #print(found)
    #found = concat_list(find_absolute(content,"metadata.name.stage"))
    #print(found)



if __name__ == "__main__":
    main()
