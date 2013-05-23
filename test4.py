"""Capture with GStreamer and display with OpenCV."""

import sys
import numpy as np
import cv2

from gstwrap import Element, Pipeline

DEVICE = sys.argv[1]
WIDTH  = int(sys.argv[2])
HEIGHT = int(sys.argv[3])
DEPTH  = int(sys.argv[4])

def onVideoBuffer(pad, idata):
    image = np.ndarray(
        shape=(HEIGHT, WIDTH, DEPTH),
        dtype=np.uint8,
        buffer=idata,
        )
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imshow('output', image)
    cv2.waitKey(1)

elements = [
    Element('v4l2src', [('device', DEVICE), ]),
    Element('ffmpegcolorspace'),
    Element('videoscale'),
    Element('capsfilter', [
            ('caps',
             'video/x-raw-rgb,width=%s,height=%s,bpp=%s'%(
                    WIDTH, HEIGHT, DEPTH*8)),
            ]),
    Element('fakesink'),
    ]

pipe = Pipeline()
for index in range(len(elements)):
    pipe.add(elements[index])
    if index:
        elements[index-1].link(elements[index])

elements[-1].addSinkProbe(onVideoBuffer)
print(pipe)
pipe.start()
raw_input('Hit <enter> to stop.')
