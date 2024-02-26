'''
    grok 是logstash 用于结构化解析的匹配工具，基于正则表达式 来匹配非结构化数据

    # 结构化正则定义
    # 192.168.0.1
    （?<IP_ADDRESS>: [0-9]{1,3}\S[0-9]{1,3}\S[0-9]{1,3}\S[0-9]{1,3}）
    %{IP: IP_ADDRESS}






'''
# Grok 过滤器配置选项
'''
    break_on_match：配合if 判断使用，如果break_on_match => true 那么后面的匹配将不会执行
    keep_empty_captures: 当match匹配时如果匹配空字段处理方式，默认是不展示不保留，true表示保留
        {
            # 保留空字段
            "keep_empty_captures" => "true"
            match => {
                "message" => "STATUS=(?<status>.*)"
            }
        }

    match:  匹配字符串
        filter {
              grok {
                # 当message 中 可以通过pattern %{NUMBER} 匹配后，将设置duration=%{NUMBER}
                match => {
                  "message" => "Duration: %{NUMBER:duration}"   //单一匹配
                  "message" => [..]     // 数组方式匹配多个字段
                }
              }
        }

    named_captures_only: 只捕获命名过的分组匹配,默认false，如果强制依赖必须命名此参数很有效
        captures(捕获)方式：
            1. 在match过程中有命名过的 %{pattern:<named>}
                %{IP:ip} or (?<ip>\d{0,3})
            2. 通过位置索引匹配，这个叫未命名分组
                (%{ip}) or (\d+)
        filter {

            grok {
                named_captures_only => "true"
                match => {
                    "message" => "
                        STATUS=(?<status>\d{3}) IP=(\d{3})
                    "
                }
            }   // 只会匹配STATUS=123 IP=匹配分组为空将不会显示
        }


        pattern_definitions:   类似es中的模板，主要定义了一堆pattern匹配方式，如果存在多个grok可以共同使用一个
            # 使用方式
            filter {

                grok {
                        pattern_definitions => {
                                "my-text-pattern" =>  "A: (?<a>\d), Status: (?<b>\d)"
                        }

                        match => {
                            "message" => "%{my-text-pattern}"
                        }
                }
            }
        pattern_dir:    用于引用自定义的pattern（模式）

        tag_on_failure:   用于定义模式匹配不上的字段，如果存在那么会增加一个tag数组形式
            # 使用案例
            filter {
                grok {
                    match => {
                        "message" => "A: (?<a>\d), Status: (?<b>\d)"
                    }
                    tag_on_failure => ["grok_pattern_fail"]
                }
            }
        tag_on_timeout:   grok 匹配超时的模式字段将会记录下来
            # 使用案例
            filter {
                grok {
                    match => {
                        "message" => "A: (?<a>\d), Status: (?<b>\d)"
                    }
                    tag_on_timeout => ["grok_pattern_timeout"]
                }
            }
        target: 用于将匹配的字段写入到一个全新的字段中，类似与json嵌套(多层字段)
            # 使用案例
            filter {
                grok {
                    match => {
                        "message" => "A: (?<a>\d), Status: (?<b>\d)"
                    }
                    target => "new_dict_target"
                }

            }
        timeout_millis:  用于定义多模式下 正则处理超时时间 设置为0表示永不超时
        
'''