from abc import ABC,abstractmethod

class Zoo(object):
    animal_instance = {}

    def __init__(self,name):
        self.name = name
    
    @classmethod
    def add_animal(cls,animal_instance):
        setattr(cls,animal_instance.__class__.__name__,True)

    def __getattr__(self,item):
        return False

class Animal(ABC):
    @abstractmethod
    def __init__(self,kind,shape,character):
        self.kind = kind
        self.shape = shape
        self.character = character
        
    def dangerous(self): 
        if self.kind == "食肉"  and self.character == "凶猛"  and (self.shape == '中' or self.shape == '大'):
            return True
        False

class Cat(Animal):
    voice = '喵喵叫'

    _instance = None
    @classmethod
    def __new__(cls,*args,**kargs):
        if not cls._instance:
            cls._instance = super(Cat, cls).__new__(cls)
        return cls._instance

    def __init__(self, name, kind, shape, character):
        super(Cat, self).__init__(kind, shape, character)
        self.name = name
          

if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    #print(getattr(z,'Cat'))
    print(cat1.voice)
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = getattr(z, 'Cat')
    z.add_animal(cat1)
    print(getattr(z,'Cat'))