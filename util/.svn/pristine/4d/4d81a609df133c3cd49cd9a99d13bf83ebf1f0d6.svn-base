#-*- coding:UTF-8 -*-
import weakref
import keywords
import keyWordsData

class cNode(object):
	def __init__(self):
		self.sChar=''
		self.lChild=[]
		self.iBase=0
		self.oParent=None
		
	def children(self):	#返回该字后缀字列表
		lChar=[]
		for node in self.lChild:
			lChar.append(node.sChar)
		return lChar
		
	def child(self,sChar):	#返回当前字的某个后缀字结点
		for node in self.lChild:
			if node.sChar==sChar:
				return node
		raise
		
	def addChild(self,sChar):	#添加新结点
		childNode=cNode()
		childNode.sChar=sChar
		self.lChild.append(childNode)
		childNode.oParent=weakref.proxy(self)
		return childNode
		
	def __len__(self): 	#返回该字后缀字的个数
		return len(self.lChild)
		
def treeStruct(tree,lKeyWords): 	#建树,若该字为关键字的最后一个字,置iBase为-1
	for sWord in lKeyWords:
		root=tree
		iLast=len(sWord)-1
		for idx,sChar in enumerate(sWord):
			if sChar not in root.children():
				child=root.addChild(sChar)
			root=root.child(sChar)
			if idx==iLast:
				root.iBase=-1
			
def makeFirstCharLnode(tree):	#返回所有关键字的首字结点列表
	lNode=[]
	for child in tree.lChild:
		lNode.append(child)
	for node in lNode:
		for childNode in node.lChild:
			lNode.append(childNode)
	return lNode

def makeCharIndex(lNode): 	#返回关键字中所有字的索引(编码)
	i=1
	dCharIndex={}
	for node in lNode:
		if node.sChar not in dCharIndex:
			dCharIndex[node.sChar]=i
			i+=1
	return dCharIndex

def levelTraverseToMakeDoubleArrayTrie(tree,lNode,dIndex,lbase,lcheck): 	#层次遍历树,构造双数组
	lToExtend=[0]*len(dIndex) #base数组长度不够时扩充一次
	iFirstCharAmount=len(tree) #关键词首字个数
	for child in lNode:
		parent=child.oParent
		s=abs(parent.iBase)
		sPreChar=parent.sChar
		sCurChar=child.sChar
		c=dIndex[sCurChar]	#当前字的编码(索引)
		t=abs(lbase[s])+c 	#当前状态的位置
		if t<0:
			raise
		if lcheck[t]!=s:
			raise Exception,'wrong check[{}]={},base[{}]={},(preChar.curChar:{}.{}'.format(t,lcheck[t],s,lbase[s],sPreChar,sCurChar)

		if child.iBase==-1: 	#若该字为结束字
			if not child.lChild: 	#若该字后面无后缀字,则将其置为-1,例如:法轮
				lbase[t]=-1
				child.iBase=t 	#设置当前节点状态为t
				#print 'base[{}]={},check[{}]={},{}'.format(t,base[t],t,check[t],sCurChar)
				continue

		iStartBase=1
		while iStartBase!=0: #不断寻找base位置,直到返回正确的位置
			iStartBase=findChildBase(t,child,iStartBase,lToExtend,iFirstCharAmount,dIndex,lbase,lcheck)

def findChildBase(t,child,iStartBase,lToExtend,iFirstCharAmount,dIndex,lbase,lcheck):
	try:
		for iNewBase in xrange(iStartBase,len(lbase)): 	#若该字存在孩子节点,设置新状态的base(每个base即为1个状态)
			bFlag=True
			for tempChild in child.lChild:
				iChildIdx=dIndex[tempChild.sChar]
				next_t=iNewBase+iChildIdx
				if next_t<=iFirstCharAmount: #若满足条件的位置小于首字长度,跳过(前n个base为首字的位置,不能占用)
					bFlag=False
					break
				if lbase[next_t]>0 or lcheck[next_t]:	#base与check任意一个不为0,说明该状态(位置)已被占用,继续寻找下一个base
					bFlag=False
					break
			if bFlag:
				for tempChild in child.lChild:
					iChildIdx=dIndex[tempChild.sChar]
					lcheck[iNewBase+iChildIdx]=t
				if lbase[t]!=0:
					raise Exception,'base[{}]={} already exist,sCurChar:{},sPreChar:{}'.format(t,lbase[t],sCurChar,sPreChar)
				lbase[t]=-iNewBase if child.iBase==-1 else iNewBase 	#若该位置为匹配敏感词,后缀词仍存在
				child.iBase=t	#设置当前节点状态为t
				#print 'base[{}]={},check[{}]={},{}'.format(t,base[t],t,check[t],sCurChar)
				return 0 #找到正确的base位置,返回0,终止循环
	except IndexError: #初始数组长度不够,增加数组长度(最小放得下所有字的长度不会推导...每次发现不够就扩充一次)
		lbase.extend(lToExtend)
		lcheck.extend(lToExtend)
		return iNewBase
	except:
		raise Exception,'no base meet demands,base[{}]={},sCurChar:{},sPreChar:{}'.format(t,base[t],sCurChar,sPreChar)

