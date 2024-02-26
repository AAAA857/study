
'''
   布尔查询是最常用的组合查询，不仅将多个查询条件组合在一起，
   并且将查询的结果和结果的评分组合在一起。当查询条件是多个表达式的组合时，
   布尔查询非常有用，实际上，布尔查询把多个子查询组合（combine）成一个布尔表达式，
   所有子查询之间的逻辑关系是与（and）；只有当一个文档满足布尔查询中的所有子查询条件时，
   ElasticSearch引擎才认为该文档满足查询条件。布尔查询支持的子查询类型共有四种，
   分别是：
    1.must：必须匹配，返回score评分
    2.should: 文档应该出现一个或多个匹配
    3.must_not 文档不应该出现匹配查询
    4.filter： 文档必须匹配，没有score评分
'''


'''
    # must
    # 必须匹配查询 会根据评分返回
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200 -d '
    {
        "query": {
            "bool": {
                "must": {
                    "term": {
                        "name": "ytc"
                    }

                }

            }

        }
    }
    '
    # filter
    # 必须匹配查询 没有score评分，尝试缓存下来
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200 -d '
    {
        "query": {
            "bool": {
                "filter": {
                    "term": {
                        "age": 18
                    }
                }
            }
        }
    }
    '
    # must_not
    # 不得出现取反
        curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/my-index-000002/_search?pretty -d '
        {
            "query": {
                "bool": {
                    # 上文
                    "must_not": {
                        "term": {
                            "age": 18
                        }
                    },
                    # 下文
                    "filter": {
                        "term": {
                            "name": "ytc"
                        }
                    }
                }
            }
            }
        '
        # should 文档应该匹配的内容或关系
        curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/my-index-000002/_search?pretty -d '
        {
            "query": {
                "bool": {
                    "should": [
                       {"term": {
                        "name": "ytc1"
                       }},
                        {"term": {
                        "name": "abc"
                        }}
                    ]
                }
            }
        }
        '
'''