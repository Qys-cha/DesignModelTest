'''
    单例设计模式：确保类有且只有一个实例对象，并提供全局访问点，避免对同一资源产生冲突
    UML：
                Singleton
        -----------------------------
         -instance：Singleton
        ----------------------------
         - Singleton()
         + instance:Singleton
    python 实现
'''

class Singleton(object):
    '''
    通过覆盖__new__方法（Python用于实例化对象的特殊方法）来控制对象的创建
    方法hasattr（Python的特殊方法，用来了解对象是否具有某个属性）用于查看对象cls是否具有属性instance，该属性的作用是检查该类是否已经生成了一个对象
    '''
    def __init__(self):
       print("object inited")
       if not hasattr(self, 'instance'):
           print("init not has attr instance")

    def __new__(cls):
        if not hasattr(cls,'instance'):
            print("not has attr instance")
            Singleton.outStr(Singleton)
            cls.instance = super(Singleton,cls).__new__(cls)
        return cls.instance
    def outStr(self):
        print("can print")

#
# s = Singleton()
# print("object created",s)
# s1 = Singleton()
# print("object created",s1)
# s.outStr()
'''
    懒汉式实例化能够确保在实际需要时才创建对象。所以，懒汉式实例化是一种节约资源并仅在需要时才创建它们的方式。
'''
class Singleton(object):
    __instance = None
    def __init__(self):
        if not Singleton.__instance:
            print("__init__ method called.")
        else:
            print("Instance already created.",self.getInstance())
    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = Singleton()
        return cls.__instance
    def outputStr(self):
        print("obj already created")
    # def __new__(cls, *args, **kwargs):
    #     print("create obj")
    #     cls.__instance = super(Singleton, cls).__new__(cls)
    #     return cls.__instance
# s = Singleton()
# print(s)
# # s.outputStr()
# print("object created",Singleton.getInstance())
# s1 = Singleton()
# print(s,"\n",s1)
# s2 = Singleton()
# print(s2)

'''
所有对象共享相同状态，因此它也被称为Monostate（单态）模式
__shared_state赋给了变量__dict__（它是Python的一个特殊变量）。Python使用__dict__存储一个类所有对象的状态
'''
class Borg(object):
    __shared_state = {'1':'1'}
    def __init__(self):
        self.x = 1
        self.__dict__ = self.__shared_state
# class Borg(object):
#     __shared_state = {}
#     def __new__(cls, *args, **kwargs):
#         obj = super(Borg,cls).__new__(cls)
#         obj.__dict__ = obj.__shared_state
#         return obj
# a = Borg()
# b = Borg()
# print(a.__dict__,b.__dict__)
# b.x = 2
# print(a.__dict__,b.__dict__)
# a.y = 4
# print(a.__dict__,b.__dict__)

'''
元类是一个类的类，这意味着该类是它的元类的实例。使用元类，程序员有机会从预定义的Python类创建自己类型的类
如果我们说a=5，则type(a)返回<type'int'>，这意味着a是int类型。但是，type(int)返回<type'type'>，这表明存在一个元类，因为int是type类型的类。
类的定义由它的元类决定，所以当我们用类A创建一个类时，Python通过A=type(name, bases, dict)创建它
'''
class MyInt(type):
    def __call__(cls, *args, **kwargs):
        print("****here is my int ****",args)
        return type.__call__(cls,*args,**kwargs)
class int(metaclass = MyInt):
    def __init__(self,x,y):
        self.x = x
        self.y = y
'''当我们使用int(4,5)实例化int类时，MyInt元类的__call__方法将被调用，这意味着现在元类控制着对象的实例化'''
i = int(4,5)
print(type(i),i)
'''
元类单例实现
'''
class MetaSingleton(type):
    _instance = {}
    def __call__(cls):
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaSingleton,cls).__call__()
        return cls._instance[cls]
class Logger(metaclass=MetaSingleton):
    pass
    # def __new__(cls, *args, **kwargs):
    #     print("logger")

logger1 = Logger()
logger2 = Logger()
print(logger1,logger2,MetaSingleton._instance)
'''
这里不妨以需要对数据库进行多种读取和写入操作的云服务为例进行讲解。
完整的云服务被分解为多个服务，每个服务执行不同的数据库操作。
针对UI（Web应用程序）上的操作将导致调用API，最终产生相应的DB操作。
很明显，跨不同服务的共享资源是数据库本身。
'''
import sqlite3
class DateBase(metaclass=MetaSingleton):
    connection = None
    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect("db.sqlite3")
            self.cursorobj = self.connection.cursor()
        return self.cursorobj
'''
1．我们以MetaSingleton为名创建了一个元类。就像在上一节中解释的那样，Python的特殊方法__call__可以通过元类创建单例。
2．数据库类由MetaSingleton类装饰后，其行为就会表现为单例。因此，当数据库类被实例化时，它只创建一个对象。
'''
db1 = DateBase().connect()
db2 = DateBase().connect()
print(db1,db2)

'''
让我们考虑另一种情况，即为基础设施提供运行状况监控服务（就像Nagios所作的那样）。
我们创建了HealthCheck类，它作为单例实现。我们还要维护一个被监控的服务器列表。
当一个服务器从这个列表中删除时，监控软件应该觉察到这一情况，并从被监控的服务器列表中将其删除。
'''
class HealthCheck(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(HealthCheck,cls).__new__(cls)
        return cls._instance
    def __init__(self):
        self._servers = []
    def addServer(self):
        self._servers.append("Server 1")
        self._servers.append("Server 2")
        self._servers.append("Server 3")
        self._servers.append("Server 4")
    def changeServer(self):
        self._servers.pop()
        self._servers.append("Server 5")
hc1 = HealthCheck()
hc2 = HealthCheck()
hc1.addServer()
for i in range(4):
    print(hc1._servers[i])
hc1.changeServer()
for i in range(4):
    print(hc2._servers[i])

'''
虽然单例模式在许多情况下效果很好，但这种模式仍然存在一些缺陷。
由于单例具有全局访问权限，因此可能会出现以下问题:
    1.全局变量可能在某处已经被误改但是开发人员仍然认为它们没有发生变化，而该变量还在应用程序的其他位置被使用
    2.可能会对同一对象创建多个引用。由于单例只创建一个对象，因此这种情况下会对同一个对象创建多个引用
    3.所有依赖于全局变量的类都会由于一个类的改变而紧密耦合为全局数据，从而可能在无意中影响另一个类
对于单例模式来说，以下几点需要牢记:
    1.在许多实际应用程序中，我们只需要创建一个对象，如线程池、缓存、对话框、注册表设置等
      如果我们为每个应用程序创建多个实例，则会导致资源的过度使用。单例模式在这种情况下工作得很好
    2.单例是一种经过时间考验的成熟方法，能够在不带来太多缺陷的情况下提供全局访问点
    3.当然，该模式也有几个缺点。当使用全局变量或类的实例化非常耗费资源但最终却没有用到它们的情况下，
      单例的影响可以忽略不计
'''