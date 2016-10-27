#-*-coding:utf-8-*-

class Celsius001:
    def __init__(self, temperature = 0):
        self.temperature = temperature
   
    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32
       
def test_001():
    # create new object
    man = Celsius001()
   
    # set temperature
    man.temperature = 37
   
    # get temperature
    print man.temperature
   
    # get degrees Fahrenheit
    print man.to_fahrenheit()
   
    print man.__dict__
    
    
class Celsius002:
    def __init__(self, temperature = 0):
        self.set_temperature(temperature)
        
    def to_fahrenheit(self):
        return (self.get_temperature() * 1.8) + 32
        
    def get_temperature(self):
        return self._temperature
    
    def set_temperature(self, value):
        if value < -273:
            raise ValueError("Temperature below -273 is not possible")
        self._temperature = value
     
def test_002():
    # 会抛出异常 valueerror
    # c = Celsius002(-277)
    
    c = Celsius002(37)
    print c.get_temperature()
    
    c.set_temperature(10)
    print c.get_temperature()
    
    c._temperature = -434
    print c.get_temperature()
    c.set_temperature(-300)
    
class Celsius003(object):
    def __init__(self, temperature=0):
        self.temperature = temperature
    
    def to_fahrenheit(self):
        return (self.temperature * 1.8) +32
        
    def get_temperature(self):
        print("Getting value")
        return self._temperature
     
    def set_temperature(self, value):
        if value < -273:
            raise ValueError("Temperature below -273 is not possible")
        print("Setting value")
        self._temperature = value
        
    temperature = property(get_temperature, set_temperature)
    
def test_003():
    c = Celsius003()
    #print c.temperature
    #c.temperature = -33333
    
if __name__ == "__main__":
    test_003()