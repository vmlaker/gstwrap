import sys
import gst
import gstwrap
DEVICE = sys.argv[1]
WIDTH  = int(sys.argv[2])
HEIGHT = int(sys.argv[3])
DEPTH  = int(sys.argv[4])
specs = (
    ('e1', 'v4l2src', [('device', DEVICE), ]),
    ('e2', 'ffmpegcolorspace'),
    ('e3', 'videoscale'),
    ('e4', 'capsfilter', [
            ('caps',
             'video/x-raw-yuv,width=%s,height=%s,bpp=%s'%(
                    WIDTH, HEIGHT, DEPTH*8)),
            ]),
    ('e5', 'xvimagesink'),
    )
pipe, elements, args = gstwrap.create(specs)
print(args)
pipe.set_state(gst.STATE_PLAYING)
raw_input('Hit <enter> to stop.')
