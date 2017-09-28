# Copyright (C) 2017-2018 Digital Epics <mail@nico-miebach.de>
# This file is part of the company Digital Epics.
# This file cannot be copied and/or distributed without the express permission
# of Digital Epics.

"""
@author: Emre Tekinalp
@date: Sep 16, 2017
@contact: e.tekinalp@icloud.com
@package: core/io
@brief: input output handling
@requires: None
@version: 1.0.0
"""

__author__ = 'Emre Tekinalp'
__copyright__ = 'Copyright (C) 2017 Digital Epics'
__license__ = 'Digital Epics'
__version__ = '1.0'

# python
import os


def join_path(*args):
    """Construct and return a path by several given string values"""
    return ''.join([os.path.abspath(os.path.join(arg)) for arg in args])
