# -*- coding: utf-8 -*-
from __future__ import division
import math
from lxml import etree
import re
import sys

# ===================================================================================	

class SvgCanvas:

	# ==============================
	# Variables
	# ==============================

	loc_var = {}
	complete_string = ""
	error_string = ""	
	debug_string = ""
	xml_parent = None
	xml_pointer = None
	xml_parent_pointer = None

	# Error Handling
	loc_var["complete_log"] = 0			# SVG Flags: Completed lines of code
	loc_var["error_log"] 		= 1			# SVG Flags: Errors that occur

	# Canvas Variables
	loc_var["xmin"] = loc_var["defaultxmin"] 								= -5
	loc_var["xmax"] = loc_var["defaultxmax"] 								= 5
	loc_var["ymin"] = loc_var["defaultymin"] 								= -5
	loc_var["ymax"] = loc_var["defaultymax"] 								= 5
	loc_var["xscl"] = loc_var["defaultxscl"] 								= 1
	loc_var["yscl"] = loc_var["defaultyscl"] 								= 1
	loc_var["xgrid"] = loc_var["defaultxgrid"] 							= 1
	loc_var["ygrid"] = loc_var["defaultygrid"] 							= 1
	loc_var["xtick"] = loc_var["defaultxtick"] 							= 4
	loc_var["ytick"] = loc_var["defaultytick"] 							= 4
	loc_var["border"] = loc_var["defaultborder"] 						= 0
	loc_var["height"] = loc_var["defaultheight"]  					= 600
	loc_var["width"] = loc_var["defaultwidth"]							= 600
	loc_var["xunitlength"] = loc_var["defaultxunitlength"] 	= 1
	loc_var["yunitlength"] = loc_var["defaultyunitlength"] 	= 1
	loc_var["origin"] = loc_var["defaultorigin"] 						= [0,0]

	# Element Variables
	loc_var["axesstroke"] = loc_var["defaultaxesstroke"] 							= "black"
	loc_var["gridstroke"] = loc_var["defaultgridstroke"] 							= "grey"
	loc_var["strokewidth"] = loc_var["defaultstrokewidth"] 						= 1 					
	loc_var["strokedasharray"] = loc_var["defaultstrokedasharray"] 		= [1, 0]
	loc_var["stroke"] = loc_var["defaultstroke"] 											= "black"
	loc_var["arrowfill"] = loc_var["defaultarrowfill"] 								= loc_var["stroke"]
	loc_var["fill"] = loc_var["defaultfill"] 													= "none"
	loc_var["fontstyle"] = loc_var["defaultfontstyle"] 								= "italic"
	loc_var["fontfamily"] = loc_var["defaultfontfamily"] 							= "times"		
	loc_var["fontsize"] = loc_var["defaultfontsize"]									= 16
	loc_var["fontweight"] = loc_var["defaultfontweight"] 							= "normal"
	loc_var["fontstroke"] = loc_var["defaultfontstroke"] 							= "none"
	loc_var["fontfill"] = loc_var["defaultfontfill"] 									= "black"  
	loc_var["markerstrokewidth"] = loc_var["defaultmarkerstrokewidth"]= 1
	loc_var["markerstroke"] = loc_var["defaultmarkerstroke"] 					= "black"
	loc_var["markerfill"] = loc_var["defaultmarkerfill"] 							= "yellow"
	loc_var["markersize"] = loc_var["defaultmarkersize"] 							= 4
	loc_var["marker"] = loc_var["defaultmarker"] 											= "none"
	loc_var["dotradius"] = loc_var["defaultdotradius"] 								= 4
	loc_var["ticklength"] = loc_var["defaultticklength"] 							= 4
	
	# Function Variables
	loc_var["f_func"] = None
	loc_var["g_func"] = None

	# Formula Variables
	loc_var["cpi"] 		= "&#960;"
	loc_var["ctheta"] = "&#952;"

	# SVG Labels
	loc_var["above"] = "above"
	loc_var["below"] = "below"
	loc_var["left"] = "left"
	loc_var["right"] = "right"
	loc_var["aboveleft"] = "aboveleft"
	loc_var["aboveright"] = "aboveright"
	loc_var["belowleft"] = "belowleft"
	loc_var["belowright"] = "belowright"
	loc_var["open"] = "open"
	loc_var["closed"] = "closed"

	# ========================================================================================

	'''
	==============================
	Functions (Initialization)
	==============================
	> __init__
	> convert_ascii_to_python()
	> mathjs
	> process_ascii_multi_line
	> process_ascii_single_line
	> generate_string
	> reset_variables
	> frange
	> jrange
	> removeComments
	> initPicture
	> setBorder
	============================== 
	'''

	# ========================================================================================

	def __init__(self, name, width=None, height=None):

		self.reset_variables()		# Reset variables
		self.xml_parent = etree.fromstring("<svg></svg>")		# Initialize SVG Canvas
		self.xml_parent.attrib['id'] = str(name)
		if (width != None): self.loc_var["width"] = int(float(width))
		if (height != None): self.loc_var["height"] = int(float(height)) 
		self.start_group()	# Create a blank rotation group
		self.initPicture(-5,5,-5,5)

		# Declare Functions as Variables
		self.loc_var["mathjs"] = self.mathjs
		self.loc_var["dprint"] = self.dprint
		self.loc_var["process_text"] = self.process_text
		self.loc_var["find_quote_pairs"] = self.find_quote_pairs

		self.loc_var["initPicture"] = self.initPicture
		self.loc_var["setBorder"] = self.setBorder
		self.loc_var["text"] = self.text
		self.loc_var["arrowhead"] = self.arrowhead
		self.loc_var["dot"] = self.dot
		self.loc_var["line"] = self.line
		self.loc_var["ellipse"] = self.ellipse
		self.loc_var["circle"] = self.circle
		self.loc_var["arc"] = self.arc
		self.loc_var["noaxes"] = self.noaxes
		self.loc_var["axes"] = self.axes
		self.loc_var["grid"] = self.grid
		self.loc_var["rect"] = self.rect
		self.loc_var["path"] = self.path
		self.loc_var["plot"] = self.plot
		self.loc_var["curve"] = self.curve
		self.loc_var["bunnyhop"] = self.bunnyhop
		self.loc_var["smoothcurve"] = self.smoothcurve
		self.loc_var["petal"] = self.petal
		self.loc_var["heart"] = self.heart
		self.loc_var["slopefield"] = self.slopefield
		self.loc_var["xml_get_pointer"] = self.xml_get_pointer
		self.loc_var["start_group"] = self.start_group
		self.loc_var["stop_group"] = self.stop_group
		self.loc_var["angle_arc"] = self.angle_arc
		self.loc_var["cloud"] = self.cloud
		self.loc_var["star"] = self.star
		self.loc_var["grass"] = self.grass
		self.loc_var["flower"] = self.flower

		# Special Functions
		self.loc_var["frange"] = self.frange										# Decimal-compatible "range"
		self.loc_var["jrange"] = self.jrange										# Javascript in Python

		# Math Functions
		for key in [	'sin','cos','tan','asin','acos','atan','sinh','cosh', 									'tanh','asinh','acosh','atanh','log','pi','e','sqrt', 'floor', 'ceil']:
			self.loc_var[key] = math.__getattribute__(key)

