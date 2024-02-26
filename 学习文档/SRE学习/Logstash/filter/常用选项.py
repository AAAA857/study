'''
    常用选项：
        1. 适用与所有filter插件，通用配置


    # 方法
    add_field:          用于新增字段
        # 使用方式
            filter {
                grok {

                     if [path] =~ "/root/logstash-tutorial-dataset" {

                            mutate {
                                    add_field => {"service" => "apache" }
                            }
                    }else {
                            mutate {
                                    add_field => {"service" => "ohter"}
                            }

                    }
                }
            }


    remove_field:       用于删除字段
       # 使用方式
            filter {
                grok {

                     if [path] =~ "/root/logstash-tutorial-dataset" {

                            mutate {
                                    remove_field => {"service" => "apache" }
                            }
                    }else {
                            mutate {
                                    remove_field => {"service" => "ohter"}
                            }
                    }
                }
            }

    id: 用于添加一个id字段，这个对多grok处理很有用，主要用于区分。可以在config中指定

    periodic_flush： 如果为true，那么output插件将会根据flush_interval时间做数据刷新，就是将数据发送过去
        # 默认为false
        # flush_interval 默认为1s
    remove_tag： 用于删除标签。
        注意：标签跟field（字段）不是同一个概念
            1. tag 用于区分元数据。比如匹配失败会
            2. field 是一个日志字段，结构化处理后对应的每个日志字段 被称之为field
        
'''