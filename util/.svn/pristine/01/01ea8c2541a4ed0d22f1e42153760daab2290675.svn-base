#-*-coding:utf-8-*-
#作者:叶伟龙@龙川县赤光镇

#获得0~(i-1)之间的随机数
def randomToN(i):
	if i<=0:
		raise Exception,'参数必须大于等于1.'
	return  random.randint(0,i-1)
	#return int(random.random()*i)

#根据几率返回key,such as  dDict={1:25,2:20,3:10,4:30,5:15}
#未命中返回None,传入空字典返回None
#类似NBA抽签选秀的方式，dDict的单元中的value值越高，概率就越高
def randomKey(dDict,iTotal=0):
	if iTotal==0:
		for v in dDict.itervalues():
			iTotal+=v
	i=randomToN(iTotal)
	t=0
	for k,v in dDict.iteritems():
		t+=v
		if i<t:
			return k
	return None

#根据几率返回多个key的list
def randomMultiKey(dDict,iCnt,iTotal=0):
	if iTotal==0:
		for v in dDict.itervalues():
			iTotal+=v
	l=[]
	for j in xrange(iCnt):
		i=randomToN(iTotal)
		t=0
		for k,v in dDict.iteritems():
			if k in l:
				continue
			t+=v
			if i<t:
				iTotal-=dDict[k]
				l.append(k)
				break
		else:
			break
	return l

#从0~iEnd-1排除ltRemove中的数字,然后随机抽出iCnt个数字,iCnt传得再大也只会返回实际可能最大个数
#不会抽到相同的值,有可能返回空的list;
#相当于洗牌程序
#iEnd	为总牌数
#iCnt	为抽出的牌数
#ltRemove	为排除的牌的序号
#return	抽牌的序号的集合
def getRandomCard(iEnd,iCnt,ltRemove=None):
	list=[]
	for i in xrange(iEnd):
		if ltRemove and i in ltRemove:
			continue
		list.append(i)

	iLen=len(list)
	for i in xrange(iLen):
		if i>=iCnt:
			break
		iPos=i+randomToN(iLen-i)
		if i!=iPos:
			tmp=list[i]
			list[i]=list[iPos]
			list[iPos]=tmp
	return list[:iCnt]



#获得不可重复随机数，适用于取值数量较少的情况
#有可能返回空的list;
#相当于洗牌程序
#iEnd	为总牌数
#iCnt	为抽出的牌数
#ltRemove	为排除的牌的序号
#return	抽牌的序号的集合
def getRandom(iEnd,iCnt,ltRemove=None):
	list=[]
	lResult=[]
	for i in xrange(iEnd):
		if ltRemove and i in ltRemove:
			continue
		list.append(i)

	for i in xrange(iCnt):
		iLen=len(list)-1-len(lResult)
		idx=randomToN(iLen)
		lResult.append(list[idx])
		temp=list[iLen]
		list[idx]=temp
		list[iLen]=temp
	return lResult

#打乱list,iCnt是需要返回list元素的个数
#抽牌程序
#list	为牌的集合
#iCnt	为抽牌数
def getShuffleList(list,iCnt=0):
	lResult=[]
	if iCnt==0:
		iCnt=len(list)
	for iPos in getRandomCard(len(list),iCnt):
		lResult.append(list[iPos])
	return lResult

import random
import u