# ===================================================================================	

	def preprocess_block(self,ascii_str):

		a = ascii_str																						# Storing string as a new variable
		# Remove Comments
		a = re.sub(re.compile("/\*.*?\*/",re.DOTALL ),"",a) 		# Javascript: /* COMMENT */
		a = re.sub(re.compile("//.*?\n"),"\n",a) 								# Javascript: // COMMENT \n
		a = re.sub(re.compile("#.*?\n"),"\n",a) 								# Python: # COMMENT \n
		# Clean spacing before opening/closing braces		
		nl_char = str(chr(10))																	# Define: New Line character
		tab_char = str(chr(9))																	# Define: TAB character
		# Remove spaces before bracket
		while(a != a.replace(" {", "{")): a = a.replace(" {", "{")
		while(a != a.replace(tab_char+"{", "{")): a = a.replace(tab_char+"{", "{")
		while(a != a.replace(" }", "}")): a = a.replace(" }", "}")
		while(a != a.replace(tab_char+" }", "}")): a = a.replace(tab_char+" }", "}")
		# Clean blank lines to ONLY \n
		while(a != a.replace(" \n", "\n")): a = a.replace(" \n", "\n")
		while(a != a.replace(tab_char+"\n", "\n")): a = a.replace(tab_char+"\n", "\n")
		while(a != a.replace(nl_char+"\n", "\n")): a = a.replace(nl_char+"\n", "\n")
		# Remove blank lines before bracket
		while(a != a.replace(nl_char+"{", "{")): a = a.replace(nl_char+"{", "{")
		# Remove spaces between STATEMENT() and bracket
		while(a != a.replace(" {", "{")): a = a.replace(" {", "{")
		while(a != a.replace(tab_char+"{", "{")): a = a.replace(tab_char+"{", "{")
		# Remove spaces between : and bracket
		a = a.replace('{', ':') 																	# Opening Braces
		a = a.replace('}', '') 																		# Closing Braces

		return a

# ===================================================================================	

	def preprocess_line(self,ascii_str):
		
		# Pre-processing of code (no EXEC command running yet)
		a = ascii_str																						# Storing string as a new variable
		a = a.replace("^", "**")																# Exponent
		a = a.replace("||", " or ")												  		# OR
		a = a.replace("&&", " and ")														# AND
		a = a.replace("else if", "elif")												# IF / ELSE IF / ELSE statements
		a = a.replace("null", "None")														# "None" elements
		a = a.replace('"green"', '"darkgreen"') 								# Colours
		a = a.replace("'green'", "'darkgreen'") 								# Colours
		a = a.replace("String(", "str(") 												# String Handling

		# Replace FOR LOOP
		if (len(re.findall("(^|[^a-zA-Z])for[^a-zA-Z]", a)) == 1):
			original_a = a
			level = 0
			start_i = 0
			end_i = len(a)

			# Isolate contents of for-loop bracket
			start_i = a.index("for") + len("for")
			for i in range(start_i, end_i):
				if (a[i] == "("): level += 1			# Determine level/depth
				if (a[i] == ")"): level -= 1			# Determine level/depth
				if (a[i] == "(" and level == 1): start_i = i + 1			# Capture start index
				if (a[i] == ")" and level == 0): end_i = i; break;		# Capture end index
			a_list = a[start_i:end_i].split(";")	# Capture insides
			
			# If it is a legitimate FOR LOOP, proceed
			if len(a_list) == 3:
				start_cond 	= (a_list[0].replace("var ", "")).strip()		# Clean start_cond term
				end_cond 		= a_list[1].strip()													# Clean end_cond term
				leap_cond 	= a_list[2].strip()													# Clean leap_cond term
				i_character = re.findall(r'\w', a_list[1])[0]		# Find most common character (usually i)

				# Replace java -> python FOR LOOP
				a = a.replace(	a[start_i-1: end_i+1], " "+str(i_character) + " in " + \
												"jrange('" + str(start_cond) +"','"+str(end_cond)+"','"+str(leap_cond)+"')")

		return a

# ========================================================================================

	def mathjs(self, string):
	
		# Replace all un-defined functions
		string = string.replace("cosec", "1/math.sin")
		string = string.replace("sec", "1/math.cos")
		string = string.replace("cot", "1/math.tan")
		string = string.replace("acosec", "1/math.asin")
		string = string.replace("asec", "1/math.acos")
		string = string.replace("acot", "1/math.atan")
		string = string.replace("cosech", "1/math.sinh")
		string = string.replace("sech", "1/math.cosh")
		string = string.replace("coth", "1/math.tanh")
		string = string.replace("acosech", "1/math.asinh")
		string = string.replace("asech", "1/math.acosh")
		string = string.replace("acoth", "1/math.atanh")

		return string

# ========================================================================================

	def find_quote_pairs(self, text):

		# Returns an array mapping all the strings in the text

		# Variabes
		index_default = None
		quote_pair = [index_default,index_default]
		quote_types = ["'", '"']
		quote_open = ""
		quote_map = []

		i = 0
		while i < len(text):

			parity = False # does text[i] have a preceeding slash? (default = false)
			char_current = text[i]

			# Is the character a valid quote?
			if (char_current in quote_types):
	
				# Count parity for quote_current (check repetitively for all \\ slashes)
				j = 0
				while (j <= i) and (text[i-j-1] == "\\"):
					# Toggle parity
					parity = not (parity)
					j += 1

				if (parity == False):

					if (quote_pair[0] == index_default): 
						# Open the pair
						quote_pair[0] = i
						quote_open = char_current
				
					elif (quote_open == char_current):
						# Close the pair
						quote_pair[1] = i
						# Append to list
						quote_map.append(quote_pair + [(quote_open == quote_types[0] and "single" or "double")])
						# Reset Variables		
						quote_pair = [index_default,index_default]
						quote_open = ""
			
			i += 1

		return quote_map

# ========================================================================================

	def process_text(self, text):
	
		quote_map =	self.find_quote_pairs(text); quote_map.sort(); quote_map.reverse()  # Reverse Sort

		for quote_map_piece in quote_map:

			# Isolate Piece
			piece = text[quote_map_piece[0]+1:quote_map_piece[1]]
			
			# Variables
			final_piece = ""
			tail_stack = []
			
			# Search string
			i = 0
			while i < len(piece):

				# Superscript
				if (i < len(piece)) and (piece[i:i+2] == "^{"):
					# Double Quote
					if (quote_map_piece[2] == "double"):
						final_piece += "<tspan dy='\"+str(int(-fontsize)*0.7)+\"' font-size='\"+str(int(fontsize)*0.7)+\"'>"
						tail_stack.append("</tspan><tspan dx='\"+str(int(-fontsize)*0.3)+\"' dy='\"+str(int(fontsize)*0.7)+\"' font-size='\"+str(int(fontsize)/0.7)+\"'> </tspan>")
					# Single quote
					elif (quote_map_piece[2] == "single"):
						final_piece += '<tspan dy="\'+str(int(-fontsize)*0.7)+\'" font-size="\'+str(int(fontsize)*0.7)+\'">'
						tail_stack.append('</tspan><tspan dx="\'+str(int(-fontsize)*0.3)+\'" dy="\'+str(int(fontsize)*0.7)+\'" font-size="\'+str(int(fontsize)/0.7)+\'"> </tspan>')
					# Increment counter (one extra)
					i += 1

				# Subscript
				elif (i < len(piece)) and (piece[i:i+2] == "_{"):
					# Double Quote
					if (quote_map_piece[2] == "double"):
						final_piece += "<tspan dy='\"+str(int(fontsize)*0.25)+\"' font-size='\"+str(int(fontsize)*0.7)+\"'>"
						tail_stack.append("</tspan><tspan dx='\"+str(int(-fontsize)*0.3)+\"' dy='\"+str(int(-fontsize)*0.25)+\"' font-size='\"+str(int(fontsize)/0.7)+\"'> </tspan>")
					# Single quote
					elif (quote_map_piece[2] == "single"):
						final_piece += '<tspan dy="\'+str(int(fontsize)*0.25)+\'" font-size="\'+str(int(fontsize)*0.7)+\'">'
						tail_stack.append('</tspan><tspan dx="\'+str(int(-fontsize)*0.3)+\'" dy="\'+str(int(-fontsize)*0.25)+\'" font-size="\'+str(int(fontsize)/0.7)+\'"> </tspan>')
					# Increment counter (one extra)
					i += 1

				# Plain Bracket
				elif (piece[i] == "{"):
					# Double Quote
					if (quote_map_piece[2] == "double"):
						final_piece += "<tspan>"
						tail_stack.append("</tspan>")
					# Single quote
					elif (quote_map_piece[2] == "single"):
						final_piece += '<tspan>'
						tail_stack.append('</tspan>')
				
				# Closing Bracket
				elif (piece[i] == "}"):
					# Pick last closing bracket from stack & delete
					if (len(tail_stack) > 0):
						final_piece += tail_stack[-1]
						del tail_stack[-1]
				
				# Else, add the character
				else:
					final_piece += piece[i]

				# Increment counter
				i += 1

			# Integrate Piece
			text = text[:quote_map_piece[0]+1] + final_piece + text[quote_map_piece[1]:]
				
		return text

