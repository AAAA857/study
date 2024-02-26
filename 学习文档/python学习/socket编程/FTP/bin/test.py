import os.path
import re
import time

def test():

    with open(file=r'/学习目录/python学习/log/backend-backend-64b464f994-tdwwt.err.log', mode='ab') as f :
        while True:


            mess = r'[ERROR] [2023-12-18 18:08:52.807] [pool-11-thread-1] [,,] [c.b.i.k.p.i.KafkaProducerServiceImpl:160] []- [kafka callback] send message fail :ProducerRecord(topic=operateRecord-v7010, partition=null, headers=RecordHeaders(headers = [], isReadOnly = false), key=0191d59e-1053-400e-84e5-9e2bede997a9, value={"agentId":"36eab94b-bcff-4420-8ef3-59030aa1acb3","opObj":"train","opAction":"deploy","source":"default","dataAct":"UPDATE","uid":"t1000000001","dataId":"a302cbc1-0fc8-4fd1-b5af-6ff3c38ea0bc","id":"eb5c9a21e09e7f927466c6b8ca6c6b09","opDataTime":"2023-12-18 17:58:56","opModuleName":"表格问答模型管理","opModule":"table_qa_model_manager","opActionName":"部>署","opId":"0191d59e-1053-400e-84e5-9e2bede997a9","opObjId":"36eab94b-bcff-4420-8ef3-59030aa1acb3:a302cbc1-0fc8-4fd1-b5af-6ff3c38ea0bc","agentName":"test1111","opOrder":87526988900271100,"opObjName":"模型","opTime":"2023-12-18 17:58:57","clientIp":"::ffff:10.85.114.165","sourceName":"默认","keyRecord":1,"username":"user1"}, timestamp=null)' + '\r'
            f.write(mess.encode('utf-8'))
            f.flush()
            time.sleep(1)




def time_test():
    filepath = os.path.getctime(r'C:\Users\THINKPAD\PycharmProjects\pythonProject\学习目录\python学习\log\log.log')
    timeStruct = time.localtime(filepath)
    print(filepath)
    return time.strftime('%Y-%m-%d', timeStruct)

print(test())