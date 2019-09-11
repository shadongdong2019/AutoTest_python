from jpype import *
import os

classpath = os.path.join(os.path.abspath('.'), 'D:/WorkSpace/')
startJVM("/usr/bin/java/jdk1.8.0_211/jre/lib/amd64/server/libjvm.so","-ea", "-Djava.class.path=%s" % (classpath))
javaClass=JClass('test')
value="oldValue"
javaInstance=javaClass(value)
print(javaInstance.getValue())
javaInstance.setValue("newValue")
print(javaInstance.getValue())

print(java.lang.System.out.println("hello world"))
shutdownJVM()