def makeSpecailMark(lSpecialMarks):
	sTemp=set()
	for lSpecial in lSpecialMarks:
		sTemp|=set(transUnicode(lSpecial))
	return sTemp

#查询词
def next_check(s,iCharIndex):
	t=abs(base[s])+iCharIndex
	if check[t]!=s:
		return False
	return True

def fliter(sWord):
	sWord=sWord.decode('utf8')
	lTargetIdx=[]			#标记敏感词开始与结束位置
	bStart=False
	bMark=False
	iLast=len(sWord)-1
	for iIdx,sChar in enumerate(sWord):
		if sChar in sSpecialMarks:
			continue
		if sChar not in dCharIndex:
			bStart=False
			if len(lTargetIdx)&1 !=0: #标记组长度为奇数,说明存入一个开始位置,将其弹掉
				lTargetIdx.pop()
			continue
		iCharIndex=dCharIndex[sChar]
		if not bStart:	#尚未开始匹配
			if sChar in sFirstChar: #该字符在首字符集中,开始匹配
				iHeadBase=iCharIndex
				bStart=True
				lTargetIdx.append(iIdx)
				if base[iHeadBase]==-1:
					lTargetIdx.append(iIdx)
					lTargetIdx.append(iIdx)
				continue
			else: 		#该字符不在首字符集中
				continue
		if not next_check(iHeadBase,iCharIndex): #匹配失败
			lTargetIdx.pop()
			if sChar in sFirstChar:
				iHeadBase=iCharIndex		#将失败字作为首字继续查
				lTargetIdx.append(iIdx)
				if base[iHeadBase]==-1:
					lTargetIdx.append(iIdx)
					bStart=False
			else:
				bStart=False
			continue
		iHeadBase=abs(base[iHeadBase])+iCharIndex      # 更新状态
		t=base[iHeadBase] #检测当前状态是否完成匹配
		if t<0:
			if t==-1: #到该词匹配结束
				bStart=False
				lTargetIdx.append(iIdx)
			else:	#到此匹配某个关键词,但另一关键词包含该部分,即这部分词为另一关键词的前缀,需要继续匹配
				lTargetIdx.append(iIdx)
				lTargetIdx.append(iIdx+1)

	if bStart:	#匹配结束,仅为某关键词的部分前缀
		lTargetIdx.pop()
	if lTargetIdx:
		if len(lTargetIdx)&1==1:
			print 'lTargetIdx wrong'
		lPiece=[]
		for iIdx in xrange(0,len(lTargetIdx),2):
			if iIdx==0:
				lPiece.append(sWord[:lTargetIdx[iIdx]])
			else:
				lPiece.append(sWord[lTargetIdx[iIdx-1]+1:lTargetIdx[iIdx]])
			#lPiece.append('*'*len(unicode(sWord[lTargetIdx[iIdx]:lTargetIdx[iIdx+1]+1],'utf8')))
			lPiece.append('*'*(lTargetIdx[iIdx+1]+1-lTargetIdx[iIdx]))
		# if iIdx+1<iLast:
		lPiece.append(sWord[lTargetIdx[iIdx+1]+1:])
		return ''.join(lPiece).encode('utf8')
	else:
		return sWord.encode('utf8')
		
def transUnicode(lWords):
	lWord=[]
	for sWord in lWords:
		lWord.append(sWord.decode('utf8'))
	return lWord

def init():
	print "trie init..."
	global sSpecialMarks,sFirstChar,dCharIndex,base,check
	lKeyWords=transUnicode(keyWordsData.gtDeny)
	sSpecialMarks=makeSpecailMark(keywords.lSpecialMarks) #特殊字符集
	#lKeyWords=['bad','bye','bay','baye','tear','grubby','trie','base','check','eloan','lexington','equity']#

	tree=cNode()
	treeStruct(tree,lKeyWords) #构建关键词字典树
	sFirstChar=set(tree.children()) #首字集合
	lNode=makeFirstCharLnode(tree)
	dCharIndex=makeCharIndex(lNode)	#关键词中各字编码
	iLen=len(dCharIndex)
	base=[0]*iLen
	check=[0]*iLen
	levelTraverseToMakeDoubleArrayTrie(tree,lNode,dCharIndex,base,check)

if '__name__'=='__main__':
	init()

	# s='有谁知道三級片在哪里?fangong反攻反共的人呢，他们又在哪里？疆獨呢？'
	# import time

	# start=time.time()
	# for i in xrange(10000):
	# 	t=fliter(s)
	# print time.time()-start

	# for sWord in transUnicode(keywords.gtDeny):
	# 	sAfterFliter=fliter(sWord)
	# 	print sAfterFliter.decode('utf8').encode('gbk')

	while True:
		sInput=raw_input().decode('gbk').encode('utf8')
		sAfterFliter=fliter(sInput)
		print sAfterFliter.decode('utf8').encode('gbk')
