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
		"""
		Whatever you draw here will be displayed IN FRONT OF the paths.
		Setting a color:
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 1.0, 1.0, 1.0, 1.0 ).set() # sets RGBA values between 0.0 and 1.0
			NSColor.redColor().set() # predefined colors: blackColor, blueColor, brownColor, clearColor, cyanColor, darkGrayColor, grayColor, greenColor, lightGrayColor, magentaColor, orangeColor, purpleColor, redColor, whiteColor, yellowColor
		Drawing a path:
			myPath = NSBezierPath.alloc().init()  # initialize a path object myPath
			myPath.appendBezierPath_( subpath )   # add subpath to myPath
			myPath.fill()   # fill myPath with the current NSColor
			myPath.stroke() # stroke myPath with the current NSColor
		To get an NSBezierPath from a GSPath, use the bezierPath() method:
			myPath.bezierPath().fill()
		You can apply that to a full layer at once:
			if len( myLayer.paths > 0 ):
				myLayer.bezierPath()       # all closed paths
				myLayer.openBezierPath()   # all open paths
		See:
		https://developer.apple.com/library/mac/documentation/Cocoa/Reference/ApplicationKit/Classes/NSBezierPath_Class/Reference/Reference.html
		https://developer.apple.com/library/mac/documentation/cocoa/reference/applicationkit/classes/NSColor_Class/Reference/Reference.html
		"""
		try:
			if not Layer.glyph().export:
				self.drawCrossOverLayer( Layer, 1.0 / self.getScale() )
		except Exception as e:
			self.logToConsole( "drawForegroundForLayer_: %s" % str(e) )
		
	def inactiveLayers(self, Layer):
		"""
		Whatever you draw here will be displayed behind the paths, but for inactive masters.
		"""
		try:
			thisGlyph = Layer.glyph()
			if thisGlyph and not thisGlyph.export:
				self.drawCrossOverLayer(Layer, 1.0 / self.getScale())
		except Exception as e:
			print traceback.format_exc()
	
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		"""
		Decides whether inactive glyphs in Edit View and glyphs in Preview should be drawn
		by Glyphs (‘the main outline drawing’).
		Return True (or remove the method) to let Glyphs draw the main outline.
		Return False to prevent Glyphs from drawing the glyph (the main outline 
		drawing), which is probably what you want if you are drawing the glyph
		yourself in self.drawBackgroundForInactiveLayer_().
		"""
		return True

