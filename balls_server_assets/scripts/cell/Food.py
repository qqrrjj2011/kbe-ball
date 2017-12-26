# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from interfaces.EntityCommon import EntityCommon

TIMER_TYPE_MOVE = 1

class Food(KBEngine.Entity, EntityCommon):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		EntityCommon.__init__(self)
		
	def isFood(self):
		"""
		virtual method.
		"""
		return True

	def moveToPosition(self, toPos):
		self.moveToPoint(toPos,1,0,None,False,True)


	def onMove( self, controllerID, userData ):
		pass
	def onMoveOver( self, controllerID, userData ):
		self.isInvincible = False
	def onMoveFailure( self, controllerID, userData ):
		self.isInvincible = False


		
	def onDestroy(self):
		"""
		entity销毁
		"""
		room = self.getCurrRoom()
		
		if room == None:
			return
			
		room.onFoodDestroy(self.id)

