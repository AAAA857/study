'''

    filter 过滤器中子插件 drop, 其主要作用在过滤删除某匹配字段

'''

'''
# 使用方式
input {
    file {
    
        path => "info.log"
    
    }

}
filter {
        if [message] == "abc" {
            drop{
                # 使用此选项将按照百分比去删除
                percentage  => 40
            }
        }
}
output {
    stdout {
    
    }
}


'''