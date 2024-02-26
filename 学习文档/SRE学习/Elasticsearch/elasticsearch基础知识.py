'''

    elasticsearch 存储方式:

        1. index： 多个文档组合
        2. 每个index都会有一个物理的文件
        3. lucense 会将index 切割多个分片，每个分片会分配到不通data节点
        4. 写压力被平均分配
        5. 每个分片(shard)会有副本分片，保证主分片丢失时index可用


    elasticsearch组件:
        1. type 类型，7x至上默认只允许一个_doc类型，正常情况下一个index 也只存储一种类型
        2. index 用于存储多个 key:values 多个doc 组成
        3. document 文档属于lucense 查询、检索的原子单位 ，key：values组成
        4. mapping  用于定义存储文档时的字段类型、分析器、切词、存储
        8. template
        9. setting

    elasticsearch集群组件：
        1. es 集群内部标识为集群名称，默认为elasticsearch，节点在加入集群时使用的就是集群名称
        2. 一个节点只能属于一个集群

        节点角色:
            1. node     用于存储数据、参与集群检索操作
            2. master   用于管理分片、路由主分片
            3. shard    es 将index 切分多个子分片，每个分片都是真实的文件存储index中一部分数据，
            shard 数量可自定义，但是一定要在创建index时确定多少个shard 数量，index创建后将不能在
            更改其shard数量

    elasticsearch工作过程:
        1. es 启动时会通过多播或单播方式监听在9300端口，来查找集群中的其他节点
        2. 通过集群名称来判断是否是一个集群中工作
        3. 集群中主节点是通过选举方式，通过比较 nodes/_id来比较出 主节点
        4. 当选举成功后，主节点来决定主shard 分片状态信息
        5. 每个es 中的节点 都可以接受、相应 client端请求
        6. 集群拥有3种工作状态: Red、Green、Yellow
            Red  此状态表示集群不可工作，其主shard 均丢失
            Green   工作状态正常
            Yellow  可查询 但不可以写入 表示修复状态


'''