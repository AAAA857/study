class School(object):

    def __init__(self,school_name,school_path):
        self.School_Name = school_name
        self.School_Path = school_path

    def Enroll_Student(self):
        mes = '学校 [%s] 正在招生，位置 [%s]'%(self.School_Name,self.School_Path)
        return mes

class Techer(object):
    def __init__(self,s,name,age,subject):
        self.Techer_Name = name
        self.Techer_Age = age
        self.Techer_Subject = subject
        self.School_Obj = s
    '''
        @classmethod
    '''
    @classmethod
    def action_school(cls,s,school_name,school_path,name,age,subject):
        return cls(s(school_path=school_path,school_name=school_name),name,age,subject)


obj = Techer.action_school(s=School,school_name='北大青鸟',school_path='五道口校区',name='尹铁成',age=18,subject='Linux')

print(obj.School_Obj.Enroll_Student())


