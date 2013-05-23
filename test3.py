import sys
from gstwrap import Element, Pipeline

DEVICE = sys.argv[1]
WIDTH  = int(sys.argv[2])
HEIGHT = int(sys.argv[3])
DEPTH  = int(sys.argv[4])
elements = (
    Element('v4l2src', [('device', DEVICE), ]),
    Element('ffmpegcolorspace'),
    Element('videoscale'),
    Element('capsfilter', [
            ('caps',
             'video/x-raw-yuv,width=%s,height=%s,bpp=%s'%(
                    WIDTH, HEIGHT, DEPTH*8)),
            ]),
    Element('xvimagesink'),
    )
pipe = Pipeline()
for index in range(len(elements)):
    pipe.add(elements[index])
    if index:
        elements[index-1].link(elements[index])

print(pipe)
pipe.start()
raw_input('Hit <enter> to stop.')
