#coding=utf-8
class Test(object):
    a = "Hello world!"

    def __init__(self): pass

    def test(self):
        # 在内部self.a和Test.a都可以访问实例变量
        Test.a="adfadf"
        print(Test.a)






A = Test()
A.test()