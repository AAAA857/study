import time
import datetime
import calendar

print(time.perf_counter())
print(calendar.month(2024,1))
print(datetime.datetime.now())

# 打印结构化时间
res = time.localtime()
print(res.tm_year,res.tm_mon,res.tm_hour)
print(res)

# 打印时间戳
print(time.time())
print(time.gmtime())

# 字符串时间格式化
Time = time.strftime('%Y-%m-%d %X',time.localtime())
print(Time)

# 字符串时间格式转换结构化时间
Time = time.strptime('2023-11-15','%Y-%m-%d')
print(Time)

# 获取字符串格式化时间
# retunt: Wed Nov 15 10:29:57 2023
Time = time.asctime(time.localtime(time.time()))
print(Time)

# 将格式化时间转换为时间戳
# time.mktime(字符串格式化时间)
a = time.strftime('%Y-%m-%d',time.localtime())
Time = time.mktime(time.strptime(a,'%Y-%m-%d'))
print(Time)
print(time.process_time())