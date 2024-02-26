# index数据迁移
'''
    1.在已经存在的mapping类型无法进行修改，会导致数据错乱丢失
    2.如果需要修改原有的mapping 则需要重新建立新的mapping后做数据迁移
    # 使用方法
    POST /_reindex

    # 查询参数
    max_docs：（可选，整数）要处理的最大文档数。默认为所有文档。
    wait_for_completion: （可选，布尔值）如果true，则请求将阻塞，直到操作完成。默认为true



    # 参数 Request body
    source: 源index
        index: 必选
        _source: 可选  迁移某个字段
        remote: 远端es server
            host:  IP
            username: 如果开启认证的话需要的用户名密码
            password: 如果开启认证的话需要的密码
            socket_timeout: 连接socket超时时间默认30s
            connect_timeout: 连接超时时间30s
            headers:    请求首部信息
        size: 每次迁移的doc文档数，当使用remote时使用默认值为100M
        slice:  切片信息
            id: 手动切片的id
            max: 切片总数

    dest:   目标index
        index: 必选


    # 重建mapping 做数据迁移
    # 在迁移index 时不能保存source index setting配置等信息，需要提前创建好mapping或template
    # 方式一
    # 迁移index内所有doc
    curl  -H 'Content-Type: application/json'
        -X POST  http://127.0.0.1:9200/_reindex
        -d '{
        "source":{
            "index": "my-index-000002"
            },
        "dest":{
            "index": "re_my-index-000003"
            }
        }'
    # 方式二
    # 迁移远端es集群，部分数据
   curl  -H 'Content-Type: application/json'
        -X POST  http://127.0.0.1:9200/_reindex
        -d
        '{
          "source": {

            "remote": {
              "host": "http://otherhost:9200",
              "username": "user",
              "password": "pass"
            },
            "index": "my-index-000001",
            "query": {
              "match": {
                "test": "data"
              }
            }
          },
          "dest": {
            "index": "my-new-index-000001"
          }
        }'

    # 方式三 通过查询来迁移index内数据
    # 将source = source_index_01 index内 name=”alex“的doc 迁移到dest_index_01内部
    POST /_reindex -d '{

        "source": {
            "index": "source_index_01",
            "query": {
                "term": {
                    "name": "alex"
                }
            }
        },
        "dest": {

            "index": "dest_index_01"
        }

    }'

    # 方式四 迁移index 只迁移1条doc文档，默认迁移是迁移所有

    -XPOST http://127.0.0.1:9200/_reindex -d '{
       "max_docs": 1 ,
       "source": {
         "index": "my-index-000002"
         },
       "dest": {
          "index":"my-index-000005"
         }
    }'

    # 方式五   将多个index 源数据合并迁移到一个目标index中

    -X POST http://127.0.0.1:9200/_reindex -d '{

        "source": {

            "index": ["my-index-000001","my-index-000003"]
        },
        "dest": {

            "index": "dest-my-index-000006"

        }

    }'

    # 方式六   将source index 中 name ,age 两个field 字段做迁移
    -X POST /_reindex -d '{

        "source": {

            "index": "mysql-index-000001",
            "_source": ["name","age"]
        },
        "dest": {
            "index": "dest-mysql-00001"
        }
    }'

    # 方式七 迁移索引同时修改新index内的field 名称
    # ctx._source.tag 新
    # ctx._source.remove(\"flag\") 移除 flag
    POST /_reindex
        {
          "source": {
            "index": "my-index-000001"
          },
          "dest": {
            "index": "my-new-index-000001"
          },
          "script": {
            "source": "ctx._source.tag = ctx._source.remove(\"flag\")"
          }
        }
'''