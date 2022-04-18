import yaml
import typing

def d_crawler_abs_path(yamld, path_list) :
    """
    absolute path is the location of the key in the yaml section
    e.g spec.template.metadata.labels.app
    """
    # = abs_target_path.split(",")
    #if len() > 1
    if isinstance(yamld, list):
        return list(map(lambda x: d_crawler_abs_path(x, path_list),yamld))
    nested_list=[]
    #print(yamld, , "sdf")
    if len(path_list) == 0:
        #print(yamld,"answer")
        return yamld
    head = path_list[0]
    tail = path_list[1:]
    if isinstance(yamld, dict):
        if head in yamld.keys(): 
            #print(yamld[[0]], "ddd")
            #if isinstance(yamld[head], list):
            #    nested_list = list(map(lambda x: d_crawler_abs_path(x, tail),yamld[head]))
                #print(nested_list, "LIST")
            #else:
            return d_crawler_abs_path(yamld[head],tail)
    #return nested_list




def yaml_to_dict (filename: str) -> dict:
    with open(filename) as f:
        content = yaml.safe_load(f)
    return content

def d_crawler(yamld: dict, target: str) -> list:
    found=[]
    for (k,v) in yamld.items():
        if k == target:
            found += [{k:v}]
        if isinstance(v, dict):
            found += d_crawler(v, target)
        if isinstance(v, list):
            for i in v:
                if isinstance(i,dict):
                    found += d_crawler(i, target)
    return found
    #return filterl(found)


def filterl(l):
    if len(l) == 0:
        return []
    if isinstance(l[0],list):
        return list(filterl(l[0])) + filterl(l[1:])
    if l[0] is None:
        return filterl(l[1:])
    else:
        return [l[0]] + filterl(l[1:])
            

def main():
    content = yaml_to_dict("pod.yaml")
    found = filterl(d_crawler_abs_path(content,["spec","containers","ports", "stage"]))
    print(found)
    return found



if __name__ == "__main__":
    main()
