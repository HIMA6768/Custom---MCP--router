
from typing import List , Any
from fastapi import FastAPI, Response,status
from pydantic import BaseModel
from execution import  selectchunk,execute
import json

filepath=r"C:\Users\HIMADRI\Desktop\mas evaluation system\environment\config.json"
with open(filepath,"r")as f:
        document=json.load(f)
print(document)


app= FastAPI()
class tooldetails(BaseModel):
    name:str

class finalcalc(BaseModel):
    chunk:dict
    inputs:List[Any]

@app.get("/logfile")
async def sendlogfile():
    return document

@app.post("/toolname")
async def toolname(n:tooldetails):
    chunk=selectchunk(n.name,document)
    print(f"chunk =  {chunk}")
    if "error" in chunk.keys():
        return chunk["error"]
    else:
        args=chunk["arguments"]
        doc={"chunk":chunk}
        input=[]
        for i in range(len(args)):
            input.append(type(args[i]).__name__)
        doc["inputs"]=input
        return doc

@app.post("/executetool")
async def executetool(e:finalcalc):
    result=execute(e.chunk,*e.inputs)
    return result



