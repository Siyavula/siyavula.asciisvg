# ========================================================
# UTILITIES SCRIPT
#
# Accepts an ASCII file, and creates an SVG file
# 
# Command: python svg_to_png.py < name.svg
#
# ========================================================

from lxml import etree
from SvgCanvas import create_png
import sys

# ========================================================

svg_string = sys.stdin.read()
svg_object = etree.fromstring(svg_string)
create_png("../files/png/file", int(float(svg_object.attrib['width'])), int(float(svg_object.attrib['height'])), svg_string) 

# ========================================================


