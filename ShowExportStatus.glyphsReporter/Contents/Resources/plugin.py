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

class ShowExportStatus(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Export Status',
			'de': 'Export-Status',
			'es': 'estado del exporto',
			'fr': 'stade d’export',
		})
	
	@objc.python_method
	def drawCrossOverLayer( self, Layer, lineWidth ):
		try:
			# determine italic angle:
			try:
				thisFont = Layer.parent.parent
				thisMaster = thisFont.masters[Layer.associatedMasterId]
				italicAngle = radians( thisMaster.italicAngle ) #% 90.0 )
			except:
				italicAngle = 0.0
			tangens = tan( italicAngle )
			
			# determine coordinates:
			Master = Layer.associatedFontMaster()
			halfXHeight = Master.xHeight/2.0
			yMax = Master.ascender
			xMax = Layer.width
			yMin = Master.descender
			xMin = 0
			italicBottomOffset = tangens * (yMin - halfXHeight)
			italicTopOffset = tangens * (yMax - halfXHeight)
			
			# draw cross:
			NSColor.redColor().set()
			cross = NSBezierPath.bezierPath()
			cross.moveToPoint_( NSPoint(xMin + italicBottomOffset, yMin) )
			cross.lineToPoint_( NSPoint(xMax + italicTopOffset,    yMax) )
			cross.moveToPoint_( NSPoint(xMax + italicBottomOffset, yMin) )
			cross.lineToPoint_( NSPoint(xMin + italicTopOffset,    yMax) )
			cross.setLineWidth_( lineWidth )
			cross.stroke()
		except Exception as e:
			self.logToConsole( "drawCrossOverLayer_: %s" % str(e) )

	@objc.python_method
	def background( self, Layer ):
		try:
			thisGlyph = Layer.glyph()
			if thisGlyph and not thisGlyph.export:
				self.drawCrossOverLayer(Layer, 1.0 / self.getScale())
		except Exception as e:
			self.logToConsole( "background: %s" % str(e) )

	@objc.python_method	
	def inactiveLayer(self, Layer):
		try:
			thisGlyph = Layer.glyph()
			if thisGlyph and not thisGlyph.export:
				self.drawCrossOverLayer(Layer, 1.0 / self.getScale())
		except Exception as e:
			self.logToConsole( "inactiveLayer: %s" % str(e) )

	@objc.python_method
	def preview(self, layer):
		try:
			thisGlyph = Layer.glyph()
			if thisGlyph and not thisGlyph.export:
				self.drawCrossOverLayer(Layer, 1.0 / self.getScale())
		except Exception as e:
			self.logToConsole( "preview: %s" % str(e) )

	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		return True

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
