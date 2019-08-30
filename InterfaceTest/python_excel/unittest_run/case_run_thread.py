#! /usr/bin/env python
#coding=utf-8
import threading
from multiprocessing import Queue
from time import ctime,sleep
from subprocess import Popen,PIPE
import os,time
lock=threading.Lock()
#单个测试用例生成的临时报告,当前目录下result\temp_年月日_时分秒\文件目录.html
#例如 E:\python\selenium\fortest\result\temp_20160704_102822\E_python_selenium_fortest_test_1_test1_py.html
def resultfile(tempdir,file):
    name=file.replace('\\','_').replace(':','').replace('.','_')+'.html'
    return os.path.join(tempdir,name)
class MyThread(threading.Thread):
    def __init__(self,queue,tempresultdir):
        threading.Thread.__init__(self)
        self.queue=queue
        self.tempresultdir=tempresultdir

    def run(self):
        while True:
            if not self.queue.empty():
                filename=self.queue.get()
                lock.acquire()
                resultname=resultfile(self.tempresultdir,filename)
                cmd="python "+filename+" "+resultname
                #print cmd
                print('start time:%s' %ctime())
                lock.release()
                p=Popen(cmd,shell=True,stdout=PIPE)
                #如果不加如下print,不会等待执行完毕
                print(p.stdout.readlines())
            else:
                print('end')
                break
#获取路径下test开头的文件夹下以test开头.py结尾的文件
def getfile(path):
    paths=[]
    for p in os.listdir(path):
        if p[0:4]=='test' and os.path.isdir(p):
            paths.append(p)
    file=[]
    for p in paths:
        temp=os.path.join(path,p)
        #print temp
        files=os.listdir(temp)
        #print files
        for f in files:
            if f[0:4]=='test' and f[-3:]=='.py':
                file.append(os.path.join(temp,f))
    return file
if __name__=='__main__':
    print('main start time:%s' %ctime())
    tempresultdir=os.path.join(os.getcwd(),"result","temp"+time.strftime("_%Y%m%d_%H%M%S",time.localtime(time.time())))
    os.mkdir(tempresultdir)
    resultreport=os.path.join(os.getcwd(),"result"+time.strftime("_%Y%m%d_%H%M%S",time.localtime(time.time())))
    allfile=getfile(os.getcwd())
    queue=Queue()
    for file in allfile:
        queue.put(file)
    my_Threads=[]
    my_Thread=threading.Thread()
    for i in range(2):
        my_Thread=MyThread(queue,tempresultdir)
        my_Thread.deamon=True
        my_Threads.append(my_Thread)
        my_Thread.start()
    for t in my_Threads:
        t.join()

    reports=os.listdir(tempresultdir)
    print(reports)
    print('main end time:%s' %ctime())