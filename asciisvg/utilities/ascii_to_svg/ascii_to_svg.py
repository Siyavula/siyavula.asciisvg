# ========================================================
# UTILITIES SCRIPT
#
# Accepts an ASCII file, and creates an SVG file
# 
# Command: python ascii_to_svg.py < name.ascsvg > name.svg
#
# ========================================================

from __future__ import division
import math
import SvgCanvas

# ========================================================
# Main Code
# ========================================================

if __name__ == '__main__':
	a = SvgCanvas.SvgCanvas("svg1", 600, 600)

	ascii_string= ""
	while True:
		try:
			new_line = raw_input()
			ascii_string += new_line + "\n"
		except:
			break	

	a.process_ascii_multi_line(ascii_string)
	xml = a.generate_string()

	print xml

# ========================================================


