import io
import os
import SvgCanvas
from lxml import etree
import cairo
import rsvg
import sys

# ============================================================

def create_png(filename, width, height, svg_string):

	# Source: http://cairographics.org/download/
	# Example Code: http://stackoverflow.com/questions/6589358/convert-svg-to-png-in-python

	img = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
	ctx = cairo.Context(img)
	handler= rsvg.Handle(None, svg_string)
	handler.render_cairo(ctx)
	img.write_to_png(filename+".png")

# ============================================================

# HTML Contents
contents = "<html> \
<body> \
<table border='1' cellpadding=10> \
<trbgcolor='#DDDDDD'><td>SVG Code</td><td>SVG Image</td><td>PNG Image</td><td>Refresh Page</td><tr>"

# ============================================================

# Read directory
path = "../files/ascii/"
png_path = "../files/png/"

i = 1
count_error = 0
count_success = 0

print "----------------------";

for dirpath, dirnames, filenames in os.walk(path):
		print "Processing files:";
		for filename in [f for f in filenames if f.endswith(".ascsvg")]:
        
			# Read ASCIISVG files
			g = open(os.path.join(dirpath, filename),'r')
			ascii_text = g.read()
			g.close()

			print "# " + str(i) + " -> " + filename

			# SVG (xml script)
			my_svg = SvgCanvas.SvgCanvas(filename.split(".")[0], 400, 400) # default size of SVG
			my_svg.process_ascii_multi_line(ascii_text)
			xml = my_svg.generate_string()

			# XML object
			svg_object = etree.fromstring(xml)

			# PNG Image	
			create_png(png_path + filename.split(".")[0], int(float(svg_object.attrib['width'])), int(float(svg_object.attrib['height'])), xml) 

			# Append contents to the HTML page
			if ("ERROR" in xml): contents += "<tr bgcolor='#cd7879'><td>"; count_error += 1
			else: contents += "<tr bgcolor='#86cd78'><td>";  count_success += 1
			contents += "Folder: /" + dirpath.split("/")[-1] + "/<br>"
			if ("ERROR" in xml): contents += "Error: #" + str(count_error) + "<br>"
			else: contents += "Correct: #" + str(count_success) + "<br>"
			contents += "File: " + filename.split(".")[0] + ".png<br><br>"
			contents += "<textarea rows=20 cols=40>" + xml + "</textarea>"
			contents += "</td><td>"
			contents += xml
			contents += "</td><td>"
			contents += "<img src='" + png_path + filename.split(".")[0] + ".png'/>"
			contents += "</td><td>"
			contents += '<form><input type=button value="Refresh" onClick="window.location.reload()"></form>'
			contents += "</td></tr>"
		
			# Increment file name counter
			i = i + 1			
print "----------------------";
print "Success Count: " + str(count_success)
print "Error Count: " + str(count_error);
print "----------------------";

# ============================================================

# Complete HTML page
contents += "</table> \
</body> \
</html>"

# ============================================================

# Write HTML document
f = open('demo.html','w')
f.write(contents)
f.close()

# ============================================================

