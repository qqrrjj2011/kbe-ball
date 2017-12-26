# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import GameUtils
import random
from interfaces.EntityCommon import EntityCommon

TIMER_TYPE_ADD_TRAP = 1

class Avatar(KBEngine.Entity, EntityCommon):
	def __init__(self):
		KBEngine.Entity.__init__(self)
		EntityCommon.__init__(self)

		# 设置每秒允许的最快速度, 超速会被拉回去
		#self.topSpeed = self.moveSpeed + 0.5
		self.topSpeed = 0.0

		# 默认开始的尺寸
		self.modelRadius = 0.5

		# 默认开始大小
		self.defaultMass = self.mass

		# 随机的初始化一个出生位置
		#self.position = GameUtils.randomPosition3D(self.modelRadius)
		self.position = GameUtils.randomPosition3DByRange(100,100,0,20)
		
		# self.topSpeedY = 10.0
		self.getCurrRoom().onEnter(self)
		
		# 可视范围起始位30米，后期根据长大尺寸调整
		self.setAoiRadius(30.0, 1.0)
	 
		self.addTimer(0.1, 0, TIMER_TYPE_ADD_TRAP)
		
	def isAvatar(self):
		"""
		virtual method.
		"""
		return True
	
	def addMass(self, v):
		self.mass += v
		
		# 判断是否要升级体积
		#  所有的和别为: 毫克、克、千克、吨、万吨 
		# 到达万吨后将持续累加
		if self.level < 5:
			if self.mass > 1000:
				self.mass = 1
				self.level += 1
				self.onUpgrade()

		# 移动速度随着体重变化持续改变
		if self.moveSpeed > 0.5:
			self.moveSpeed -= (v / 100.0) * self.level
			if self.moveSpeed < 0.5:
				self.moveSpeed = 0.5

		# 模型尺寸和陷阱尺寸随之长大
		self.modelScale += (v / 10000.0) * self.level

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		引擎回调timer触发
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.className, self.id, tid, userArg))
		EntityCommon.onTimer(self, tid, userArg)

		if TIMER_TYPE_ADD_TRAP == userArg:
			self.addProximity(self.modelScale+0.2, 0, 0)

	def onUpgrade(self):
		pass
		
	def onEnterTrap(self, entityEntering, range_xz, range_y, controllerID, userarg):
		"""
		KBEngine method.
		有entity进入trap
		"""
		# 只有玩家实体进入，陷阱才工作
		if entityEntering.isDestroyed:
			return
			
		DEBUG_MSG("%s::onEnterTrap: %i entityEntering=(%s)%i, range_xz=%s, range_y=%s, controllerID=%i, userarg=%i" % \
						(self.className, self.id, entityEntering.className, entityEntering.id, \
						range_xz, range_y, controllerID, userarg))

		if entityEntering.isAvatar():
			# 如果对方体积足够被吞嚼则吞掉
			if self.mass /entityEntering.mass >=1:
				self.addMass(entityEntering.mass)
				entityEntering.destroy()

		elif entityEntering.isSmash():
			
			#玩家分裂成粮食.
			
			if self.mass > self.defaultMass * 5:
				radius = 1.0
				splitMass = self.mass - int(self.mass*0.5)
				self.addMass(-splitMass)
				room = self.getCurrRoom()
				if room:
					 
					maxSplitMass = int(splitMass * 0.5)
					minRadius = self.modelRadius * self.modelScale
					while splitMass > self.defaultMass:
						curMass = random.randint(self.defaultMass,splitMass)
						splitMass = splitMass - curMass
						self.getCurrRoom().createStartMoveFood(self.position,curMass,radius,minRadius+1,minRadius+5)
					if splitMass > 0:
						self.getCurrRoom().createStartMoveFood(self.position,splitMass,radius,minRadius+1,minRadius+5)
			
			entityEntering.destroy()
		else:
			# 吃掉粮食
			if not entityEntering.getInvincible():
				self.addMass(entityEntering.mass)
				entityEntering.destroy()

	def onLeaveTrap(self, entityLeaving, range_xz, range_y, controllerID, userarg):
		"""
		KBEngine method.
		有entity离开trap
		"""
		pass

	def onGetWitness(self):
		"""
		KBEngine method.
		绑定了一个观察者(客户端)
		"""
		DEBUG_MSG("Avatar::onGetWitness: %i." % self.id)

	def onLoseWitness(self):
		"""
		KBEngine method.
		解绑定了一个观察者(客户端)
		"""
		DEBUG_MSG("Avatar::onLoseWitness: %i." % self.id)
	
	def onDestroy(self):
		"""
		KBEngine method.
		entity销毁
		"""
		DEBUG_MSG("Avatar::onDestroy: %i." % self.id)
		room = self.getCurrRoom()
		
		if room:
			room.onLeave(self.id)
		
	def relive(self, exposed, type):
		"""
		defined.
		复活
		"""
		if exposed != self.id:
			return
			
		DEBUG_MSG("Avatar::relive: %i, type=%i." % (self.id, type))
