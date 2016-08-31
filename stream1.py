import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *
import numpy as np
import smbus
import time
import logging
import struct


# Some constants
DS1624_READ_TEMP = 0xAA
DS1624_START = 0xEE 
DS1624_STOP = 0x22

bus = smbus.SMBus(1)
address = 0x48
bus.write_byte(address, DS1624_START)
time.sleep(.1)


stream_ids = tls.get_credentials_file()['stream_ids']

#Get stream id from stream id list
stream_id = stream_ids[0]

#Make instance of stream id object
stream = Stream(
  token = stream_id, # (!) link stream id to 'token' key
  maxpoints = 80      # (!) keep a max of 80 points on screen
)

#Initialize trace of streaming plot by embedding the unique stream_id
trace1 = Scatter(
  x=[],
  y=[],
  mode='lines+markers',
  stream=stream # (!) embed stream id, 1 per trace
)

data = Data([trace1])

#Add title to layout object
layout = Layout(title='Time Series')

#Make a figure object
fig = Figure(data=data, layout=layout)

# (@) Send fig to plotly, initialize streaming plot, open new tab
unique_url = py.plot(fig, filename='s7_first-stream')

import datetime
import time

# (@) Make instanc of the stream link object,
#     with same stream id as Stream id object
s = py.Stream(stream_id)

# (@) Open the stream
s.open()

i = 0   # a counter
k = 5   # some shape parameter
N = 200 # number of points to be plotted

#Delay start of stream by 5 sec (time to switch tabs)
time.sleep(5)

while True:
  i += 1 #add to the counter
  raw = bus.read_word_data(address, DS1624_READ_TEMP)

  # As the DS1624 is Big-endian and the Pi Little-endian, the byte order is reversed.
  temp_integer = raw & 0x00FF
  temp_fractional = ((raw & 0xFF00) >> 8) >> 3

  a, b = struct.unpack('bb', '{}{}'.format(chr(temp_integer), chr(temp_fractional)))
  temperature = a + (0.03125 * b)
  temperaturef = temperature * 9 / 5 + 32
  
  #Current time on x-axis, random numbers on y-axis
  x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
  y = temperaturef
  
  # (-) Both x and y are numbers (ie not lists or arrays)
  
  # (@) write to plotly stream!
  s.write(dict(x=x, y=y))
  
  # (!) write numbers to stream to append current data on plot,
  #     write lists to overwrite existing data on plot
  
  time.sleep(60) # (!) plot a point every 80 ms, for smoother plotting
  
# (@) Close the stream when done plotting
s.close()