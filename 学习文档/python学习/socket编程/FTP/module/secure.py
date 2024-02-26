import pickle
import hashlib
import random
import sys,os
import hmac

class auth:
    a = []
    a.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    a.append('database')
    a.append('data.pickle')
    path_f = os.sep.join(a)
    dic = {
        "user": None,
        "password": None
    }
    def __init__(self,username,password):
        self.username = username
        self.password = password


    def hmac_check(self,mes):
        h = hmac.new(key='abc'.encode('utf-8'),digestmod='MD5')
        h.update(msg=mes.encode('utf-8'))
        digest_bytes = h.hexdigest()
        return digest_bytes
    def read_password(self,file):
        with open(file=file,mode='rb') as f:
            res = pickle.load(file=f)
        return res
    def insert_user(self,d):
        '''判断用户是否重复存在'''
        for i in d:
            if i['user'] == self.username:
                return '用户已经存在'
        h_res = self.hmac_check(mes=self.password)
        with open(file=self.path_f, mode='wb') as f:
            self.dic['user'] = self.username
            self.dic['password'] = h_res
            d.append(self.dic)
            pickle.dump(obj=d, file=f)
        return '新增完成'

    def Token_Create(self,user):
        '''
        :return:   返回一个随机token 用户:token 持久保存文件
        '''
        t = []
        t.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
        t.append('database')
        t.append('token.pickle')
        token_f = os.sep.join(t)
        t_dict = {
            'user': None,
            'token': None
        }
        user_token = ''.join([chr(random.randint(65,90)) for i in range(20)])
        try:
            u = self.read_password(file=token_f)
        except Exception as E:
            u = []
        finally:
            for i in u:
                if i['user'] == user:
                    return i['token']
            with open(file=token_f,mode='wb') as f:
                t_dict['user'] = user
                t_dict['token'] = user_token
                u.append(t_dict)
                pickle.dump(obj=u,file=f)

            return user_token

    @property
    def Verify_Password(self):
        '''
            1. 校验用户密码
            2. 返回校验状态并且返回一个token
            3. token 用于client 与server 端校验通信状态
            4. token 持久保存在本地
        '''
        with open(file=self.path_f,mode='rb') as r:
            pickle_data =  pickle.load(file=r)
            for i in pickle_data:
                if i['user'] == self.username:
                    user_password = i['password']
                    '''返回用户输入密码加密结果'''
                    insert_password = self.hmac_check(mes=self.password)
                    '''校验逻辑'''
                    check_status = hmac.compare_digest(user_password,insert_password)
                    if check_status:
                        status,token = check_status,self.Token_Create(user=self.username)
                        return status,token
                    return check_status
            return False
    def Delete_User_Token(self):
        '''清空token逻辑'''
        pass
    def _create_user(self):
        '''
                   dump： 是将obj对象二进制后直接写入一个已经打开的file 对象内 它等同于 Pickler(file, protocol).dump(obj)。
                   dumps: 是将obj对象二进制后直接返回而不是写入到file文件内
                   load:  从已打开的 file object 文件 中读取封存后的对象，重建其中特定对象的层次结构并返回。它相当于 Unpickler(file).load()。
                   loads:  重建并返回一个对象的封存表示形式 data 的对象层级结构。 data 必须为 bytes-like object。
            '''
        '''返回密码加密结果'''
        try:
            d = self.read_password(file=self.path_f)
        except Exception as  E:
            d = []
        finally:
            res = self.insert_user(d=d)
        return res
if __name__ == '__main__':
    obj = auth(username='ytc1',password='12345673')
    print(obj.Verify_Password)