# ===================================================================================	

	def process_ascii_multi_line(self, ascii_string):

		# Format Text (superscript & subscript)
		b = self.process_text(ascii_string)			# Convert Ascii to Python (except FOR loops)

		# Process Javascript -> Python (brackets)
		b = self.preprocess_block(b)			# Convert Ascii to Python (except FOR loops)
	
		# Process Javascript -> Python (keywords)
		final_string = ""
		ascii_list = b.split('\n')		
		for ascii_line in ascii_list:
			if len(ascii_line) > 0:
				a = self.preprocess_line(ascii_line)		# Convert Ascii to Python (except FOR loops)
				a = self.mathjs(a)											# Math Formulas
				final_string += a + '\n'

		# Try Except
		try:
			exec(final_string, None, self.loc_var)
			self.complete_string += "\nASCII -> SVG conversion complete. \n\nOriginal Code:\n\n" + str(ascii_string) + "\n\nCode Processed:\n\n" + str(final_string) 
		except Exception, err:
			self.error_string += "\nASCII -> SVG conversion ERROR: " + str(err) + ", " + str(sys.exc_info()[0]) + "\n\nOriginal Code:\n\n" + str(ascii_string) + "\n\nCode Processed:\n\n" + str(final_string) 

# ===================================================================================	

	process_ascii = process_ascii_multi_line

# ===================================================================================	

	def process_ascii_single_line(self, ascii_string):

		b = self.preprocess_block(ascii_string)			# Convert Ascii to Python (except FOR loops)

		ascii_list = b.split('\n')		
		for ascii_line in ascii_list:
			if len(ascii_line) > 0:
				a = self.preprocess_line(ascii_line)		# Convert Ascii to Python (except FOR loops)
				a = self.mathjs(a)											# Math Formulas
				try:
					exec(a, None, self.loc_var)
					self.complete_string += "\nComplete: " + str(a)
				except Exception, err:				
					self.error_string += "\nERROR: " + str(a) + "\nMessage: " + str(err) + ", " + str(sys.exc_info()[0])
					break

		return ascii_string

# ===================================================================================

	def generate_string(self):

		self.str_parent = etree.tostring(self.xml_parent, pretty_print=True)	

		if ((self.loc_var["complete_log"] == 1 and len(self.complete_string) > 0) or (self.loc_var["error_log"] == 1 and len(self.error_string) > 0)):
			self.str_parent += "\n\n<!-- \n"
			# Error
			if (self.loc_var["complete_log"] == 1 and len(self.complete_string) > 0):
				self.str_parent += self.complete_string + "\n"
			if (self.loc_var["error_log"] == 1 and len(self.error_string) > 0):
				self.str_parent += self.error_string + "\n"
			self.str_parent += "\n-->\n"
		return self.str_parent

# ===================================================================================

	def generate_array(self):
		self.str_parent = etree.tostring(self.xml_parent, pretty_print=True)
		return self.str_parent, self.complete_string, self.error_string, self.debug_string

# ========================================================================================

	def reset_variables(self):

		# Canvas Variables
		self.loc_var["xmin"] = self.loc_var["defaultxmin"]
		self.loc_var["xmax"] = self.loc_var["defaultxmax"]
		self.loc_var["ymin"] = self.loc_var["defaultymin"]
		self.loc_var["ymax"] = self.loc_var["defaultymax"]
		self.loc_var["xscl"] = self.loc_var["defaultxscl"]
		self.loc_var["yscl"] = self.loc_var["defaultyscl"]
		self.loc_var["xgrid"] = self.loc_var["defaultxgrid"]
		self.loc_var["ygrid"] = self.loc_var["defaultygrid"]
		self.loc_var["xtick"] = self.loc_var["defaultxtick"]
		self.loc_var["ytick"] = self.loc_var["defaultytick"]
		self.loc_var["border"] = self.loc_var["defaultborder"]
		self.loc_var["height"] = self.loc_var["defaultheight"]
		self.loc_var["width"] = self.loc_var["defaultwidth"]
		self.loc_var["xunitlength"] = self.loc_var["defaultxunitlength"]
		self.loc_var["yunitlength"] = self.loc_var["defaultyunitlength"]
		self.loc_var["origin"] = self.loc_var["defaultorigin"]

		# Element Variables
		self.loc_var["axesstroke"] = self.loc_var["defaultaxesstroke"]
		self.loc_var["gridstroke"] = self.loc_var["defaultgridstroke"]
		self.loc_var["strokewidth"] = self.loc_var["defaultstrokewidth"]			
		self.loc_var["strokedasharray"] = self.loc_var["defaultstrokedasharray"]
		self.loc_var["stroke"] = self.loc_var["defaultstroke"]
		self.loc_var["arrowfill"] = self.loc_var["defaultarrowfill"]
		self.loc_var["fill"] = self.loc_var["defaultfill"]
		self.loc_var["fontstyle"] = self.loc_var["defaultfontstyle"]
		self.loc_var["fontfamily"] = self.loc_var["defaultfontfamily"]
		self.loc_var["fontsize"] = self.loc_var["defaultfontsize"]
		self.loc_var["fontweight"] = self.loc_var["defaultfontweight"]
		self.loc_var["fontstroke"] = self.loc_var["defaultfontstroke"]
		self.loc_var["fontfill"] = self.loc_var["defaultfontfill"]
		self.loc_var["markerstrokewidth"] = self.loc_var["defaultmarkerstrokewidth"]
		self.loc_var["markerstroke"] = self.loc_var["defaultmarkerstroke"]
		self.loc_var["markerfill"] = self.loc_var["defaultmarkerfill"]
		self.loc_var["markersize"] = self.loc_var["defaultmarkersize"]
		self.loc_var["marker"] = self.loc_var["defaultmarker"]
		self.loc_var["dotradius"] = self.loc_var["defaultdotradius"]
		self.loc_var["ticklength"] = self.loc_var["defaultticklength"]

		self.xml_parent = None
		self.xml_pointer = -1 						# !!! Important !!!
		self.xml_parent_pointer = list() 	# !!! Important !!!

# ========================================================================================

	def frange(self, start, end, leap):
		result = []
		current = start
		if (leap > 0 and end > start):
			while (current <= end):
				result.append(round(current,3))
				current += leap
			return result
		elif (leap < 0 and end < start):
			while (current >= end):
				result.append(round(current,3))
				current += leap
			return result
		else:
			return []

# ========================================================================================

	def jrange(self, start_cond=None, end_cond=None, leap_cond=None):

		# ONLY run during EXEC (not pre-processing)

		# Variables
		i_character = re.findall(r'\w', start_cond)[0]		# Find most common character (usually i)
		self.loc_var['jrange_counter'] = 0
		self.loc_var['jrange_result'] = []

		# Formatting
		leap_cond = leap_cond.replace("++", "+=1")		# Replace ++ notation
		leap_cond = leap_cond.replace("--", "-=1")		# Replace -- notation

		# Loop
		exec(start_cond, None, self.loc_var)
		exec("while(" + end_cond + " and jrange_counter < 1000): jrange_result.append(round("+i_character+",3)); jrange_counter+=1; "+leap_cond, None, self.loc_var)
		
		# Force integer values if possible
		for i in range (0,len(self.loc_var['jrange_result'])):
			if (int(self.loc_var['jrange_result'][i]) == self.loc_var['jrange_result'][i]):
				self.loc_var['jrange_result'][i] = int(self.loc_var['jrange_result'][i])

		return self.loc_var['jrange_result']

