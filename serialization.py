import __builtin__ 

def serializableDict(obj):
    res = []
    res.append("dict")
    counter = 0
    for k,v in obj.items():
        counter += 1
        res.append(serializable(k))
        res.append(serializable(v))
    return res

def serializable(obj):
    res = []
    if isinstance(obj, int):
        res.append("int")
        res.append(str(obj))
    elif isinstance(obj, str):
        resstr = obj.replace('\n', '\\n')
        res.append("str")
        res.append(resstr)
    elif isinstance(obj, float):
        res.append("float")
        res.append(str(obj))
    elif obj.__class__ == dict:
        res = serializableDict(obj)
    elif isinstance(obj, tuple):
        res.append("tuple")
        res.extend(map(serializable, obj))
    elif obj is None:
        res.append("None") 
        res.append("None")
    elif (type(obj) not in __builtin__.__dict__.values()):
        res.append("userType")
        res.append(obj.__class__.__module__)
        res.append(obj.__class__.__name__)
        res.append(serializable(obj.__dict__))
    res = "\n".join(res)
    return "%d\n%s" % (len(res), res)
    
def deserializable(data):
    res = {}
    length, typeRes, data = data.split('\n', 2)
    if typeRes == "int":
        res = int (data)
    elif typeRes =="str":
        res = (str (data)).replace('\\n','\n')
    elif typeRes =="float":
        res = float (data)
    elif typeRes =="None":
        res = None
    elif typeRes =="dict":
       res = {}
       lengthdict = len("dict")
       
       while (lengthdict < int(length)):
           lengthKey = int (data.split('\n', 1)[0])
           
           lengthKey += len(data.split('\n', 1)[0]) + 1
           key = deserializable(data[:lengthKey])
           
           lengthdict += lengthKey + 1
           data = data[lengthKey+1:]
           
           lengthEl = int (data.split('\n', 1)[0])
           
           lengthEl += len(data.split('\n', 1)[0]) + 1
           element = deserializable(data[:lengthEl])
           
           lengthdict += lengthEl + 1
           data = data[lengthEl+1:]
           
           res[key] = element
           
    elif typeRes =="tuple":
        res = ()
        lengthtuple = len("tuple")
        
        while (lengthtuple < int(length)):
            lengthEl = int (data.split('\n', 1)[0])
           
            lengthEl += len(data.split('\n', 1)[0]) + 1
            element = deserializable(data[:lengthEl])
           
            lengthtuple += lengthEl + 1
            data = data[lengthEl+1:]
            res += (element,)
    elif typeRes == "userType":
        module, className, userTypecount, data = data.split('\n', 3)
        classDict = deserializarybufble(data[:int(userTypecount)])
        print module, className, data 
        x = getattr(__import__(module), className)()
        x.__dict__ = classDict
        res = x
    return res

if __name__ == '__main__':
    pass