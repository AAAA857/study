'''
    前置条件:
        1. java 环境
        2. logstash 部署文件

    # 下载地址
    https://www.elastic.co/guide/en/logstash/current/installing-logstash.html
'''
'''
    
    # 解压logstash
    tar -axvf logstash-7.17.8.tar.gz
    
    # 启动测试
    ./bin/logstash -e 'input{stdin{}}output{stdout{}}'
    
'''
'''
    # 读取文件
    vim config/file.yml
        
    input {
           # file 插件 
            file {
                    # 通用配置
                    # 添加字段
                    add_field => { "add_field" => "a" }
                    # 编码器
                    codec => "json"
                    # id 当多个file 插件时用于区分、展示
                    id => "file-id-0"
                    
                        
                    # 开启压缩文件校验
                    # 默认false 如果为true 会执行2次校验：
                    #  1. 校验压缩包是否被破坏
                    #  2. 校验日志文件是否被破坏
                    #  3. 开启会需要更多的时间去处理消化性能，同样可以带来安全性
                    #check_archive_validity => "true"
                    
                    # 文件换行符
                    # 如果读取的压缩文件不能使用此配置
                    #delimiter => "\n"
                    
                    # 新文件发现时间
                    # 默认15s
                    discover_interval => "15"                
                    
                    # 排除某些文件
                    # 支持正则表达式
                    #exclude => "exclude.log"
                    
                    file_completed_action => "log"
                    file_completed_log_path => "/tmp/back.log"
    
                    # 文件读取路径
                    # 可以是列表 读取多个文件
                    path => "/root/logstash-tutorial-dataset"
                    # 默认读取文件行尾，start_position => "end"模式
                    # 配置文件开始读取位置为行首
                    start_position => "beginning"
            }
    }
    output {
    
            stdout {}
    }


'''