# ========================================================================================


	def initPicture(self,a=None,b=None,c=None,d=None):

		# Set Variables
		self.loc_var["xmin"] = (a == None and self.loc_var["xmin"] or a)
		self.loc_var["xmax"] = (b == None and self.loc_var["xmax"] or b)
		self.loc_var["ymin"] = (c == None and self.loc_var["ymin"] or c)
		self.loc_var["ymax"] = (d == None and self.loc_var["ymax"] or d)

		# Re-calculate variables
		self.loc_var["xunitlength"] = float(float(self.loc_var["width"])-2*self.loc_var["border"])/(self.loc_var["xmax"]-self.loc_var["xmin"])
		self.loc_var["yunitlength"] = float(float(self.loc_var["height"])-2*self.loc_var["border"])/(self.loc_var["ymax"]-self.loc_var["ymin"])
		self.loc_var["origin"] = [-self.loc_var["xmin"]*self.loc_var["xunitlength"]+self.loc_var["border"],-self.loc_var["ymin"]*self.loc_var["yunitlength"]+self.loc_var["border"]]

		# Set Attributes
		self.xml_parent.attrib['style'] = "display:inline"
		self.xml_parent.attrib['width'] = str(float(self.loc_var["width"]))
		self.xml_parent.attrib['height'] = str(float(self.loc_var["height"]))
		self.xml_parent.attrib['xmin'] = str(self.loc_var["xmin"])
		self.xml_parent.attrib['xmax'] = str(self.loc_var["xmax"])
		self.xml_parent.attrib['ymin'] = str(self.loc_var["ymin"])
		self.xml_parent.attrib['ymax'] = str(self.loc_var["ymax"])
		self.xml_parent.attrib['ox'] = str(self.loc_var["origin"][0])
		self.xml_parent.attrib['oy'] = str(self.loc_var["origin"][1])
		self.noaxes()

# ========================================================================================

	def setBorder(self,x=0,color="black"):

		if (x != None):
			self.loc_var["border"] = x
		if (color != None):
			self.loc_var["stroke"] = color

# ========================================================================================

	'''
	==============================
	Functions (GROUPING)
	==============================
	> xml_get_pointer()
	> start_group(center=[0,0], angle=0, scale=[1,1], translate=[0,0])
	> stop_group()
	============================== 
	'''

# ========================================================================================

	def dprint(self, string):
		self.debug_string += str(string) + "\n"

# ========================================================================================

	def xml_get_pointer(self):
		if (len(self.xml_parent_pointer) > 0):
			var_parent = "][".join([str(i) for i in self.xml_parent_pointer])
			return "self.xml_parent[" + var_parent + "]" # + var_current
		else:
			return "self.xml_parent"  # + var_current

# ========================================================================================

	def start_group(self, center=[0,0], rotate_angle=0, scale=[1,1], translate=[0,0]):

		# Initialize variables
		if (center == None): center=[0,0]
		if (rotate_angle == None): rotate_angle=0
		if (scale == None): scale=[1,1]
		if (translate == None): translate=[0,0]

		# Create group based on pointer
		exec("node = etree.SubElement(" + str(self.xml_get_pointer()) + ", 'g')")
		node.attrib['parent'] = str(self.xml_get_pointer())

		# Change pointer to new parent
		exec("self.xml_parent_pointer.append(len(" + str(self.xml_get_pointer()) + ".getchildren())-1)")
		node.attrib['self'] = str(self.xml_get_pointer())

		# Group attributes
		node.attrib['angle'] = str(-rotate_angle)
		node.attrib['scale_x'] = str(scale[0])
		node.attrib['scale_y'] = str(scale[1])
		cx = round(center[0] * self.loc_var["xunitlength"] + self.loc_var["origin"][0],2)
		cy = round(float(self.loc_var["height"]) - center[1] * self.loc_var["yunitlength"] - self.loc_var["origin"][1],2)
		tx = round(translate[0] * self.loc_var["xunitlength"],2)
		ty = round(translate[1] * self.loc_var["yunitlength"],2)
		sx = scale[0]
		sy = scale[1] != None and scale[1] or sx
		
		# Rotate
		transform_string = "rotate("+str(node.attrib['angle'])+", "+str(cx)+", "+str(cy)+") "
		
		# Scale (transform + scale + reverse transform)
		transform_string += "translate("+str(cx)+", "+str(cy)+") "
		transform_string += "scale("+str(sx)+", "+str(sy)+")"
		transform_string += "translate("+str(-cx)+", "+str(-cy)+") "

		# Translate
		transform_string += "translate("+str(tx/sx)+", "+str(-1*ty/sy)+")"
		node.attrib['transform'] = transform_string

# ========================================================================================	

	def stop_group(self):
		if (len(self.xml_parent_pointer) > 0):
			self.xml_parent_pointer.pop(-1)
			
# ========================================================================================

	'''
	==============================
	Functions (BASIC SVG ELEMENTS)
	==============================
	> myCreateElementSVG(t)
	> dot(center, typ, label, pos)
	> arrowhead(p,q)
	> text(p,st,pos,angle)
	============================== 
	'''

# ========================================================================================

	def dot(self, center=[0,0], typ=None, label=None, pos=None, angle=None):

		cx = center[0] * self.loc_var["xunitlength"] + self.loc_var["origin"][0]
		cy = float(self.loc_var["height"]) - center[1] * self.loc_var["yunitlength"] - self.loc_var["origin"][1]

		# If the Type is Defined
		if (typ == "+" or typ == "-" or typ == "|"):
			exec("node = etree.SubElement(" + str(self.xml_get_pointer()) + ", 'path')")
			if (typ=="+"):					
				node.attrib['d'] = 	" M " + str(cx - self.loc_var["ticklength"]) + " " + str(cy) + \
														" L " + str(cx + self.loc_var["ticklength"]) + " " + str(cy) + \
														" M " + str(cx) + " " + str(cy - self.loc_var["ticklength"]) + \
														" L " + str(cx) + " " + str(cy + self.loc_var["ticklength"])
				node.attrib['stroke-width'] = str(0.5)
				node.attrib['stroke'] = str(self.loc_var["axesstroke"])
			elif (typ=="-"):
				node.attrib['d'] = 	" M " + str(cx - self.loc_var["ticklength"]) + " " + str(cy) + \
														" L " + str(cx + self.loc_var["ticklength"]) + " " + str(cy)
			elif (typ=="|"):
				node.attrib['d'] = 	" M " + str(cx) + " " + str(cy - self.loc_var["ticklength"]) + \
														" L " + str(cx) + " " + str(cy + self.loc_var["ticklength"])
				node.attrib['stroke-width'] = str(self.loc_var["strokewidth"])
				node.attrib['stroke'] = str(self.loc_var["stroke"])

		# Type NOT Defined
		else:
			exec("node = etree.SubElement(" + str(self.xml_get_pointer()) + ", 'circle')")
			node.attrib['cx'] = str(cx)
			node.attrib['cy'] = str(cy)
			node.attrib['r'] = str(self.loc_var["dotradius"])
			node.attrib['stroke-width'] = str(self.loc_var["strokewidth"])
			node.attrib['stroke'] = str(self.loc_var["stroke"])
			node.attrib['fill'] = str(typ == "open" and "white" or self.loc_var["stroke"])

		# Label
		if (label != None):
			self.text(center,label,(pos == None and "below" or pos), (angle == None and 0 or angle))

