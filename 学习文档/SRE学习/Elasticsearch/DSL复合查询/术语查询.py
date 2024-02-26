'''


    # 存在查询
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/my-index-000002/_search?pretty -d '{

        "query": {
            # 存在方法
            "exists": {
                # 过滤字段abc是否存在，如果存在将返回所有匹配文档
                "field": "abc"
            }
        }
    }'

    # 模糊查询
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/my-index-000002/_search?pretty -d '{

        "query": {
            "fuzzy": {
                "name": {
                    "value": "y"
                }
            }

        }
    }'
    # 根据_id返回查询文档
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/my-index-000002/_search?pretty -d '{
        "query": {
            "ids": {
                "values": ["1","2","3","4","5"]
            }
        }
    }'

    # 根据行首查询
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/my-index-000002/_search?pretty -d '
    {
        "query": {
                # 行首查询
                "prefix": {
                    # 对应的field
                    "name": {
                        # 对应的前缀
                        "value": "y"
                    }
                }
        }
    }'

    # 范围查询
    # range
    # lt 小于
    # gt 大于
    # lte 小于等于
    # gte 大于等于

   curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/my-index-000002/_search?pretty -d '{
    "query": {

        "range": {

            "age": {
                "gte": 0

            }

        }
    }

   }'
'''


