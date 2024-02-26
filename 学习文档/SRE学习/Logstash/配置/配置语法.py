'''
    logstash 配置文件基于ruby写法

    数据类型:
        1. 字符串
            type => "string"
        2. 数字
            type => 123
        3. 数组
            type => ["1","2","3","4"]
        4. 哈希
            type => {
                "key" => "value",
                "key" => "value"
            }


    字段提取：
        "{
            type => "string",
            name => "ytc",
        }"

        1. 提取name字段
            [name]  //类似字典key 获取value

    逻辑判断：
        Logstash从 1.3.0 版开始支持条件判断和表达式。

        表达式支持下面这些操作符：

        equality, etc: ==, !=, <, >, <=, >=
        regexp: =~, !~
        inclusion: in, not in
        boolean: and, or, nand, xor
        unary: !()

        通常来说，你都会在表达式里用到字段引用。比如：

        if "_grokparsefailure" not in [tags] {
        } else if [status] !~ /^2\d\d/ and [url] == "/noc.gif" {
        } else {
        }
'''