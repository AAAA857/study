import os


r,w = os.pipe()
pipline = os.getpid()


def Write(fd,mes):
    number = 0
    while True:
         os.write(fd,mes)
         number += 1
         if number >= 10:
             break
def Read(fd):

        while True:
            read = os.read(fd,10)
            print(read)

input_data = 'hello world!'.encode('utf-8')

if __name__ == '__main__':
    r, w = os.pipe()	# 创建管道

    Write(fd=w,mes=input_data)
    Read(fd=r)


