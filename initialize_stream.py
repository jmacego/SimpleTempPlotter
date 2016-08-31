import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *

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
