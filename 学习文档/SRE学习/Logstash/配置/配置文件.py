'''

    1. logstash分为2种配置文件
        1.1 logstash服务配置文件，主要配置pipline、工作线程、之类
        1.2 插件配置文件，主要定制插排，用于读取日志文件 input、filter、output
'''

# 插件配置文件
'''
# 配置格式

input {
        // 输入插件
}

filter {
        // 过滤插件
}

output {
        // 输出插件
}

'''

'''
# 配置样例
# 从标准输入输出至标准输出
input {
    stdin {}
}
output {
    stdout{}
}
'''

'''
# 配置文件使用环境变量

export TYPE=json
input {
    stdin {
        codec => %{TYPE}
    }

}
'''
