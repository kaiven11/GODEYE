#coding=utf-8
class Factory:
    def createFruit(self,zz):
        if zz=="apple":
            return Apple()
        elif zz=="banana":
                return Banana()
# class Fruit:
#     def __str__(self):
#         return "fruit"
class  Apple():
    def __str__(self):
        return "apple"
class Banana():
    def __str__(self):
        return "banana"
if __name__=="__main__":
            factory=Factory()
            print (factory.createFruit("apple") )
            print (factory.createFruit("banana")  )