class Person:
    def __init__(self, name: str, age: str):
        self.name = name
        self.age = age

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("name no puede ser vacío")
        self.__name = name

    @property
    def age(self):
        return self.__age
    @age.setter
    def age(self, age):
        if not age:
            raise ValueError("age no puede ser vacío")
        self.__age = int(age)


p1 = Person("Max", "25")
p2 = Person("Peter", "83")

print(p1.name)
print(p2.name)
