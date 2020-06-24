#!/usr/bin/env python3

import sys
sys.path.append("./")
import importlib

try:
	_, filename = sys.argv
except:
	filename = None

entrypoint = importlib.import_module("scripts.entrypoint")
entrypoint.init(filename) #main.init()