# ========================================================================================
	
	def arrowhead(self,p=[0,0],q=[1,1],size=1):

		v = [p[0]*self.loc_var["xunitlength"]+self.loc_var["origin"][0],float(self.loc_var["height"])-p[1]*self.loc_var["yunitlength"]-self.loc_var["origin"][1]]		# adjusted start point
		w = [q[0]*self.loc_var["xunitlength"]+self.loc_var["origin"][0],float(self.loc_var["height"])-q[1]*self.loc_var["yunitlength"]-self.loc_var["origin"][1]]		# adjusted end point
		u = [w[0]-v[0],w[1]-v[1]] # unit vector * length
		d = math.sqrt(u[0]*u[0]+u[1]*u[1]) #length of unit vector
		if (d > 0.000001):
			u = [u[0]/d, u[1]/d]	# unit vector
			up = [-u[1],u[0]] 		# inverse unit vector
			exec("node = etree.SubElement(" + str(self.xml_get_pointer()) + ", 'path')")
			node.attrib['d'] = str("M " + str(w[0]-(size+15)*u[0]-5*up[0]) + " " + str(w[1]-(size+15)*u[1]-5*up[1]) + " L " + str(w[0]-(size*1.25-1)*u[0]) + " " + str(w[1]-(size*1.25-1)*u[1]) + " L " + str(w[0]-(size+15)*u[0]+5*up[0]) + " " + str(w[1]-(size+15)*u[1]+5*up[1]) + " Z")
			node.attrib['stroke-width'] = str(size != None and size or self.loc_var["markerstrokewidth"])
			node.attrib['stroke'] = self.loc_var["stroke"]
			node.attrib['fill'] = self.loc_var["stroke"]

# ========================================================================================

	def text(self,p=[0,0],st=None,pos=None,angle=None):

		# Default text positions
		textanchor = "middle"
		dx = 0
		dy = int(float(self.loc_var["fontsize"]))/3
		if (angle == None):
			angle = 0

		# Text Positions
		if (pos == self.loc_var["aboveleft"]):	
			dx = -int(float(self.loc_var["fontsize"]))/2 	
			dy = -int(float(self.loc_var["fontsize"]))/2		
			textanchor = "end"
		if (pos == self.loc_var["above"]):
			dx = 0 														
			dy = -int(float(self.loc_var["fontsize"]))/2		
			textanchor = "middle"
		if (pos == self.loc_var["aboveright"]):
			dx = int(float(self.loc_var["fontsize"]))/2 	
			dy = -int(float(self.loc_var["fontsize"]))/2		
			textanchor = "start"
		if (pos == self.loc_var["left"]):
			dx = -int(float(self.loc_var["fontsize"]))/2 	
			dy = int(float(self.loc_var["fontsize"]))/3			
			textanchor = "end"
		if (pos == self.loc_var["right"]):
			dx = int(float(self.loc_var["fontsize"]))/2 	
			dy = int(float(self.loc_var["fontsize"]))/3			
			textanchor = "start"
		if (pos == self.loc_var["belowleft"]):
			dx = -int(float(self.loc_var["fontsize"]))/2 	
			dy = int(float(self.loc_var["fontsize"]))				
			textanchor = "end"
		if (pos == self.loc_var["below"]):
			dx = 0 														
			dy = int(float(self.loc_var["fontsize"]))				
			textanchor = "middle"
		if (pos == self.loc_var["belowright"]):
			dx = int(float(self.loc_var["fontsize"]))/2 	
			dy = int(float(self.loc_var["fontsize"]))				
			textanchor = "start"
		
		# Text Rotation (Using old append method -- UNICODE compatability)
		node = etree.fromstring("<text>" + str(st) + "</text>")
		exec(str(self.xml_get_pointer()) + ".append(node)")

		# Remove angle for EACH parent
		adjusted_angle = int(angle)
		adjusted_scale_x = 1;
		adjusted_scale_y = 1;
		str_transform = "";

		# Properties
		node.attrib['x'] = str(round(p[0] * self.loc_var["xunitlength"] + self.loc_var["origin"][0] + dx,2))		
		node.attrib['y'] = str(round(float(self.loc_var["height"]) - p[1] * self.loc_var["yunitlength"] - self.loc_var["origin"][1]+dy,2))

		for k in range (0,len(self.xml_parent_pointer)):
			var_parent = "[" + "][".join([str(i) for i in self.xml_parent_pointer[0:k+1]]) + "]"
			
			# Reverse Angle
			adjusted_angle -= float(eval("self.xml_parent" + str(var_parent) + ".attrib['angle']"))
			
			# Reverse Scale
			adjusted_scale_x = 1/float(eval("self.xml_parent" + str(var_parent) + ".attrib['scale_x']"))
			adjusted_scale_y = 1/float(eval("self.xml_parent" + str(var_parent) + ".attrib['scale_y']"))
			str_transform += "translate("+str(node.attrib['x'])+", "+str(float(node.attrib['y'])-dy)+") "
			str_transform += "scale("+str(adjusted_scale_x)+", "+str(adjusted_scale_y)+") "
			str_transform += "translate("+str(-1*float(node.attrib['x']))+", "+str(-1*(float(node.attrib['y'])-dy))+") "

		# Properties
		str_transform += "rotate("+str(adjusted_angle)+", "+str(float(node.attrib['x'])-dx)+", "+str(float(node.attrib['y'])-dy)+") "
		node.attrib['transform'] = str_transform
		node.attrib['font-style'] = str(self.loc_var["fontstyle"])
		node.attrib['font-family'] = str(self.loc_var["fontfamily"])
		node.attrib['font-size'] = str(self.loc_var["fontsize"])
		node.attrib['font-weight'] = str(self.loc_var["fontweight"])
		node.attrib['text-anchor'] = str(textanchor)
		node.attrib['stroke'] = str(self.loc_var["fontstroke"])
		node.attrib['fill'] = str(self.loc_var["fontfill"])

# ========================================================================================
	
	'''
	
	==============================
	Functions (COMPOUND SVG ELEMENTS)
	==============================
	> line(p,q)
	> ellipse(center,rx,ry)
	> circle(center,radius)
	> arc(start,end,radius)
	============================== 

	'''
	
# ========================================================================================
	
	def line(self,p,q):

		exec("node = etree.SubElement(" + str(self.xml_get_pointer()) + ", 'path')")

		# Formatting
		if (self.loc_var["strokedasharray"] == None):
			self.loc_var["strokedasharray"] = [1,0]
		if (isinstance(self.loc_var["strokedasharray"], str)):
			try:
				self.loc_var["strokedasharray"] = eval("[" + self.loc_var["strokedasharray"] + "]")
			except:
				self.loc_var["strokedasharray"] = [1,0]

		# Attributes
		node.attrib['d'] = 	str(	" M " + \
			str(round(p[0] * self.loc_var["xunitlength"] + self.loc_var["origin"][0],2)) + \
			"," + \
			str(round(float(self.loc_var["height"]) - p[1] * self.loc_var["yunitlength"] - self.loc_var["origin"][1],2)) + \
			" "+ \
			str(round(q[0] * self.loc_var["xunitlength"] + self.loc_var["origin"][0],2)) + \
			"," + \
			str(round(float(self.loc_var["height"]) - q[1] * self.loc_var["yunitlength"] - self.loc_var["origin"][1],2)))
		node.attrib['stroke-width'] = str(self.loc_var["strokewidth"])
		node.attrib['stroke'] = str(self.loc_var["stroke"])
		node.attrib['fill'] = str(self.loc_var["fill"])
		node.attrib['stroke-dasharray'] = str(self.loc_var["strokedasharray"][0]) + ", " + \
																			str(self.loc_var["strokedasharray"][1])
		# starting point (p)
		if (self.loc_var["marker"] == "dot" or self.loc_var["marker"] == "arrowdot"):
			self.dot(p)

		# ending point (q) 
		if (self.loc_var["marker"] == "arrowdot" or self.loc_var["marker"] == "arrow"):	
			self.arrowhead(p,q,self.loc_var["markersize"])
		if (self.loc_var["marker"] == "dot"):
			self.dot(q)

# ========================================================================================

	def ellipse(self, center=[0,0], rx=1, ry=None):

		exec("node = etree.SubElement(" + str(self.xml_get_pointer()) + ", 'ellipse')")
		node.attrib['cx'] = str(round(center[0] * self.loc_var["xunitlength"] + self.loc_var["origin"][0],2))
		node.attrib['cy'] = str(round(float(self.loc_var["height"]) - center[1] * self.loc_var["yunitlength"] - self.loc_var["origin"][1],2))
		node.attrib['rx'] = str(round(rx * self.loc_var["xunitlength"],2))
		node.attrib['ry'] = (ry != None and (str(round(ry * self.loc_var["yunitlength"],2))) or node.attrib['rx'])
		node.attrib['stroke-width'] = str(self.loc_var["strokewidth"])
		node.attrib['stroke-dasharray'] = str(self.loc_var["strokedasharray"][0]) + ", " + \
																			str(self.loc_var["strokedasharray"][1])
		node.attrib['stroke'] = str(self.loc_var["stroke"])
		node.attrib['fill'] = str(self.loc_var["fill"])

