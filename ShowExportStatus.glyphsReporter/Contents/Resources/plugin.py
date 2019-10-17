# encoding: utf-8

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
import sys, os, re, math, traceback

class ShowExport(ReporterPlugin):
	
	def settings(self):
		self.menuName = "Export Status"

	def drawCrossOverLayer( self, Layer, lineWidth ):
		try:
			# determine italic angle:
			try:
				thisFont = Layer.parent.parent
				thisMaster = thisFont.masters[Layer.associatedMasterId]
				italicAngle = math.radians( thisMaster.italicAngle ) #% 90.0 )
			except:
				italicAngle = 0.0
			tangens = math.tan( italicAngle )
			
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

	def background( self, Layer ):
		try:
			if not Layer.glyph().export:
				self.drawCrossOverLayer( Layer, 1.0 / self.getScale() )
		except Exception as e:
			self.logToConsole( "drawForegroundForLayer_: %s" % str(e) )
		
	def inactiveLayer(self, Layer):
		try:
			thisGlyph = Layer.glyph()
			if thisGlyph and not thisGlyph.export:
				self.drawCrossOverLayer(Layer, 1.0 / self.getScale())
		except Exception as e:
			print traceback.format_exc()
	
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		return True

