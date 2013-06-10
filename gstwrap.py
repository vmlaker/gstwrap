"""Wrapper for gst module. Adds retrieval of 
command-line paramenters for GStreamer launch tool."""

import gst

class Element(object):
    """Wrapper of gst.Element class."""

    index = -1  # Maintain object count (index+1).

    def __init__(self, type, props=tuple(), name=''):
        """Initialize the object."""

        # Create the wrapped gst.Element object.
        Element.index += 1
        self._gst_element = gst.element_factory_make(
            type, 
            '{:s}{:d}'.format(name, Element.index),
            )

        # Maintain command-line string representation.
        self._cmd_string = '{:s} '.format(type)

        for ptype, pval in props:
            if ptype == 'caps':
                pval = gst.Caps(pval)
            self._gst_element.set_property(ptype, pval)
            self._cmd_string += '{:s}="{:s}" '.format(ptype, pval)

    def link(self, other):
        self._gst_element.link(other._gst_element)

    def addTo(self, gst_pipeline):
        gst_pipeline.add(self._gst_element)

    def addSinkProbe(self, func):
        pad = next(self._gst_element.sink_pads())
        pad.add_buffer_probe(func)

    def __str__(self):
        """Return command-line string representation."""
        return self._cmd_string


class Pipeline(object):
    """Wrapper of gst.Pipeline class."""

    def __init__(self, name=''):
        """Initialize the object."""

        # The wrapped gst.Pipeline object.
        self._gst_pipeline = gst.Pipeline(name)

        # Maintain count of elements.
        self._count = 0

        # Command-line parameters for the GStreamer launch tool.
        self._cmd_string = ''

    def start(self):
        """Start the pipeline."""
        self._gst_pipeline.set_state(gst.STATE_PLAYING)

    def add(self, element):
        """Add element to pipeline."""

        element.addTo(self._gst_pipeline)

        # Update the command-line parameters string.
        if self._count:
            self._cmd_string += '! '
        self._cmd_string += str(element)
        self._count += 1

    def __str__(self):
        """Return command-line parameters string."""
        return self._cmd_string