# ========================================================================================

	def circle(self,center=[0,0],radius=1):
		self.ellipse(center,radius,radius)

# ========================================================================================

	def arc(self,start=[0,0],end=[1,1],radius=None):
		
		exec("node = etree.SubElement(" + str(self.xml_get_pointer()) + ", 'path')")
		
		# Radius
		if (radius==None):  
			vector = [end[0]-start[0],end[1]-start[1]]
			radius = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])

		# Draw Arc
		node.attrib['d'] = 	" M " +	\
			str(start[0] * self.loc_var["xunitlength"] + self.loc_var["origin"][0]) + "," + \
			str(float(self.loc_var["height"]) - start[1] * self.loc_var["yunitlength"] - self.loc_var["origin"][1]) + \
			" A " + \
			str(radius * self.loc_var["xunitlength"]) + "," + \
			str(radius * self.loc_var["yunitlength"]) + " 0 0,0 " + \
			str(end[0] * self.loc_var["xunitlength"] + self.loc_var["origin"][0]) + "," + \
			str(float(self.loc_var["height"]) - end[1] * self.loc_var["yunitlength"] - self.loc_var["origin"][1])
		node.attrib['stroke-width'] = str(self.loc_var["strokewidth"])
		node.attrib['stroke'] = str(self.loc_var["stroke"])
		node.attrib['fill'] = str(self.loc_var["fill"])

		# Markers

		sign_rad = ((end[1]-start[1]) >= 0 and -1 or 1)
		len_m = math.sqrt((end[0]-start[0])*(end[0]-start[0]) + (end[1]-start[1])*(end[1]-start[1]))/2
		radius = max(radius,len_m)

		if ((end[0]-start[0]) == 0): grad = 100000; inv_grad = 0
		elif ((end[1]-start[1]) == 0): grad = 0; inv_grad = 100000
		else: grad = (end[1]-start[1])/(end[0]-start[0]); inv_grad = -1/grad

		xm = start[0] + (end[0]-start[0])/2
		ym = start[1] + (end[1]-start[1])/2
		distance = sign_rad * math.sqrt(radius*radius - len_m*len_m)
		xc = xm + distance*math.cos(math.atan(inv_grad))
		yc = ym + distance*math.sin(math.atan(inv_grad))
		tangent = [end[0]-(yc-end[1]),end[1]+(xc-end[0])]

		if (self.loc_var["marker"] == "dot"):
			self.dot(start)
			self.dot(end)
		if (self.loc_var["marker"] == "arrowdot"):
			self.dot(start) 
			self.arrowhead(tangent,end)
		if (self.loc_var["marker"] == "arrow"):
			self.arrowhead(tangent,end)

# ========================================================================================

	'''

	==============================
	Functions (COMPLEX SVG ELEMENTS)
	==============================
	> noaxes()
	> axes(dx,dy,labels,gdx,gdy)
	> grid(dx,dy)
	> rect(p,q,rx,ry)
	> path(plist,c)
	> plot(fun,x_min,x_max,points)
	> curve(plist)
	> bunnyhop(plist)
	> smoothcurve(plist)
	> petal(p,d)
	> heart(p,size)
	> slopefield(fun,dx,dy)
	============================== 

	'''

# ========================================================================================

	def noaxes(self):

		# Initialize blank background
		exec("node = etree.SubElement(" + str(self.xml_get_pointer()) + ", 'rect')")
		node.attrib['x'] = "0"
		node.attrib['y'] = "0"
		node.attrib['width'] = str(float(self.loc_var["width"]))
		node.attrib['height'] = str(float(self.loc_var["height"]))
		node.attrib['stroke-width'] = str(self.loc_var["border"])
		node.attrib['stroke'] = str(self.loc_var["stroke"])
		node.attrib['fill'] = "white"

# ========================================================================================

	def axes(self,dx=None,dy=None,labels=None,gdx=None,gdy=None,units=None):

		if (dx != None and dx <= 0): dx = 1
		if (dy != None and dy <= 0): dy = 1
		if (gdx != None and gdx <= 0): gdx = 1
		if (gdy != None and gdy <= 0): gdy = 1
		if (gdx != None and gdy == None): gdy = gdx

		tdx = (dx != None and dx*self.loc_var["xunitlength"] or self.loc_var["xunitlength"])
		tdy = (dy != None and dy*self.loc_var["yunitlength"] or self.loc_var["yunitlength"])
		self.loc_var["fontsize"] = min(tdx/2,tdy/2,16)
		ticklength = int(float(self.loc_var["fontsize"]))/4
		string = ""

		# Grid
		if (gdx != None or gdy != None):

			if (gdx != None):

				gdx = gdx*self.loc_var["xunitlength"]
				for i in self.frange(self.loc_var["origin"][0], float(self.loc_var["width"]), gdx):
					string += " M " + str(i) + ",0 " + str(i) + "," + str(float(self.loc_var["height"])) # x-axis (positive)
				for i in self.frange(self.loc_var["origin"][0], 0, -gdx):
					string += " M " + str(i) + ",0 " + str(i) + "," + str(float(self.loc_var["height"])) # x-axis (negative)

			if (gdy != None):

				gdy = gdy*self.loc_var["yunitlength"]
				for i in self.frange((float(self.loc_var["height"]) - self.loc_var["origin"][1]), float(self.loc_var["height"]), gdy):
					string += " M 0," + str(i) + " " + str(float(self.loc_var["width"])) + "," + str(i) # y-axis (positive)
				for i in self.frange((float(self.loc_var["height"]) - self.loc_var["origin"][1]), 0, -gdy):
					string += " M 0," + str(i) + " " + str(float(self.loc_var["width"])) + "," + str(i) # y-axis (negative)

			# Create SVG Element
			exec("pnode = etree.SubElement(" + str(self.xml_get_pointer()) + ", 'path')")
			pnode.attrib['d'] = str(string)
			pnode.attrib['stroke-width'] = str(0.5)
			pnode.attrib['stroke'] = str(self.loc_var["gridstroke"])
			pnode.attrib['fill'] = str(self.loc_var["fill"])

		if (dx != None or dy != None):

			# Thicker Axes lines
			string = " M 0," + str(float(self.loc_var["height"])-self.loc_var["origin"][1]) + \
			" " + str(float(self.loc_var["width"])) + "," + str(float(self.loc_var["height"])-self.loc_var["origin"][1]) + \
			" M " + str(self.loc_var["origin"][0]) + ",0 " + \
			str(self.loc_var["origin"][0]) + "," + str(float(self.loc_var["height"]))

			# Ticks
			if (dx != None):

				for i in self.frange(self.loc_var["origin"][0], float(self.loc_var["width"]), tdx): 
					string += " M " + str(i) + \
					"," + str(float(self.loc_var["height"]) - self.loc_var["origin"][1] + self.loc_var["ticklength"]) + " " + \
					str(i) + "," + \
					str(float(self.loc_var["height"])-self.loc_var["origin"][1]-self.loc_var["ticklength"]) # x-axis (positive)
		
				for i in self.frange(self.loc_var["origin"][0], 0, -tdx):
					string += " M " + str(i) + \
					"," + str(float(self.loc_var["height"]) - self.loc_var["origin"][1] + self.loc_var["ticklength"]) + " " + \
					str(i) + "," + \
					str(float(self.loc_var["height"])-self.loc_var["origin"][1]-self.loc_var["ticklength"]) # x-axis (positive)
			
			if (dy != None):

				for i in self.frange((float(self.loc_var["height"]) - self.loc_var["origin"][1]), float(self.loc_var["height"]), tdy):
					string += " M " + str(self.loc_var["origin"][0] + self.loc_var["ticklength"]) + \
					"," + str(i) + " " + \
					str(self.loc_var["origin"][0] - self.loc_var["ticklength"]) + "," + str(i) # y-axis (positive)

				for i in self.frange((float(self.loc_var["height"]) - self.loc_var["origin"][1]), 0, -tdy): 
					string += " M " + str(self.loc_var["origin"][0] + self.loc_var["ticklength"]) + \
					"," + str(i) + " " + \
					str(self.loc_var["origin"][0] - self.loc_var["ticklength"]) + "," + str(i) # y-axis (negative)
		
			# Axes
			exec("pnode = etree.SubElement(" + str(self.xml_get_pointer()) + ", 'path')")
			pnode.attrib['d'] = str(string)
			pnode.attrib['stroke-width'] = str(0.5)
			pnode.attrib['stroke'] = str(self.loc_var["axesstroke"])
			pnode.attrib['fill'] = str(self.loc_var["fill"])

		# Units
		xunits = ""
		yunits = ""
		if (isinstance(units, list)):
			if (len(units) > 0):
				xunits = units[0]
			if (len(units) > 1):
				yunits = units[1]

		# Labels
		if (labels!=None):
			if (isinstance(labels, list)):
				if(len(labels) > 0):
					if(labels[0] == 1):
						for i in self.frange(dx, self.loc_var["xmax"], dx):
							self.text([i,0],str(int(i)) + str(xunits),"below") # x-axis (positive)
				if(len(labels) > 1):
					if(labels[1] == 1):
						for i in self.frange(-dx, self.loc_var["xmin"], -dx):
							self.text([i,0],str(int(i)) + str(xunits),"below") # x-axis (positive)
				if(len(labels) > 2):
					if(labels[2] == 1):
						for i in self.frange(dy, self.loc_var["ymax"], dy):
							self.text([0,i],str(int(i)) + str(yunits),"left") # y-axis (positive)
				if(len(labels) > 3):
					if(labels[3] == 1):
						for i in self.frange(-dy, self.loc_var["ymin"], -dy): 
							self.text([0,i],str(int(i)) + str(yunits),"left") # y-axis (negative)
				if(len(labels) > 4):
					if(labels[4] != None):
						self.text([0,0],0,labels[4]) # origin

			else:
				# Labels
				for i in self.frange(dx, self.loc_var["xmax"], dx):
					self.text([i,0],str(int(i)) + str(xunits),"below") # x-axis (positive)
				for i in self.frange(-dx, self.loc_var["xmin"], -dx):
					self.text([i,0],str(int(i)) + str(xunits),"below") # x-axis (positive)
				for i in self.frange(dy, self.loc_var["ymax"], dy):
					self.text([0,i],str(int(i)) + str(yunits),"left") # y-axis (positive)
				for i in self.frange(-dy, self.loc_var["ymin"], -dy): 
					self.text([0,i],str(int(i)) + str(yunits),"left") # y-axis (negative)
				self.text([0,0],0,"belowleft") # origin

