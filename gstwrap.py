"""Helper code for gst module."""

import gst

# When using this module in a multi-thread/process program,
# need to initialize Python threading in gobject module first.
# Let's just do this always.
import gobject
gobject.threads_init()  


def create(specs):
    """Given an iterable of GStreamer specifications, each
    specification having two or three elements of format:
       (name, gst_element, properties)
    where properties is optional, return three values:
       1) GStreamer pipeline
       2) dictionary of GStreamer elements
       3) string of GStreamer launch arguments
    """
    
    # Create pipeline and elements.
    pipeline = gst.Pipeline('hello')
    prev_element = None
    elements = dict()
    launch_args = ''  # Assemble a string for command line.
    for spec in specs:
        ekey = spec[0]
        etype = spec[1]
        try: eprops = spec[2]
        except: eprops = tuple()
        element = gst.element_factory_make(etype, '%s'%ekey)
        for ptype, pvalue in eprops:
            if ptype == 'caps':
                pvalue = gst.Caps(pvalue)
            element.set_property(ptype, pvalue)
        pipeline.add(element)
        elements[ekey] = element

        # Link this element to the previous element.
        if prev_element:
            prev_element.link(element)
        prev_element = element

        # Append to the launch auguments string.
        if launch_args:
            launch_args += ' ! '
        launch_args += '%s '%etype
        for prop in eprops:
            launch_args += ' %s=%s '%(prop[0], prop[1])

    return pipeline, elements, launch_args
