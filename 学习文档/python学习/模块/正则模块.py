import re
'''
    通配符：
        \d 表示匹配一个数字
        \D 表示匹配一个非数字
        \W 表示匹配非数字字母的字符
        \w 表示匹配字母和字符
        \s 表示匹配任何空字符、制表符、换行符
        \S 表示匹配任何非空字符

    基础正则：
        .  表示匹配任意单个字符
        ?  表示匹配前面字符0-1次
        *  表示匹配前面字符0次到多次
        +  贪婪模式，尽可能匹配前面出现的多次
        {} 表示出现次数
        （）分组匹配
        [] 表示字符集匹配
        [-] 表示范围匹配
        [^] 表示not 取反同理不匹配
        ^   表示匹配开头
        $   表示匹配结尾
        |   表示或关系
        \<  行首牟定符号
        \>  行尾牟定符号
        
'''

test = 'asnka,nsdkalea,sdsax1msadml34'
# match 只会匹配开头切只会匹配一次
print(re.match('\\d+',test))
# search 只会匹配第一个匹配字符串
print(re.search('(?P<id>\\d+)',test).group('id'))
# compile 定义正则表达式，省去多次的pattern匹配
patt = re.compile('(?P<id>\\d+)')
print(patt.match(test))
print(patt.search(test).group('id'))
# 指定分割符号
print(re.split(',|a',test))
# 返回一个迭代器对象，通过__next__方法进行取值
print(re.finditer('\\d+',test).__next__().group())
# sub 用于替换，将正则匹配的结果替换成指定字符
print(re.sub('\\d+','K',test))