from importlib import import_module
from posixpath import exists
import sys
import json




def execute(d,*inputs):
    val=d
    inputs=list(inputs)
    funcname=val["name"]
    modulepath=val["path"]
    modulename=val["module"].split(".")[0]
    args=val["arguments"]
    try:
     for i in range(len(inputs)):
        inputs[i]=type(args[i])(inputs[i])
    except :
        return {"error":"invalid input error"}

 
    if modulepath not in sys.path:
        sys.path.append(modulepath)
    module= import_module(modulename)
    funcname=getattr(module,funcname)
    
    result= funcname(*inputs)
    return result



def selectchunk(name:str,doc):
    if len(doc)>0:
        for d in doc:
            if name.lower().strip() == d["name"].lower().strip():
                return d
                
        else:
            return {"error": "function not found"}
    else:
        return {"error": "file is empty !!"}


def runtool(name:str,inputs:str,document):
    chunk=selectchunk(name,document)
    print(chunk)
    if "error" in chunk.keys() :
        return chunk["error"]
    else:
        args=chunk["arguments"]
        print(args,len(args))
        inputs=inputs.split(",")
        print(inputs)
        if len(inputs)==len(args):
            for i in range(len(args)):
                inputs[i]=type(args[i])(inputs[i])
        else:
            return {"error":f"invalid input ex- {args}"}
        result=execute(chunk,*inputs)
        return result

if __name__=="__main__":
    name="add"
    inputs="5,2"

    filepath=r"C:\Users\HIMADRI\Desktop\mas evaluation system\environment\config.json"
    with open(filepath,"r")as f:
        doc=json.load(f)
    print(doc)

    result=runtool(name,inputs,doc)
    print(result)






