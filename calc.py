class Calc:
    def add(self,a,b):
        return a + b

    def sub(self,a,b):
        return a -b

c=Calc()
x=c.add(5,7)
y=c.sub(5,7)
print(f"the diff between 5 and 7 is {y}")
