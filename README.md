gstwrap
=======

A wrapper of [GStreamer Python bindings](http://gstreamer.freedesktop.org/modules/gst-python.html).

*Make super-easy GStreamer pipelines in Python!*

Software requirements
---------------------

First make sure you have GStreamer Python bindings installed
by running
```
yum install gstreamer-python
```
or
```
apt-get install python-gst0.10
```

Some of the examples use OpenCV Python bindings.
```
yum install opencv-python
```

Running the examples
--------------------

```
python test1.py
python test2.py
python test3.py /dev/video0 640 480 3
python test4.py /dev/video0 640 480 3
python test5.py
python test6.py
```
