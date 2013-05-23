"""Helper code for gst module."""

import gst

# When using this module in a multi-thread/process program,
# need to initialize Python threading in gobject module first.
# Let's just do this always.
import gobject
gobject.threads_init()  

class Element(object):

    index = -1

    def __init__(self, type, props=tuple(), name=''):
        Element.index += 1
        self._gst_element = gst.element_factory_make(
            type, 
            '%s%d'%(name, Element.index),
            )
        self._cmd_string = '%s '%type
        for ptype, pval in props:
            if ptype == 'caps':
                pval = gst.Caps(pval)
            self._gst_element.set_property(ptype, pval)
            self._cmd_string += ' %s="%s" '%(ptype, pval)

    def link(self, other):
        self._gst_element.link(other._gst_element)

    def addTo(self, gst_pipeline):
        gst_pipeline.add(self._gst_element)

    def addSinkProbe(self, func):
        pad = next(self._gst_element.sink_pads())
        pad.add_buffer_probe(func)

    def __str__(self):
        return self._cmd_string

class Pipeline(object):

    def __init__(self, name=''):
        self._gst_pipeline = gst.Pipeline(name)
        self._count = 0
        self._cmd_string = ''

    def start(self):
        self._gst_pipeline.set_state(gst.STATE_PLAYING)

    def add(self, element):
        element.addTo(self._gst_pipeline)
        if self._count:
            self._cmd_string += '! '
        self._count += 1
        self._cmd_string += str(element)

    def __str__(self):
        return self._cmd_string
