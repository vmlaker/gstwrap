"""Implementation of pipeline at
http://stackoverflow.com/q/6911954/1510289"""

from gstwrap import Element, Pipeline

elements = (

    # From src to sink [0:5]
    Element('v4l2src'),
    Element('capsfilter', [('caps','video/x-raw-yuv,framerate=30/1,width=640,height=360')]),
    Element('tee', [('name', 't_vid')]),
    Element('queue'),
    Element('videoflip', [('method', 'horizontal-flip')]),
    Element('xvimagesink', [('sync', 'false')]),

    # Branch 1 [6:9]
    Element('queue'),
    Element('videorate'),
    Element('capsfilter', [('caps', 'video/x-raw-yuv,framerate=30/1')]),
    Element('queue'),

    # Branch 2 [10:15]
    Element('alsasrc'),
    Element('capsfilter', [('caps', 'audio/x-raw-int,rate=48000,channels=2,depth=16')]),
    Element('queue'),
    Element('audioconvert'),
    Element('queue'),

    # Muxing
    Element('avimux', [('name', 'mux')]),
    Element('filesink', [('location', 'me_dancing_funny.avi')]),
)

pipe = Pipeline()

for index in range(len(elements)):
    pipe.add(elements[index])

elements[0].link(elements[1])
elements[1].link(elements[2])
elements[2].link(elements[3])
elements[3].link(elements[4])
elements[4].link(elements[5])

# Branch 1
elements[2].link(elements[6])
elements[6].link(elements[7])
elements[7].link(elements[8])
elements[8].link(elements[9])

# Branch 2
elements[10].link(elements[11])
elements[11].link(elements[12])
elements[12].link(elements[13])
elements[13].link(elements[14])
elements[14].link(elements[15])

# Muxing
elements[9].link(elements[15])
elements[15].link(elements[16])

print(pipe)
pipe.start()
raw_input('Hit <enter> to stop.')
