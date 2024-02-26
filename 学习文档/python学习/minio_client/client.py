from minio import  Minio
import os
import sys
import re
from  progress.bar import Bar
from a import Progress
class client(object):

    def __init__(self,ak,sk,minioServer,secure=True):
        self.ak = ak
        self.sk = sk
        self.secure = secure
        self.address = minioServer
        self.obj = self.create_object(secure=self.secure)
        self.p = []
        self.bucket = ""
    def create_object(self,secure=True):

        obj = Minio(endpoint=self.address,access_key=self.ak,secret_key=self.sk,secure=secure,region="package")
        return obj

    def put(self,object_name):

        total_size = os.path.getsize(object_name)
        pattern = re.compile(pattern=r'(\w)+\W(.*)')
        upload_path = pattern.match('/'.join(self.p)).group(2) + "/" + os.path.basename(object_name)
        with open(file=object_name,mode='rb') as r:
            self.obj.put_object(
                bucket_name=self.bucket,
                object_name=upload_path,
                data=r,
                length=total_size,
                progress=Progress()
            )

        return '上传完成'

    def get(self,object_name):

        data = self.obj.get_object(bucket_name=self.bucket,object_name=object_name)
        total_length = int(data.headers.get('content-length'))

        bar = Bar(object_name, max=total_length / 1024 / 1024,color="green",fill='*', check_tty=False,
                  suffix='%(percent).1f%% - %(eta_td)s')
        try:
            with open(os.path.basename(object_name), 'wb') as file_data:
                for d in data.stream(1024 * 1024):
                    bar.next()
                    file_data.write(d)
                    file_data.flush()
                bar.finish()

        except Exception as err:
            print(err)

    def Progress_Bar(self):
        print('bar')
        bar = Bar('Processing', max=20)
        for i in range(20):
            # Do some work
            bar.next()
        bar.finish()

    def cd(self,User_Selector_Prefix):

        p = re.compile(pattern=r"(\w+)(\W)")
        if User_Selector_Prefix == '..':
            self.p.pop()
        else:
            self.p.append(p.match(User_Selector_Prefix).group(1))

        if len(self.p) == 1:
            self.select(Bucket=self.bucket)
        else:
            pattern = re.compile(r'(\w)+\W(.*)')
            User_Selector_Prefix = pattern.match('/'.join(self.p)).group(2)

            self.select(Bucket=self.bucket,prefix=User_Selector_Prefix + "/")
    def get_bucket(self):
        bucket_li = [i.name for i in self.obj.list_buckets()]
        return bucket_li

    def select(self,Bucket,prefix=""):
        select_file = []
        if prefix is None:
            list_obj = self.obj.list_objects(bucket_name=Bucket)
        else:
            list_obj = self.obj.list_objects(bucket_name=Bucket,prefix=prefix)
        for bucket_file in list_obj:
            print(bucket_file.object_name)
            select_file.append(bucket_file)

        if len(select_file) == 0:
            print("当前%s为空"%Bucket+prefix)
    def ls(self,*args):

        if len(self.p) == 1:
            self.select(Bucket=self.p[0])
        else:
            s = '/'.join(self.p)
            pattern = re.compile(r'(\w)+\W(.*)')
            # print(pattern.match(s).group(2),'ls')
            self.select(Bucket=self.p[0],prefix=pattern.match(s).group(2) + "/")
    def Base_Terminal(self):
        while True:

            print("==============="
                  "minio client"
                  "===============")
            print("当前bucket:%s"%self.get_bucket())
            self.p = []
            User_Selector_Bucket = input("输入要查询的bucket名称:").strip()
            if not User_Selector_Bucket:
                continue
            self.bucket = User_Selector_Bucket
            self.p.append(User_Selector_Bucket)
            if User_Selector_Bucket.lower() == "exit":
                break
            self.select(Bucket=User_Selector_Bucket)
            while True:
                path = '/'.join(self.p)
                user_input = input("路径@{}:".format(path)).strip().split()
                if not user_input:
                    continue
                Action = user_input[0]
                try:
                    User_Selector_Prefix = user_input[1]
                except IndexError:
                    User_Selector_Prefix = ""

                if Action.lower() == "exit":
                    break
                if hasattr(self,Action):
                   resp = getattr(self,Action)
                   resp(User_Selector_Prefix)

                # p.append(User_Selector_Prefix)
                # pattern = re.compile(r'(\w)+/(.*)')
                # User_Selector_Prefix = pattern.match(os.path.sep.join(p)).group(2)
                # self.select(Bucket=User_Selector_Bucket,prefix=User_Selector_Prefix)

    def __call__(self, *args, **kwargs):
        self.Base_Terminal()
        # self.Progress_Bar()
        # self.obj.make_bucket(bucket_name="yin")
        # path = "test/a"
        dummy_data = b''
        # self.obj.put_object(
        #     "yin",
        #     "test" + "user.txt",
        #     io.BytesIO(dummy_data),
        #     len(dummy_data),
        #     content_type = "application/octet-stream"
        # )
        # result = self.obj.fput_object(
        #     bucket_name="yin",
        #     object_name="data/" + 'user.txt',
        #     file_path="/Users/yintiecheng/PycharmProjects/pythonProject/课程/函数篇/user.txt")
        #
        # print(result.object_name,result.etag,result.version_id)
if __name__ == '__main__':

    obj = client(
        minioServer="10.180.0.55",
        ak="yintiecheng",
        sk="yintiecheng@123",
        secure=False
    )

    print(obj())