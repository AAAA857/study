'''
input {
        # 使用jdbc 连接器
        jdbc {
                # jdbc 连接jar包
                jdbc_driver_library => "/data/package/logstash-7.12.0/config/mariadb-java-client-2.4.2.jar"
                # jdbc 设备驱动class
                jdbc_driver_class => "Java::org.mariadb.jdbc.Driver"
                # mariadb 连接信息
                jdbc_connection_string => "jdbc:mariadb://10.180.0.41:3306/logstash"
                jdbc_user => "logstash"
                jdbc_password => "baidu@123"
                # 计划任务
                schedule => "*/1 * * * *"
                # 日志查询语句
                statement => "select * from name"
                # jdbc 连接时间 默认5s
                jdbc_pool_timeout => "5"
        }
}
output {
    stdout {}
}
'''
'''
常用参数:
    jdbc_password_filepath          // 文件密码路径
    jdbc_validation_timeout         // 连接频率
    jdbc_validation_connection      // 验证连接
    jdbc_user                       // 连接用户名
    jdbc_password                   // 连接用户名密码
    parameters                      // 指定mysql where 参数
    schedule                        // 计划任务执行时间
'''