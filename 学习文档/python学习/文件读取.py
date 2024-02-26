import os
import time

def read_file(file=None):

    with open(file='info.log', mode='rb') as file_obj:

            while True:
                tell = file_obj.tell()
                message = file_obj.readline()
                if not message:
                    size = os.stat('info.log').st_size
                    if size == 0:
                        file_obj.seek(0)
                    else:
                        file_obj.seek(tell)
                    time.sleep(0.5)
                else:
                    yield message

if __name__ == '__main__':

    for i in read_file():
        print(i.decode('utf-8'),end="")