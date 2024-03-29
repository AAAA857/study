'''
    搜索引擎：
        全文搜索:
            1。检索
            2. 存储

        组成：
            1。索引链： 数据对应的索引
            2. 存储段:  保留数据
            3. 搜索组件: 用于分析、正规化、聚合等操作

        数据收集方式:
            1. 爬虫
            2. 日志

        文档:
            1. 类似mysql的表
            2. 文档存储的数据，数据结构是不一致的
            3.  key: value 形式
            4. 在lucense 中文档会根据词语做分词操作，用于全文索引
            5. 分词后会对词做权重排名
'''


# 搜索组件
'''
流程:
    1. 构建查询语句
    2. 运行查询
    3. 获取index
    4. 返回运行结构
'''
# 倒排索引
'''
    1. 会做文档切词
    2. 记录每个切词出现在那些文档中
    3. 根据记录的词出现位置找具体那些文档
    4. 组成格式 为 文档号 + 词
'''

# 文档组成
'''
    文档: 包含一个或多个域的容器
        域：key
        值: values
        
    域配置选项:
        1. mapping：
            1. 索引选项
                1. Index: ANYLYZED 表示字段内容可以做分析
                2. Index: Not-Anylyzed  不做分析
                3. Index: No    不做索引 不做查询
            2. 存储选项
                1. store: yes  存储原始值，额外占用真实空间
                2. store: no   按照默认方法进行存储
            3. 分析选项
                1. 
        2. 字段类型
                
    查询：
        1. lucene 会根据查询返回一个scoreDOC文档
        
        API：
            1. IndexSearch  搜索入口
            2. query
                   
'''
