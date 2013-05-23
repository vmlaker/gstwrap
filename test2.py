from gstwrap import Element, Pipeline
e1 = Element('v4l2src')
e2 = Element('xvimagesink')
pipe = Pipeline()
pipe.add(e1)
pipe.add(e2)
e1.link(e2)
print(pipe)
pipe.start()
raw_input('Hit <enter> to stop.')
