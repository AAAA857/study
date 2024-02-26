'''
    journald 是用与读取linux 中具体某个服务的日志输出
'''

'''
filebeat.inputs:
- type: journald
  # 读取所有服务的日志
  #id: everything
  # 读取单一服务或另外一个服务
  #id: sshd.service 
  #include_matches:
  #- _SYSTEMD_UNIT=sshd.service
  #- _SYSTEMD_UNIT=kubelet.service
  # 读取httpd access日志
  id: httpd.service
  # 日志读取位置
  # head 从头开始读取
  # tail 从尾部开始读取
  # cursor 第一次从头开始读取，后续服务重启在末尾读取
  seek: head
  # 匹配unit单元服务
  include_matches:
  - _SYSTEMD_UNIT=httpd.service
  tag:
  - "message"

output.logstash:
  hosts: ["127.0.0.1:5044"]
'''