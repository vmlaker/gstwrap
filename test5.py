from gstwrap import Element, Pipeline

elements = (
    Element('videotestsrc'),
    Element(
        'capsfilter', 
        [('caps','video/x-raw-yuv,framerate=25/1,width=640,height=360')]
        ),
    Element(
        'timeoverlay',
        [('halign', 'left'),
         ('valign', 'bottom'),
         ('text', 'Stream time:'),
         ('shaded-background', 'true'),
         ]
        ),
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
