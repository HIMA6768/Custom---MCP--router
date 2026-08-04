import inspect
import os
import json
from ntpath import exists
toolregistry=[]
def trace_tool(fx):
    path = inspect.getfile(fx)
    path = os.path.dirname(path)
    
    def newfunc(*args, **kwargs):
        print("tracing function running")
        if not fx.__doc__ :
            raise ValueError("!!! ERROR !!!\n no description please add description to this function") 
        print(args,kwargs)
        ag = []
        c=0
        for va in args:
            ag.append(va)
            
        v = fx(*args, **kwargs)
        
        filename = str(fx.__code__.co_filename).split(os.sep)
        filename = filename[len(filename) - 1]
        
        doc = {
            "name": fx.__name__,
            "description": fx.__doc__ or "",
            "module": filename,
            "path": path,
            "arguments": ag
        }
        print(doc)
        toolregistry.append(doc)
        return v
        
    return newfunc




def writelogs(log,name):
    p=str(log[0]["path"])
    filepath = os.path.join(p, f"{name}.json")
    print(filepath)
    if not exists(filepath):
        with open(filepath,"a+")as f:
            json.dump(log,f,indent=4)
    else:
        with open(filepath,"r")as f:
            data=json.load(f)
        for l in log:
            data.append(l)
        with open(filepath,"w")as f:
            json.dump(data,f,indent=4)
            
            




    

    

