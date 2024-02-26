import configparser


def read_config():

    config = configparser.ConfigParser()


    print(config.read(
        filenames=r'C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\python学习\loki\config\config.ini',
        encoding='utf-8'
    ))
    # print(config.sections())

    for key,value in config['DEFAULT'].items():
        print(key,value)

if __name__ == '__main__':

    print(read_config())