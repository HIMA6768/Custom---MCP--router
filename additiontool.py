from decorators import trace_tool, writelogs,toolregistry

@trace_tool
def add(a,b):
    """ this is  an arithmetic addition tool"""
    return a+b

# @trace_tool
# def minus(a,b):
#     """ this is a substraction tool"""
#     return a-b


if __name__=="__main__":
    filename="config"
    print(add(3,2))
    writelogs(toolregistry,filename)
    # print(minus(4,2))
    # writelogs(toolregistry,filename)
    





