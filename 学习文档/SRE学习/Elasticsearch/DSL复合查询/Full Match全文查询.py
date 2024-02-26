'''
    1.全文查询能够搜索能够分析的text字段
'''

'''
    # match匹配
    
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/my-index-000002/_search?pretty -d '
    {
        "query": {
            "match": {
                # 匹配发field字段
                "name": {
                    # query 后面对应的是查询内容
                    "query": "ytc",
                    # 模糊匹配
                     "fuzziness" : "AUTO"
                }
            }
        }
    }
    '
    
    # 前缀匹配
    # match_bool_prefix：按单词前缀匹配
    # match_phrase_prefix: 按短语前缀匹配
    # match_bool_prefix
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/my-index-000002/_search?pretty -d '
    {
        "query": {
            # 使用前缀匹配方法
            "match_bool_prefix": {
                    # 匹配field 字段为 name ，匹配的前缀为ytc
                    "name": "ytc"
            }
        }
    }
    '
    # 短语前缀匹配
    # 下面匹配结果
    # ytc1 ytc23ssssss 可以匹配
    # y is jb t kmc 不可以匹配
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/my-index-000002/_search?pretty -d '
    {
        "query": {

            "match_phrase_prefix": {
                    "name": "ytc"
            }
        }
    }
    '
    # 短语查询
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/my-index-000002/_search?pretty -d '
    {
        "query": {
            "match_phrase": {
                "name": "ytc"
            }
        }
        
    }
    '
    # 多字段匹配
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/my-index-000002/_search?pretty -d '{
        "query": {
            # 多字段匹配方法
            "combined_fields": {
                # 匹配的内容模糊匹配
                "query": "ytc",
                # 需要匹配的fields数组
                # 仅支持text类型
                "fields": [ "name","mes" ],
                "operator": "and"
            }
        }
    }'
    
    # 多字段匹配
    # multi_match
    # 与combined_fields 区别在于可以支持文本和非文本字段类型,根据query 输入类型判断，不可以 整数和string混合使用
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/my-index-000002/_search?pretty -d '{
        "query": {
            "multi_match": {
                "query": "ytc",
                # fields 支持使用*模糊匹配
                "fields": ["name","mes","*-age"]
            }
        }
    }'
    
'''