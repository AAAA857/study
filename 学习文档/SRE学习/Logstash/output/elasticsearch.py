'''
    1。logstash将数据输入到elasticsearch中做存储
    2. kibana展示时需要使用elasticsearch做数据分析
'''
# 插件常用方法
'''

    host => 对应ES主机，支持传入字符串或列表，如果是列表，那边logstash将会轮询调用
        "IP" , "IP:9200" , "["ip1","ip2","ip3"]"
    index => 对应写入ES中的索引名称，建议使用变量方式生成基于时间切割方式
    action => 对应工作模式默认为index 
        index： 将文档写入到索引中
        update: 更新对应index _id数据
        delete: 删除对应index _id数据
    document_id => 写入index后生成的_id 号，默认不指定将根据自带算法生成随机字符串
    manage_template => 使用ES中template功能，如果为True 将有logstash 自动管理
    template_name => 使用ES中template功能，模板有用户自定义
    template_overwrite => 模板如果存在 那么将被覆盖

'''

# 配置样例
'''
input {
        udp{
                port => 25826
                buffer_size => 1452
                workers => 3          # Default is 2
                queue_size => 30000   # Default is 2000
                codec => collectd { }
                type => "collectd"
                add_field => {"log_type" => "offline"}
        }
}

filter {
                if [log_type] == "offline" {
                        mutate {
                                add_field => {  "[@metadata][target_index]" => "test-%{+YYYY.MM.dd}"}
                        }
                } else {
                        mutate {
                                add_field => { "[@metadata][target_index]" => "prod-%{+YYYY.MM.dd}"}
                        }
                }      
}


output {
       elasticsearch {
                index => "%{[@metadata][target_index]}"
                hosts => "10.180.0.41:9200"
        }
}
'''