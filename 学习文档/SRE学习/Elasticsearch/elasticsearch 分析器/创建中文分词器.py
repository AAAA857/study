'''
    elasticsearch 之所以支持模糊全文查询，一是因为使用全文倒排索引，倒排
    索引的核心就是词语进行分词，根据分词结果做全文检索。

    分析器是一组控制整个过程的规则

    mapping类型:
        1. text 文本类型
        2. keyword  非结构类型
        3. long 长整数类型
        4. integer  长整数类型




    Text Analysis:
        1. Tokenization: 将text 文本拆分更小的快称为标记
           案例：
                “the quick brown fox jumps” 如果改词语做为一个完整词语，当用户输入 fox jumps是检索不到的
                但是将文本做了标记拆分则可以检索到该文本。
        2. Normalization： 将标化后的分词做标准化的转换称之为正规化
            案例:
                文本: “the quick brown fox jumps”
                标记后: ["the","quick","brown","fox","jumps"]

                用户检索:
                    The != the  在不做正规化之前是不可以匹配到的
                正规化包括将字符都转换为小写

    分词器类型:
        1.standard analyzer： 默认es使用标准分词器，基于unicod分词算法实现
        # 创建index 设置analyzer
        curl -XPUT -H 'Content-Type: application/json' http://127.0.0.1:9200/my_index -d '{

            "settings": {
                "analysis": {
                    "my_analyzer_standar": {

                        "type": "standar",
                        "max_token_length": 10,
                        "stopwords": "_english_"
                    }

                }
            }
        }'
        # 插入数据
        curl -XPUT -H 'Content-Type: application/json' http://127.0.0.1:9200/my_index/_doc/1 -d '{

            "name": "ytc",
            "age": 18,
            "text": "My Test Analyzer Index"

        }'
        # 查看analyzer 分词结果
        curl -XPOST -H 'Content-Type: application/json' http://127.0.0.1:9200/my_index/_analyzer -d '{

            "field": "text",
            "text": "my test analyzer index"-H 'Content-Type: application/json' http://127.0.0.1:9200/my_index/_
        }'

        # 全文检索词
        curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/my_index/_search?pretty -d '

            {
                "query": {
                    "match": {
                        "text": "test"
                    }
                }
            }
        '
'''


# dynamic mapping fielad
# field 动态匹配 进行分配数据类型
'''
curl -H 'Content-Type: application/json' -XPUT http://127.0.0.1:9200/my-index-000003 -d '
{
  "mappings": {
    # mapping 使用动态模板
    "dynamic_templates": [
      {
        # 自定义名称
        "strings_as_the": {
          # 匹配类型 不能包含text类型
          # 可用 [object, string, long, double, boolean, date, binary]
          "match_mapping_type": "string",
          # 匹配field 如果不写此选项那么只要是string类型都匹配
          "match": "age*",
          # 当匹配后将其修改成什么类型
          # runtime 就是运行时 、创建过程中替换
          # 当runtime为空时，默认使用long、float类型
          "runtime": {
            # age 字段的都将会转换为ip 类型
            "type": "ip"
          }
        }
      }
    ]
  }
}
'
'''
# 显示mapping 俗称自定义mapping
# 好处就是不需要es 根据分析来自己规划类型，需要人为指定
# 在es 6.0 之后没有string类型 变更为text 类型
'''
curl -X PUT  -H 'Content-Type: application/json' -XPUT  http://127.0.0.1:9200/my-index-000003 -d '
{
        "mappings": {
                # properties 下面对应的配置均是field 名称与类型
                "properties": {
                        "name": {
                                "type": "text"
                        },
                        "age": {
                                "type": "long"
                        },
                        "text": {
                                "type": "text"
                        }
                        }
        }
}
'
'''

# mapping 插入新field
'''
curl -X PUT -H 'Content-Type: application/json' -XPUT http://127.0.0.1:9200/my-index-000003/_mappings -d 
 '{
        "properties":{
            "email-id": {
                "type": "keyword",
                "index":false
                }
            }
    }'

'''

