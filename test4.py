"""Capture with GStreamer and display with OpenCV."""

import sys
import numpy as np
import cv2
import gst

import gstwrap

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

specs = (
    ('e1', 'v4l2src', [('device', DEVICE), ]),
    ('e2', 'ffmpegcolorspace'),
    ('e3', 'videoscale'),
    ('e4', 'capsfilter', [
            ('caps',
             'video/x-raw-rgb,width=%s,height=%s,bpp=%s'%(
                    WIDTH, HEIGHT, DEPTH*8)),
            ]),
    ('e5', 'fakesink'),
    )
pipe, elements, args = gstwrap.create(specs)

pad = next(elements['e5'].sink_pads())
pad.add_buffer_probe(onVideoBuffer)

pipe.set_state(gst.STATE_PLAYING)
raw_input('Hit <enter> to stop.')
