class Vehicle:
    def __init__(self, brand):
        self.brand = brand

class Car(Vehicle):
    def __init__(self, brand, year):
        super().__init__(brand)
        self.year = year

c = Car("GTR", 2018)
print(c.brand, c.year)