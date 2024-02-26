'''

    快照可以为正在运行的es集群做数据备份:
        1. 快照来自由官方
        2. 快照关注点在数据与原数据之上
        3. 快照不能恢复template


    快照作用:
        1.定期备份
        2.故障数据还原
        3.集群之间数据


    快照备份内容:
        1. 数据索引
        2. 元数据
            2.1 mapping
            2.2 setting
            2.3 alias
            2.4 pipline
            2.5 索引状态信息: 索引工作状态关闭或开启，是否只读
            2.6 分片信息:  描述每个分片对应的节点位置 以及状态
            2.7 事务日志:   包括未刷新到磁盘之前的数据，确保持久性
        3. template是不包含在快照内的，因此如果需要备份模板需要手动备份

    备份方案:
        1. snapshot 来着官方，备份关注点在 数据和元数据之上
        2. esdump   来着第三方，关注点在数据层面，可以备份template


    适用场景:
        1. snapshot
            1.1 适合在全量备份场景
            1.2 适合跨集群迁移
            1.3 在大集群场景下数据大影响带宽
            1.4 备份更安全设计备份translog
            1.5 依赖共享存储
        2. esdump
            2.1 轻量级
            2.2 做数据层面备份不做元数据备份
            2.3 不依赖共享存储
'''

'''
    # 共享存储配置
    vim config/elasticsearch.yaml
        path.repo=/data/package/elasticsearch01/backup
    # 重启所有node节点
    
    # PUT新增备份配置信息
    curl -XPUT -H 'Content-Type: application/json' http://127.0.0.1:9200/_snapshot/my_fs_backup -d '{
        "type": "fs",
        "settings": {
            "location": "/data/package/elasticsearch01/backup"
         }
    }'
'''

'''
    # 配置快照
    # 特点
        1. 每个注册的快照名称必须唯一
        2， 多个集群访问一个挂载路径最终只有一个es集群生效
        3. 快照会自己删除重复数据，在频繁做快照时压力小
        4. 每个快照互补干预，因此可以删除任意快照从而不影响其他快照使用
    # 创建快照
    curl -XPUT -H 'Content-Type: application/json' http://127.0.0.1:9200/_snapshot/my_fs_backup/my_cluster_index{now/d}

    # 查看当前备份任务列表
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/_snapshot/my_fs_backup/_current
    # 查看备份状态
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/_snapshot/my_fs_backup/_status
'''

'''
    # 备份恢复
    # 跨节点恢复方案
        1. 需要先将备份目录下的数据迁移到新节点
        2. 新es集群需要配置path.repo=<数据迁移目录>
        3. POST新增快照配置
        4. 快照恢复需要删除或关闭索引，或者在恢复是重命名
        5. 恢复完成后可以对index做_reindex 操作来恢复名称
        
    # 获取当前快照
    curl -XGET -H 'Content-Type: application/json' http://127.0.0.1:9200/_snapshot/my_fs_backup/_all?pretty
    # 恢复快照
    # 全量恢复
    curl -XPOST -H 'Content-Type: application/json' http://127.0.0.1:9200/_snapshot/my_fs_backup/<快照名称>/_restore

    # 全量恢复-恢复做重命名
    curl -XPOST -H 'Content-Type: application/json' http://127.0.0.1:9200/_snapshot/my_fs_backup/<快照名称>/_restore -d '{
        "rename_pattern": "(.+)",    //恢复时匹配值
        "rename_replacement": restore-$1    //恢复后的名称 $1来之pattern匹配值
    }'
    
    # 恢复指定index
    curl -XPOST -H 'Content-Type: application/json' http://127.0.0.1:9200/_snapshot/my_fs_backup/<快照名称>/_restore -d '{
        "indices": "index-01,index-02"
    }'
    
    
'''