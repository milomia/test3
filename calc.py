# comment for calculator class
# another comment
class Calc:
    def add(self,a,b):
        return a + b

    def sub(self,a,b):
        return a -b

    def mult(self,a,b):
        return a * b

    def div(self,a,b):
        # protect div by zero
        if (b == 0):
          return 0
        return a / b

    def mod(self,a,b):
        return a % b
        
