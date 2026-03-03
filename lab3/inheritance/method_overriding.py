class Person:
    def greet(self):
        print("Hello")

class Student(Person):
    def greet(self):
        print("Hello, I am a student")

Student().greet()