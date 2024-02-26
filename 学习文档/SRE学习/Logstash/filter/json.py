'''
    filter 过滤器 子模块json ，主要用于解析json类型数据，非结构数据中存在多种类型，当input
插件接收的数据包含json类型那么可以使用json 插件做数据处理。

'''

'''使用事例'''
'''
# 本地日志
/var/log/text.log
{
"message": "abc",
json_data: '{
    "user": "abc",
    "age": 18,
    "city": "New York"
}'
}

# logstash 配置文件
vim config/filter-json.yaml
input {
    file => "/var/log/text.log"
    start_position => "beginning"
}
filter {
    # 将解析input 插件中输入的 json_data字段并且新增一个tag
    json {
        source => "json_data"
        mutate => {
            add_field => {"key"=> "123"}
        }
    }
}
output {
    stdout {}
}
'''