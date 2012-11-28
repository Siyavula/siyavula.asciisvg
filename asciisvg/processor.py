#!/usr/bin/python

from SvgCanvas import *
import cgi
import os
import cgitb; cgitb.enable()
import cairo
import rsvg
import urllib
import random

# ========================================================================================
# Functions
# ========================================================================================

def fn_strip_tags(text, templateLocals={}):

	# =======================================
	newText = ''
	stop = 0
	startSubstr = '<valueof>'
	stopSubstr = '</valueof>'
	while True:
		start = text.find(startSubstr, stop)
		if start == -1:
			newText += text[stop:]
			break
		newText += text[stop:start]
		start += len(startSubstr)
		stop = text.find(stopSubstr, start)
		eval_piece = text[start:stop].strip()
		if (len(eval_piece) > 0):
			try:
				newText += str(eval(eval_piece, templateLocals, templateLocals))
			except Exception, err:
				error_flag = 1
				error_string = "VALUEOF tags\n\n" + str(err)
				return error_flag, error_string, text
		else:
			newText += ""
		stop += len(stopSubstr)
	# =======================================

	return 0, "", newText

# ========================================================================================

def AJAX_return(output, error_flag, error_string, randomSeed, debug_string):
	print "Content-Type: text/html"
	print
	if (error_flag == 1 or len(error_string) > 0):
		print urllib.quote("[BRK]Error: " + str(error_string) + "[BRK]" + str(randomSeed) + "[BRK]" + str(debug_string))
	else:
		print urllib.quote(output + "[BRK][BRK]" + str(randomSeed) + "[BRK]" + str(debug_string))

# ========================================================================================
# INPUT
# ========================================================================================

form = cgi.FieldStorage()
error_flag = 0
error_string = ""
debug_string = ""
output = ""
templateLocals = {}
iRandomSeed=None

# Process <valueof> tags
if (form.getvalue('strip_tags') == 'true'):

	# =======================================
	# Import template environment header

	if not (iRandomSeed == None):
		randomSeed = iRandomSeed
	elif (form.getvalue('randomize_lock') == 'true'):
		randomSeed = int(form.getvalue('random_seed'))
	else:
		randomSeed = random.randint(1, 1000000)		

	# =======================================
	import template_environment
	for key in dir(template_environment):
	    if (key[:2] != '__') or (key[-2:] != '__'):
	        templateLocals[key] = template_environment.__getattribute__(key)
	templateLocals['random'] = templateLocals['randomModule'].Random(randomSeed)
	templateLocals['ENVIRONMENT'].random = templateLocals['random']
	# =======================================

	# dprint() code
	lib_code = 'debug_string_py = "";\ndef dprint(string): global debug_string_py; debug_string_py += str(string) + "\\n" \n'

	# Process Python first (in templateLocals)
	python_text = urllib.unquote(lib_code + form.getvalue('python'))
	try:
		exec("# encoding: utf-8\nfrom __future__ import division\n" + python_text + '\n', templateLocals, templateLocals)
	except Exception, err:
		error_flag = 1
		error_string = "Python code\n\n" + str(err) 

	# Process Python first (in loc_val)
	if (error_flag == 0):
		ascii_text = urllib.unquote(form.getvalue('ascii'))
		error_flag, error_string, ascii_text = fn_strip_tags(ascii_text, templateLocals)

# Process Python + ASCII tags (for standard mode)
else:
	ascii_text = urllib.unquote(form.getvalue('python') + "\n" + form.getvalue('ascii'))

# Only make changes to output if NO errors
if (error_flag == 0):

	# SVG handling (for both cases)
	my_svg = SvgCanvas("test", 400, 400) # default size of SVG
	my_svg.process_ascii_multi_line(ascii_text)
	svg_string, complete_string, error_string, debug_string = my_svg.generate_array()
	debug_string = str(templateLocals['debug_string_py']) + "--------------------------\n" + str(debug_string)
	if (len(error_string.strip()) > 0): error_string = "ASCII code\n" + error_string

	# PNG Generator
	if (form.getvalue('type') == 'png'):
		img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 400)
		ctx = cairo.Context(img)
		handler= rsvg.Handle(None, svg_string)
		handler.render_cairo(ctx)
		img.write_to_png("buffer/buffer.png")
		output = "<img src='cgi-bin/buffer/buffer.png'>"
	else:
		output = svg_string

# ========================================================================================
# OUTPUT
# ========================================================================================

AJAX_return(output, error_flag, error_string, randomSeed, debug_string)


