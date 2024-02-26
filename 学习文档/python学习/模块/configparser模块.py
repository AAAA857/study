import configparser


'''
    configparser 模块用于对ini 文件信息操作，通常用于配置、修改、删除、新增
    
    1.操作方式类似与字典操作方法



    参数:
        allow_no_value=True 默认配置key,value 形式保存，当配置文件中存在只有key 并没有values 时可以带此方法
        
'''
# 实例化出一个config对象，基于此对象进行配置文件操作
def create_config(fd):
    config = configparser.ConfigParser()

    # 创建一个config.ini 配置文件
    # 插入方式一

    # default 公共部分
    # 所有子区域查询时都会带上default内的配置
    config['DEFAULT'] = {
        "base": "true",
        "size": 1000
    }
    # 插入方式二
    config['server'] = {}
    config['server']['name'] = "www.baidu.com"
    res = config['server']
    res['prifx'] = "www"
    res['end'] = ".com"

    # 调用configparser write 方法，将新增的配置写入磁盘文件中
    config.write(fd)
    return True

# 读取配置文件
def read_config(file):
    '''

        1. 调用configparser.read()方法
        2. 返回一个字典key 对象
        3. 根据返回的key 对象进行修改、删除等操作
    :param file:
    :return:
    '''
    # 实例化出config对象
    # 返回配置文件列表
    config = configparser.ConfigParser(allow_no_value=True)
    # 读取配置文件,返回一个节点名称列表
    # return ['default', 'server']
    config.read(file)
    '''
    # 判断一个key 是否存在列表内
    if 'default' in config.sections():
        return True
    else:
        return  None
    '''
    '''
    # 获取节点下配置
    print(config['default']['size'])
    res = config['default']
    print(res.get('base'))
    '''
    for v in config.sections():
        mes = config[v].get('end')

        if mes == ".cn":

            pass
            '''
            config[v]['end'] = ".cn"
            print("修改完成 %s" % config[v]['end'])
            with open(file='config.ini',mode='w',encoding='utf-8') as w:
                config.write(w)
            '''

            '''
                1.删除
        
            del config[v]['end']
            print("删除完成")
            with open(file='config.ini', mode='w', encoding='utf-8') as w:
                config.write(w)
                
            '''






def read_config_string(file):

    config = configparser.ConfigParser()

    config.read_string('[DEFAULT]\nserver=1.1.1.1\n[server1]\nnumber=1')

    for i in config.sections():
        print(config[i]['number'])


def read_config_dict(d):

    config = configparser.ConfigParser(allow_no_value=False)
    config.read_dict(d)

    for i in config.sections():
        print(config[i].get('number'))
        print(config[i].get('skip-db'))


if __name__ == '__main__':

    d = {

        "server": {

            "number": 1,
            "size": 100,

        },
        "DEFAULT": {

            "base": "False"

        }

    }

    print(read_config(file='config.ini'))