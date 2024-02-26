import os
import requests
import json
import time
import configparser
import re
import threading

_run_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class message(object):

    def __init__(self):
        self.run_file = []
        self.config = configparser.ConfigParser()
        self.config.read(
            filenames=os.path.join(_run_dir,'config','config.ini'),
            encoding='utf-8'
        )
        self.loki = self.config['default']['Loki_Server']
        self.path = self.config['default']['Log_Path']
        self.file = eval(self.config['default']['Log_File_Name'])
        self.pattern = eval(self.config['pattern']['Match_Pattern'])
        print(type(self.file),self.file,1111)
    def match_write(self,file,mes):
        file_name = file + '-' + time.strftime('%Y-%m-%d',time.localtime(time.time()))
        with open(file=os.path.join(_run_dir,'data',os.path.basename(file_name)),mode='a+',encoding='utf-8') as f :
            f.write(mes)
            f.flush()

    def get_time(self,t):
        Time = time.localtime(t)
        return time.strftime('%Y-%m-%d', Time)
    def get_config(*args,**kwargs):
        conf = kwargs.get('region')
        def inner(fun):
            def warsp(self,*args,**kwargs):
                label_dict = {}
                for k,v in self.config[conf].items():
                    label_dict[k] = v
                kwargs['label_dict'] = label_dict
                return fun(self,*args,**kwargs)
            return warsp
        return inner
    def list_file(fun,*args,**kwargs):
        def inner(self, *args, **kwargs):
            file_list = []
            for i in self.file:
                for n in os.listdir(self.path):
                    pattern = re.compile(i)
                    f = pattern.search(n)
                    try:
                        file = os.path.join(self.path,f.group())
                        file_time = time.strftime('%Y-%m-%d', time.localtime(os.path.getctime(file)))
                        if file_time == time.strftime('%Y-%m-%d', time.localtime(time.time())):
                            file_list.append(os.path.join(self.path,f.group()))
                    except Exception as  E:

                        continue
            result = fun(self, file=file_list)
            return result
        return inner
    def request_header(self,*args,**kwargs):
        entries = []
        entries.append([time.time_ns(), kwargs.get('message')])

        payload = {
            'streams': [{
                "stream": {},
                "values": entries
            }]
        }
        label = kwargs.get('label_dict')
        for key,value in label.items():
            payload['streams'][0]['stream'][key] = value
        payload['streams'][0]['stream']['level'] = kwargs.get('level')
        payload['streams'][0]['stream']['file'] = kwargs.get('file')
        payload = json.dumps(payload)
        return payload

    @get_config(region="lable")
    def send_message(self,*args,**kwargs):

        payload = self.request_header(*args,**kwargs)

        headers = {
            "Content-Type": "application/json"
        }
        loki_url = "{addr}/loki/api/v1/push".format(addr=self.loki)
        response = requests.post(
            url=loki_url,
            data=payload,
            headers=headers
        )
        print(response.status_code,response.text)
        if response.status_code == 204:
            print('发送成功')
        else:
            print('发送失败')

    def match_error(self,file,line):
        # 正则list
        pattern_list = self.pattern
        for m in pattern_list:
            pattern = re.compile(m,re.IGNORECASE)
            rest = pattern.search(line)

            if rest:
                self.send_message(file=file,message=rest.group(),level="ERROR")
                self.match_write(file=file,mes=line)
            else:
                continue
    def read_log(self,file):
        size = os.path.getsize(file)
        create_time = self.get_time(t=os.path.getctime(file))
        with open(file=file, mode='rb') as r:
            r.seek(size)
            while True:
                '''文件不存在退出'''
                if not os.path.exists(file):
                    self.run_file.remove(os.path.basename(file))
                    return
                else:
                    '''文件时间不一致退出'''
                    if create_time != self.get_time(t=time.time()):
                       self.run_file.remove(os.path.basename(file))
                       return
                    try:
                       size = os.path.getsize(file)
                       data = r.readline()
                       if not data:
                          r.seek(size)
                          continue
                       else:
                          self.match_error(file=file,line=data.decode('utf-8'))
                    except Exception as E:
                          self.run_file.remove(os.path.basename(file))
                          return

    def start_thread(self,file):
        t = []
        for i in file:
            if os.path.basename(i) not in self.run_file:
                self.run_file.append(os.path.basename(i))
                th = threading.Thread(target=self.read_log,kwargs={"file": i})
                t.append(th)
        for start in t:
            start.start()

    @list_file
    def res(self,file):
        return file
    def __call__(self, *args, **kwargs):
        print(args,kwargs)
        while True:
            print('11111111')
            self.start_thread(file=self.res())
            time.sleep(3)
if __name__ == '__main__':
    obj = message()
    obj()

