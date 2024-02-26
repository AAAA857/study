'''

    alisa(别名)：
        1. 是一组数据量或单一索引的别名
        2. 程序调用alisa可以实现无缝重建

    组成类型:
        1. 多条index
        2. 单挑index

'''

'''
创建一条别名index
    1. 前提被别名的index应该提前存在
    
# 查看alias
curl -H 'Content-Type: application/json' http://127.0.0.1:9200/_aliases

# 添加alias
curl -H 'Content-Type: application/json' -X POST http://127.0.0.1:9200/_aliases -d '
{
        "actions": [
            {
                "add": {
                    "index": "my-index-000002",
                    "alias": "logs"
                }
            }
        
        ]
}

# 删除alias
curl -H 'Content-Type: application/json' -X POST http://127.0.0.1:9200 -d '
{
    "actions": [
    
        {
            "remove": {
            
                    "index": my-index-000002,
                    "alias": logs
                }
        }
    
    ]
}

# 修改
# 先删除在新增
curl -XPOST -H 'Content-Type: application/json' http://127.0.0.1:9200 -d '
{
    "actions": [
        {
            "remove": {
                "index": "my-index-000002",
                "alias": "logs"
            }
        },
        {
            "add": {
                "index": "my-index-000003",
                "alias": "logs"
            }
        }
    ]
}
'

'


'
'''