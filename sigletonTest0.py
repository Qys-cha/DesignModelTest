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
