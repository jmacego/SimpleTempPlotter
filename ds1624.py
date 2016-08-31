import smbus

class DS1624:
  'Does some stuff'
  

  # Some constants
  DS1624_READ_TEMP = 0xAA
  DS1624_START = 0xEE 
  DS1624_STOP = 0x22
  DS1624_MEMORY = 0xAC
  DS1624_CONFIG = 0x17

  def __init__(self, address, bus):
    self.address = address
    self.bus = smbus.SMBus(bus)
    
    
  def start(self):
    self.bus.write_byte(self.address, self.DS1624_START)

  def get_config(self):
    return self.bus.read_byte_data(self.address, self.DS1624_CONFIG)

  def oneshot_on(self):
    config = self.__get_config()
    config = config | 0b00000001
    self.bus.write_byte_data(self.address, self.DS1624_CONFIG, config)
    
  def oneshot_off(self):
    config = self.__get_config()
    config = config & 0b11111110
    self.bus.write_byte_data(self.address, self.DS1624_CONFIG, config)
    
  def is_done(self):
    config = self.__get_config()
    return config & 0b10000000
  
  def __read_sensor(self):
    return self.bus.read_word_data(self.address, self.DS1624_READ_TEMP)

  def __convert_temp(self, raw):
    # DS1624 is big endian, pi is little endian. DS1624 also only uses first 12 bits
    temp_integer = raw & 0x00FF
    if temp_integer > 127:
      temp_integer = temp_integer - 256  
    temp_fractional = (raw >> 12) * 0.0625
    return temp_integer + temp_fractional
  
  def convert_c_f(self, temp_c):
    temp_f = temp_c * 9 / 5 + 32
    return temp_f
  
  def get_temp(self):
    raw = self.__read_sensor()
    return self.__convert_temp(raw)
  
  def get_temp_f(self):
    temp_c = self.get_temp()
    return self.convert_c_f(temp_c)

sensor = DS1624(0x48, 1)

sensor.start()

# print bin(sensor.__read_sensor())
print "%02.02fC" % sensor.get_temp()
print "%02.02fF" % sensor.get_temp_f()
