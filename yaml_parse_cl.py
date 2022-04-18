import yaml
import typing

def d_crawler_abs_path(yamld, path_list) :
    """
    absolute path is the location of the key in the yaml file 
    e.g spec.template.metadata.labels.app
    """
    if isinstance(yamld, list):
        return list(map(lambda x: d_crawler_abs_path(x, path_list),yamld))
    if len(path_list) == 0:
        return yamld
    #for 3.x python
    #head, *tail = path_list
    head, tail = path_list[0], path_list[1:]
    if isinstance(yamld, dict):
        if head in yamld.keys(): 
            return d_crawler_abs_path(yamld[head],tail)


def yaml_to_dict (filename):
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


def filterl(l):
    if isinstance(l,str):
        return l
    if l is None or len(l) == 0:
        return []
    if isinstance(l[0],list):
        return list(filterl(l[0])) + filterl(l[1:])
    if l[0] is None:
        return filterl(l[1:])
    else:
        return [l[0]] + filterl(l[1:])
            

def main():
    content = yaml_to_dict("pod.yaml")
    found = d_crawler(content,"ports")
    print(found)
    found = d_crawler(content,"stage")
    print(found)
    found = d_crawler(content,"namespace")
    print(found)
    found = filterl(d_crawler_abs_path(content,["spec","containers","ports"]))
    print(found)
    found = filterl(d_crawler_abs_path(content,["metadata","name"]))
    print(found)
    found = filterl(d_crawler_abs_path(content,["metadata","name","stage"]))
    print(found)
    return found



if __name__ == "__main__":
    main()
