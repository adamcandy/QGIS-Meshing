"""
Python script for testing class ShapeData (in /scripts/input_output_for_id.py)
"""

import sys
sys.path.append("../scripts/")
import input_output_for_id

shapeData = input_output_for_id.ShapeData('data/circle',0.01,True)
print shapeData.get_shapes()

DCA_shapeData = input_output_for_id.ShapeData('data/celticDoubleAxe',0.01,False)
print shapeData.get_shapes()
