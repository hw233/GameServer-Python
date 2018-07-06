# -*- coding: utf-8 -*-
'''寻路相关
'''
import math

class NodeElem:
	"""开放列表和关闭列表的元素类型，parent用来在成功的时候回溯路径
	"""
	def __init__(self, parent, x, y, dist):
		self.parent = parent
		self.x = x
		self.y = y
		self.dist = dist
		
class AStar:
	"""A星算法实现类
	"""
	# 注意w,h两个参数，如果你修改了地图，需要传入一个正确值或者修改这里的默认参数
	def __init__(self, mapData, srcX, srcY, destX, destY):
		self.mapData = mapData # 坐标数据, 0.阻挡   >0.有效坐标
		
		# 原x,y坐标
		self.srcX = srcX
		self.srcY = srcY
		
		# 目标x,y坐标
		self.destX = destX
		self.destY = destY
		
		# 坐标二维图的宽和高
		self.width = len(self.mapData[0])
		self.height = len(self.mapData)
		
		self.open = []
		self.close = []
		self.path = []
		
	# 查找路径的入口函数
	def findPath(self):
		# 构建开始节点
		p = NodeElem(None, self.srcX, self.srcY, 0.0)
		while True:
			# 扩展F值最小的节点
			self.extendRound(p)
			# 如果开放列表为空，则不存在路径，返回
			if not self.open:
				return
			# 获取F值最小的节点
			idx, p = self.getBest()
			# 找到路径，生成路径，返回
			if self.isTarget(p):
				self.makePath(p)
				return
			# 把此节点压入关闭列表，并从开放列表里删除
			self.close.append(p)
			del self.open[idx]
			
	def makePath(self, p):
		# 从结束点回溯到开始点，开始点的parent == None
		while p:
			self.path.append((p.x, p.y))
			p = p.parent
		
	def isTarget(self, i):
		return i.x == self.destX and i.y == self.destY
		
	def getBest(self):
		best = None
		bv = 1000000  # 如果你修改的地图很大，可能需要修改这个值
		bi = -1
		for idx, i in enumerate(self.open):
			value = self.getDist(i)  # 获取F值
			if value < bv:  # 比以前的更好，即F值更小
				best = i
				bv = value
				bi = idx
		return bi, best
		
	def getDist(self, i):
		# F = G + H
		# G 为已经走过的路径长度， H为估计还要走多远
		# 这个公式就是A*算法的精华了。
		return i.dist + math.sqrt(
			(self.destX - i.x) * (self.destX - i.x)
			+ (self.destY - i.y) * (self.destY - i.y)) * 1.2
		
	def extendRound(self, p):
		# 可以从8个方向走
		xs = (-1, 0, 1, -1, 1, -1, 0, 1)
		ys = (-1, -1, -1, 0, 0, 1, 1, 1)
		# 只能走上下左右四个方向
#		xs = (0, -1, 1, 0)
#		ys = (-1, 0, 0, 1)
		for x, y in zip(xs, ys):
			new_x, new_y = x + p.x, y + p.y
			# 无效或者不可行走区域，则勿略
			if not self.isValidCoord(new_x, new_y):
				continue
			# 构造新的节点
			node = NodeElem(p, new_x, new_y, p.dist + self.getCost(
						p.x, p.y, new_x, new_y))
			# 新节点在关闭列表，则忽略
			if self.nodeInClose(node):
				continue
			i = self.nodeInOpen(node)
			if i != -1:
				# 新节点在开放列表
				if self.open[i].dist > node.dist:
					# 现在的路径到比以前到这个节点的路径更好~
					# 则使用现在的路径
					self.open[i].parent = p
					self.open[i].dist = node.dist
				continue
			self.open.append(node)
			
	def getCost(self, x1, y1, x2, y2):
		"""
		上下左右直走，代价为1.0，斜走，代价为1.4
		"""
		if x1 == x2 or y1 == y2:
			return 1.0
		return 1.4
		
	def nodeInClose(self, node):
		for i in self.close:
			if node.x == i.x and node.y == i.y:
				return True
		return False
		
	def nodeInOpen(self, node):
		for i, n in enumerate(self.open):
			if node.x == n.x and node.y == n.y:
				return i
		return -1
		
	def isValidCoord(self, x, y):
		if x < 0 or x >= self.width or y < 0 or y >= self.height:
			return False
		return self.mapData[y][x] != 0
	
	def getSearched(self):
		l = []
		for i in self.open:
			l.append((i.x, i.y))
		for i in self.close:
			l.append((i.x, i.y))
		return l

	

def findPath(mapData, srcX, srcY, destX, destY):
	'''寻路
	'''
	obj = AStar(mapData, srcX, srcY, destX, destY)
	obj.findPath()
	return obj.path
	

