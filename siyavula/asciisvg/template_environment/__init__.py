from __future__ import division

# Hack to make random instance of template available to modules
# imported here (so that random seed can be shared)
class X(object):
    pass
ENVIRONMENT = X()

import math
import fractions
import sympy, numpy

import constants

# Import random lists
import names
names.ENVIRONMENT = ENVIRONMENT
import colors
colors.ENVIRONMENT = ENVIRONMENT

import random as randomModule
