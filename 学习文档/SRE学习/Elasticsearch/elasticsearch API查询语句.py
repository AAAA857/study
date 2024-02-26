'''

    Elasticsearch API DSL分为两大类匹配模式：
        1. query  相关度匹配 full-text 基于相关度，查询复杂 不会被缓存
        2. filter 精确值查询 true or false 结果 ， 查询速度快 可缓存









语法格式：
    -XGET 'IP:PORT/index/_doc/_search?pretty' -d ‘

        {
            "query": {

                "option": {

                    values
                }

            }

        }

        ’
'''

'''
option:
    1. 精确值匹配
        math
        math_all
            
    2. 模糊匹配
        range 做数值或时间范围匹配
        trem  做关键字模糊匹配
        trems 做多关键字模糊匹配
        exists 做值是否为空匹配
        fuzzy  做模糊匹配
        ids    根据_id 返回文档
        prefix  根据前缀做匹配     

    3. 复合查询
        multi_match:    查询内容来着多个域中(key)
            
            {
                "query": {
                    "multi_match": {
                        "query": "查询内容",
                        "field": "查询字段"
                    }
                }
            }
'''


'''
    1、创建index
    curl -XPUT http://localhost:9200/my_index/_doc/1 -d '
    
        {
            "id": 1
            "name": "abc",
            "age": 18
        
        }
    '

'''