# ========================================================================================

	def grid(self,dx=1,dy=1):
		self.axes(None,None,None,dx,dy)

# ========================================================================================

	def rect(self,p=[0,0],q=[1,1],rx=0,ry=0):
		exec("node = etree.SubElement(" + str(self.xml_get_pointer()) + ", 'rect')")
		node.attrib['x'] = str(p[0]*self.loc_var["xunitlength"]+self.loc_var["origin"][0])
		node.attrib['y'] = str(float(self.loc_var["height"])-q[1]*self.loc_var["yunitlength"]-self.loc_var["origin"][1])
		node.attrib['width'] = str((q[0]-p[0])*self.loc_var["xunitlength"])
		node.attrib['height'] = str((q[1]-p[1])*self.loc_var["yunitlength"])
		node.attrib['stroke-width'] = str(self.loc_var["strokewidth"])
		node.attrib['stroke'] = str(self.loc_var["stroke"])
		node.attrib['fill'] = str(self.loc_var["fill"])
		node.attrib['rx'] = str(round(rx*self.loc_var["xunitlength"],2))
		node.attrib['ry'] = str(round(ry*self.loc_var["yunitlength"],2))

# ========================================================================================

	def path(self,plist=[[0,0]],style=None,closed=None):
	
		# =================================================================================================
		# Source:													http:#www.w3schools.com/svg/svg_path.asp
		# Line:														M 0 0 L 100 100 200 0 ... 														(any number)	
		# Curve:													M 0 0 C {100 100 200 0 300 100} 											(only 3)
		# Smooth Curve: 									M 0 0 S {50 50 100 0} {150 50 200 0} {250 50 300 0}" 	(in pairs)
		# Quadratic Bezier curve: 				M 0 0 Q {50 50 100 0} {150 50 200 0} {250 50 300 0}" 	(in pairs)
		# Smooth quadratic Bezier curve:	M 0 0 T 50 50 100 0 150 50 200 0 250 50 300 0" 				(any number)
		# Close Loop:											M 0 0 ............... Z	
		# Eliptical Curve:								Complex!
		# =================================================================================================

		# Style default = L
		if (style == None):
			style = "L"
	
		# Move Command
		string = " M " + \
		str(round(plist[0][0] * self.loc_var["xunitlength"] + self.loc_var["origin"][0],2)) + "," + \
		str(round(float(self.loc_var["height"]) - plist[0][1]*self.loc_var["yunitlength"] - self.loc_var["origin"][1],2))
	
		# Draw the line
		if (style == "L" or style == "C" or style == "S" or style == "Q" or style == "T"):
			string += " " + str(style) + " "
			for i in range (1, len(plist)):
				string += str(round(plist[i][0] * self.loc_var["xunitlength"] + self.loc_var["origin"][0],2)) + "," + \
				str(round(float(self.loc_var["height"]) - plist[i][1] * self.loc_var["yunitlength"] - self.loc_var["origin"][1],2)) + " "

		# Close the Path
		if (closed != None):
			string += " Z"
		exec("node = etree.SubElement(" + str(self.xml_get_pointer()) + ", 'path')")
		node.attrib['d'] = str(string)
		node.attrib['stroke-width'] = str(self.loc_var["strokewidth"])
		node.attrib['stroke-dasharray'] = 	str(self.loc_var["strokedasharray"][0]) + ", " + \
																				str(self.loc_var["strokedasharray"][1])
		node.attrib['stroke'] = str(self.loc_var["stroke"])
		node.attrib['fill'] = str(self.loc_var["fill"])

		# Dots
		if (self.loc_var["marker"] == "dot" or self.loc_var["marker"] == "arrowdot"):
			for i in range (1, len(plist)):
				self.dot(plist[i])

# ========================================================================================

	def plot(self,func="sin(x)",x_min=None,x_max=None,points=200):

		x_min = (x_min == None and self.loc_var["xmin"] or x_min)
		x_max = (x_max == None and self.loc_var["xmax"] or x_max)
		if (x_max <= x_min):
			x_max = x_min + 5
		array_points = []

		# plot ("sin(x)") 
		if (isinstance(func, str)):
			# Precautionary string formatting
			func = func.replace("x", "t")
			#Exec
			exec ("def f_func(t): return (t)", self.loc_var, self.loc_var)							# Note: Global Scope used here!
			exec ("def g_func(t): return (" + func + ")", self.loc_var, self.loc_var)		# Note: Global Scope used here!

		# plot (["t", "sin(t)"])
		elif (isinstance(func, list)):
			#Exec
			exec("def f_func(t): return (" + func[0] + ")", self.loc_var, self.loc_var)	# Note: Global Scope used here!
			exec("def g_func(t): return (" + func[1] + ")", self.loc_var, self.loc_var)	# Note: Global Scope used here!

		# Number of points
		inc = (points == None and (x_max-x_min)/points or (x_max-x_min+0.0000001)/points)

		# Fill the array_points
		for i in self.frange(x_min, x_max+0.01, inc):

			error_count = 0

			# f(x)
			try:
				exec("fout = min(max(self.loc_var['f_func'](" + str(i) + "), -10000), 10000)")	# Note: Global Scope used here!)
			except:
				error_count += 1
			
			# g(x)
			try:
				exec("gout = min(max(self.loc_var['g_func'](" + str(i) + "), -10000), 10000)")	# Note: Global Scope used here!)
			except:
				error_count += 1

			# Append
			if (error_count == 0):
				array_points.append([fout, gout])

		#	Draw Graph
		self.path(array_points)

