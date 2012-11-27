# ========================================================
# UTILITIES SCRIPT
#
# Accepts an ASCII file, and creates an SVG file
# 
# Command: python svg_to_png.py < name.svg
#
# ========================================================

from lxml import etree
import sys

# ========================================================

def create_png(filename, width, height, svg_string):

	# Source: http://cairographics.org/download/
	# Example Code: http://stackoverflow.com/questions/6589358/convert-svg-to-png-in-python

	img = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
	ctx = cairo.Context(img)
	handler= rsvg.Handle(None, svg_string)
	handler.render_cairo(ctx)
	img.write_to_png(filename+".png")

# ========================================================

svg_string = sys.stdin.read()
svg_object = etree.fromstring(svg_string)
create_png("../files/png/file", int(float(svg_object.attrib['width'])), int(float(svg_object.attrib['height'])), svg_string) 

# ========================================================


