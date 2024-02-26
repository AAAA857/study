import json
import pickle
import shelve
'''
    1. json             通用字符串序列反序列方式，适用于任何语言
    2. pickle           仅限python内使用的序列化方式，方法与json 一致，可以传入的方式比json多,字节模式
    2. shelve           仅支持一个open方式，内部封装pickle方式处理,写入以字节的方式
'''

Dict = {

    "id": 1,
    "name": "ytc",
    "age": 18,
    "work": "code"

}
'''
# 方式一  dumps,loads
# 将dict 写入本地磁盘
# 序列化
res = json.dumps(Dict)
print(res)

with open(file="./json.txt",mode='w',encoding='utf-8') as w:
    w.write(res)

# 反序列化
# 读取dict
with open(file='./json.txt',mode='r',encoding='utf-8') as  r:

    res = r.read()
    print(res,type(res))
    res = json.loads(res)
    print(res.get('name'))
'''


'''
# 方式二 dump，load

# dump 适用与在写入文件场景

with open(file='json.txt',mode='w',encoding='utf-8') as w:

    # 接受2个对象 一个是写入数据，一个是文件句柄
    json.dump(Dict,w)

# load 同理dump 不需要read()方法
with open(file='json.txt',mode='r') as r:
    res = json.load(r)
    print(res,type(res))
'''

'''
# pickle
with open(file='./json.txt',mode='wb') as w:
    # data = pickle.dumps(Dict)
    # print(data)
    # w.write(data)
    pickle.dump(Dict,w)

with open(file='./json.txt',mode='rb') as  r:
    # data = r.read()
    # res = pickle.loads(data)
    # print(res.get('age'))
    data = pickle.load(r)
    print(data.get('age'))
'''
