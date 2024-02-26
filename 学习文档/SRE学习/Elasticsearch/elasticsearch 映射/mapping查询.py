'''
# 查看index mapping

-XGET /my-index-000001/_mapping
-XGET /my-index-000001/_mapping?pretty


# 查看某个field字段索引mapping
-XGET /my-index-000001/_mapping/field/<field 名称>
'''


'''
# 开启关闭index的dynamic mapping 功能

    # 支持的参数
        1. dynamic: true        默认开启
        2. dynamic: false       如果是显示mapping配置当遇见未知的field时不报错 不添加mapping，但是数据可以插入
        3. dynamic: strict      如果是显示mapping配置将严格按照mapping设置遇见未知的field时将会抛出异常

    curl -XPUT http://127.0.0.1:9200/my-index/_mappings -d '{
            
            "dynamic": "strict"
    
    }'

'''


