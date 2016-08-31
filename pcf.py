import smbus
import time

try:
  bus = smbus.SMBus(1)
except IOError:
  bus = smbus.SMBus(0)

#while True:
#  switch = bus.read_byte(0x21)
#  bus.write_byte(0x20, switch)
#  time.sleep(.1)

bus.write_byte(0x20, 0xFF)