# ========================================================================================

	def curve(self, plist):
		self.path(plist,"T")

# ========================================================================================

	def bunnyhop(self, plist): 
		self.path(plist,"Q")

# ========================================================================================

	def smoothcurve(self, plist):
		self.path(plist,"S")

# ========================================================================================

	def petal(self,p,d):
		if (d==None):
			d=[1,1]
		self.path([p,[p[0]+d[0],p[1]+d[1]],[p[0]-d[1],p[1]+d[0]],p],"C")

# ========================================================================================

	def heart(self,p,size):
		if (size==None):
			size = 1
		self.path([[p[0],p[1]], [p[0]+size,p[1]+size], [p[0],p[1]+size*1.25], [p[0],p[1]+size*0.75]], "C")
		self.path([[p[0],p[1]+size*0.75],[p[0],p[1]+size*1.25], [p[0]-size,p[1]+size], [p[0],p[1]]], "C")

# ========================================================================================

	def cloud(self,p=[0,0],size=2,humps=6):

		# Backup of original colours
		backup_fill = self.loc_var["fill"];	backup_stroke = self.loc_var["stroke"]; 

		# Cloud fill
		self.loc_var["stroke"] = backup_fill;	self.arc([p[0]+size,p[1]],[p[0]-size,p[1]],size)

		# Bottom of cloud
		self.loc_var["stroke"] = backup_stroke; self.line([p[0]-size,p[1]],[p[0]+size,p[1]])

		# Humps
		hump_array = []
		for i in range(0,humps+1):
			hump_array.append([p[0]+size*math.sin(i*math.pi/humps - math.pi/2),p[1]+size*math.cos(i*math.pi/humps - math.pi/2)])
		for i in range(1,len(hump_array)):
			self.arc(hump_array[i],hump_array[i-1],0.001)

# ========================================================================================

	def star(self,p=[0,0],size=2,points=6, inner_radius=0.5):

		# Backup of original colours
		backup_fill = self.loc_var["fill"];	backup_stroke = self.loc_var["stroke"]; 

		# Points
		point_array = []
		for i in range(0,points+1):
			point_array.append([p[0]+size*math.sin(2*i*math.pi/points - math.pi/2),p[1]+size*math.cos(2*i*math.pi/points - math.pi/2)])
			point_array.append([p[0]+inner_radius*size*math.sin(2*(i+0.5)*math.pi/points - math.pi/2),p[1]+inner_radius*size*math.cos(2*(i+0.5)*math.pi/points - math.pi/2)])
		
		# Star Fill
		self.path(point_array)

# ========================================================================================

	def grass(self,p=[0,0],size=2,leaves=3,droop = 0.6):

		# Backup of original colours
		backup_fill = self.loc_var["fill"];
		
		self.loc_var["fill"] = "none"
	
		if (leaves > 1 and leaves < 20):
			# Left / Right
			for i in [-1,1]:
				for j in range(0,leaves):
				  dot_a = [p[0],p[1]]
				  dot_b = [p[0],p[1]+size]
				  dot_c = [p[0]+size*(0.5*math.sin(j*2*math.pi/(2*(leaves-1)) - math.pi/2)),p[1]+size*((droop/2)*math.cos(j*2*math.pi/(2*(leaves-1)) - math.pi/2) + droop)]
				  self.smoothcurve([dot_a,dot_b,dot_c])

		self.loc_var["fill"] = backup_fill

# ========================================================================================

	def flower(self,p=[0,0],size=2,petals=12,center_fill="white",center_stroke="black",center_size =0.8):

		# Backup of original colours
		backup_fill = self.loc_var["fill"];	backup_stroke = self.loc_var["stroke"]; 

		# Cloud fill
		self.loc_var["stroke"] = backup_fill;	self.circle([p[0],p[1]],size)

		self.loc_var["stroke"] = backup_stroke;

		# Humps
		petal_array = []
		for i in range(0,petals+1):
			petal_array.append([p[0]+size*math.sin(i*2*math.pi/petals),p[1]+size*math.cos(i*2*math.pi/petals)])
		for i in range(1,len(petal_array)):
			self.arc(petal_array[i],petal_array[i-1],0.001)

		# Center
		self.loc_var["fill"] = center_fill;
		self.loc_var["stroke"] = center_stroke;
		self.circle([p[0],p[1]],size*center_size)

		# Restore Values
		self.loc_var["stroke"] = backup_stroke;
		self.loc_var["fill"] = backup_fill;

# ========================================================================================

	def angle_arc(self, center=[0,0], radius=1, start_deg=0, stop_deg=45, text="", text_offset=0.25):

		# Backup of original colours
		backup_fill = self.loc_var["fill"];
		self.loc_var["fill"] = "none"

		# Calculations
		start_deg %= 360
		stop_deg %= 360
		diff = (stop_deg - start_deg) % 360
		angle_start = (math.pi/180) * start_deg
		angle_stop = (math.pi/180) * stop_deg
		
		# Drawing the arc
		if (diff > 180):
			self.arc(	[center[0] + radius*math.cos(angle_start),
									center[1] + radius*math.sin(angle_start)],
								[center[0] + radius*math.cos(angle_start + math.pi),
									center[1] + radius*math.sin(angle_start + math.pi)],radius)
			self.arc(	[center[0] + radius*math.cos(angle_start + math.pi),
									center[1] + radius*math.sin(angle_start + math.pi)],
								[center[0] + radius*math.cos(angle_stop),
									center[1] + radius*math.sin(angle_stop)],radius)
		else:
			self.arc([center[0] + radius*math.cos(angle_start),center[1] + radius*math.sin(angle_start)],[center[0] + radius*math.cos(angle_stop),center[1] + radius*math.sin(angle_stop)],radius)

		# Text
		if (angle_start > angle_stop):
			text_angle = angle_start + ((2*math.pi+angle_stop)-angle_start)/2
		else:
			text_angle = angle_start + (angle_stop-angle_start)/2			

		text_x = center[0] + radius*math.cos(text_angle)*(1+text_offset)*int(text_angle/abs(text_angle))
		text_y = center[1] + radius*math.sin(text_angle)*(1+text_offset)*int(text_angle/abs(text_angle))
		#unit_vector_sign = int(1/abs(1)))
		self.text([text_x,text_y], str(text))

		# Restore FILL variable
		self.loc_var["fill"] = backup_fill

# ========================================================================================

	def slopefield(self,func="sin(x)",dx=None,dy=None):

		if (dx == None or dx <= 0): dx=1
		if (dy == None or dy <= 0): dy=1

		# plot ("sin(x)")
		exec ("def g(x,y): return (" + self.mathjs(func) + ")", None, self.loc_var)

		# Length of Line
		dz = math.sqrt(dx*dx+dy*dy)/6

		# Loop	
		ddx = 0.001
		for x in self.frange(self.loc_var["xmin"], self.loc_var["xmax"], dx):
		  for y in self.frange(self.loc_var["ymin"], self.loc_var["ymax"], dy):
				
				# Calculate the Instantaneous Gradient
				try:
					gout = (self.loc_var["g"](x+ddx,y) - self.loc_var["g"](x-ddx,y))/(2.0*ddx)
					error_flag = 0
				except:
					error_flag += 1		
		
				# Plot Line
				if (error_flag == 0):
					u = dz/math.sqrt(1 + gout*gout)
					v = gout * u
					self.line([round(x-u,2),round(y-v,2)],[round(x+u,2),round(y+v,2)])

# ========================================================================================
