# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

import objc
from math import tan, radians
from GlyphsApp import *
from GlyphsApp.plugins import *
from AppKit import NSColor, NSBezierPath, NSPoint

class ShowExportStatus(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Export Status',
			'de': 'Export-Status',
			'es': 'estado de la exportación',
			'fr': 'état de l’export',
		})

	@objc.python_method
	def drawCross(self, xMin, xMax, yMin, yMax, lineWidth=1, italicAngle=0, halfXHeight=0):
		tangens = tan(italicAngle)
		italicBottomOffset = tangens * (yMin - halfXHeight)
		italicTopOffset = tangens * (yMax - halfXHeight)
		NSColor.redColor().set()
		cross = NSBezierPath.bezierPath()
		cross.moveToPoint_(NSPoint(xMin + italicBottomOffset, yMin))
		cross.lineToPoint_(NSPoint(xMax + italicTopOffset,    yMax))
		cross.moveToPoint_(NSPoint(xMax + italicBottomOffset, yMin))
		cross.lineToPoint_(NSPoint(xMin + italicTopOffset,    yMax))
		cross.setLineWidth_(lineWidth)
		cross.stroke()
	
	def drawFontViewForegroundForLayer_inFrame_(self, layer, frame):
		if layer.parent.export:
			return
		xMin, yMin = frame.origin.x, frame.origin.y
		xMax = xMin + frame.size.width
		yMax = yMin + frame.size.height
		self.drawCross(xMin, xMax, yMin, yMax)
	
	@objc.python_method
	def drawCrossOverLayer(self, Layer, lineWidth):
		try:
			# determine italic angle:
			try:
				thisFont = Layer.parent.parent
				thisMaster = thisFont.masters[Layer.associatedMasterId]
				italicAngle = radians(thisMaster.italicAngle) #% 90.0)
			except:
				italicAngle = 0.0
			
			# determine coordinates:
			Master = Layer.associatedFontMaster()
			halfXHeight = Master.xHeight/2.0
			yMax = Master.ascender
			xMax = Layer.width
			yMin = Master.descender
			xMin = 0
			
			# draw cross:
			self.drawCross(xMin, xMax, yMin, yMax, lineWidth=lineWidth, italicAngle=italicAngle, halfXHeight=halfXHeight)
		except Exception as e:
			self.logToConsole("drawCrossOverLayer_: %s" % str(e))

	@objc.python_method
	def background(self, Layer):
		try:
			thisGlyph = Layer.glyph()
			if thisGlyph and not thisGlyph.export:
				self.drawCrossOverLayer(Layer, 1.0 / self.getScale())
		except Exception as e:
			self.logToConsole("background: %s" % str(e))

	@objc.python_method	
	def inactiveLayerBackground(self, Layer):
		try:
			thisGlyph = Layer.glyph()
			if thisGlyph and not thisGlyph.export:
				self.drawCrossOverLayer(Layer, 1.0 / self.getScale())
		except Exception as e:
			self.logToConsole("inactiveLayer: %s" % str(e))
			
	@objc.python_method	
	def inactiveLayer(self, Layer):
		self.inactiveLayerBackground(Layer)
		# legacy method for backwards compatibility

	@objc.python_method
	def preview(self, Layer):
		try:
			thisGlyph = Layer.glyph()
			if thisGlyph and not thisGlyph.export:
				self.drawCrossOverLayer(Layer, 1.0 / self.getScale())
		except Exception as e:
			self.logToConsole("preview: %s" % str(e))

	def needsExtraMainOutlineDrawingForInactiveLayer_(self, Layer):
		return True

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
