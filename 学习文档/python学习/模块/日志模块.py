import logging
import sys

'''
 参数:
         filename  使用filehandler ,将日志输入到指定的文件内
         filemode  文件写入模式默认使用追加方式
         format    定义日志格式
             # 常用方法
             %(asctime)s // 定义时间戳
             %(message)s // 传入的日志正文
             %(levelno)s // 打印日志级别的数值
             %(levelname)s   // 日志级别
             # 其他方法
             %(funname)s // 打印当前执行的函数名称
             %(thread)d  // 打印当前线程id号
             %(threadName)s  //打印当前线程名称
             %(process)d     // 打印进程ID号
             %(processName)s // 打印进程ID名称
             %(lineno)d      // 打印当前行号


         level      定义日志级别
             DEBUG 
             WARINNING
             INFO
             ERROR
             CRITICA 
     '''
logging.basicConfig(
    filename="abc.log",
    level=logging.DEBUG,
    encoding='utf-8',
    format="%(asctime)s [%(levelname)s]  %(message)s",
    datefmt="%m-%d-%y %H:%M:%S"

)
logging.debug('debug')
logging.info('info')
logging.warning('warning')
logging.error('error')

'''
    对象方式设置logging
    1. 输出至文件与窗口
'''

def test():

    # 获取logger 对象
    logger = logging.getLogger('test')

    # 设置一个日志处理方法
    # 文件
    fh = logging.FileHandler(filename='test.log', encoding='utf-8')
    # 终端
    ch = logging.StreamHandler(sys.stdout)
    # 设置日志文件格式
    fm = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")

    # 绑定日志格式到处理方法
    fh.setFormatter(fm)
    ch.setFormatter(fm)
    fh.setLevel('DEBUG')
    ch.setLevel('INFO')

    # logger 添加触发器
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.filter('a')

    return logger

a = test
print(a().info('a'))



