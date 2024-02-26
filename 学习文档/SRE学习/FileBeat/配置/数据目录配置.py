'''

# filebeat 安装目录
path.home: /data/package/filebeat-7.17.16-linux-x86_64
# filebeat 配置目录
path.config: ${path.home}
# filebeat 数据目录
path.data: ${path.home}/data
# filebeat 日志目录
path.logs: ${path.home}/logs


# filebeat 模块加载目录
filebeat.config.modules:
  # Glob pattern for configuration loading
  path: ${path.config}/modules.d/*.yml
  #
  #     # Set to true to enable config reloading
'''