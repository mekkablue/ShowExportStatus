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
	def drawCross(self, xMin, xMax, yMin, yMax, lineWidth=1, italicAngle=0, halfXHeight=0, isDarkMode=False):
		tangens = tan(italicAngle)
		italicBottomOffset = tangens * (yMin - halfXHeight)
		italicTopOffset = tangens * (yMax - halfXHeight)
		if isDarkMode:
			NSColor.systemPinkColor().set() # visibility is a bit better
		else:
			NSColor.systemRedColor().set()
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
	def drawCrossOverLayer(self, layer, lineWidth, isDarkMode=False):
		try:
			master = layer.associatedFontMaster()

			# determine italic angle:
			try:
				italicAngle = radians(master.italicAngle) #% 90.0)
			except:
				italicAngle = 0.0
			
			# determine coordinates:
			halfXHeight = master.xHeight / 2.0
			yMax = master.ascender
			xMax = layer.width
			yMin = master.descender
			xMin = 0
			
			# draw cross:
			self.drawCross(xMin, xMax, yMin, yMax, lineWidth=lineWidth, italicAngle=italicAngle, halfXHeight=halfXHeight, isDarkMode=isDarkMode)
		except Exception as e:
			self.logToConsole("drawCrossOverLayer: %s" % str(e))

	@objc.python_method
	def drawCrossOverLayerInEditView(self, layer):
		glyph = layer.glyph()
		if glyph and not glyph.export:
			self.drawCrossOverLayer(
				layer,
				1.0 / self.getScale(),
				isDarkMode=self.controller.graphicView().drawDark(),
				)
	
	@objc.python_method
	def background(self, layer):
		self.drawCrossOverLayerInEditView(layer)

	@objc.python_method	
	def inactiveLayerBackground(self, layer):
		self.drawCrossOverLayerInEditView(layer)
			
	@objc.python_method	
	def inactiveLayer(self, layer):
		self.inactiveLayerBackground(Layer)
		# legacy method for backwards compatibility

	def drawBackgroundInPreviewLayer_options_(self, layer, options):
		try:
			glyph = layer.glyph()
			if glyph and not glyph.export:
				self.drawCrossOverLayer(
					layer,
					1.0 / options["Scale"],
					isDarkMode=options["Black"],
					)
		except Exception as e:
			self.logToConsole("preview: %s" % str(e))

	def needsExtraMainOutlineDrawingForInactiveLayer_(self, layer):
		return True

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
