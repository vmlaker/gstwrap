import gst
import gstwrap
specs = (
    ('e1', 'v4l2src'),
    ('e2', 'xvimagesink'),
    )
pipe, elements, args = gstwrap.create(specs)
print(args)
pipe.set_state(gst.STATE_PLAYING)
raw_input('Hit <enter> to stop.')
