#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#查找与排序



#查找>=某区间对应的值,查找小于参数1的最近的key所对应的值
def getRightValue(i,dRange,default=0):
	lKeys=dRange.keys()
	lKeys.sort(None,None,True)#从大到小
	for iKey in lKeys:
		if i>=iKey:#比最大的还大
			return dRange[iKey]
	else:
		return default

#查找<=某区间对应的值,查找大于参数1的最近的key所对应的值
def getLeftValue(i,dRange,default=0):
	lKeys=dRange.keys()
	lKeys.sort()#从小到大
	for iKey in lKeys:
		if i<=iKey:#比最小的还小
			return dRange[iKey]
	else:
		return default

#查找i在dData的key相等的对应value
def getEqualValue(i,dData,default=0):
	for iKey in dData.itervalues():
		if i==iKey:
			return dData[iKey]
	else:
		return default

#多重比较器
#对两个obj依次用多个函数进行比武,直到两obj决出胜负
def multiCompare(obj1,obj2,*tCompareFunc):
	if not tCompareFunc:
		raise Exception,"必须给出比较函数."
	for func in tCompareFunc:
		iResult=func(obj1,obj2)
		if iResult!=0:#用胜负已经出来了,不用继续比了
			return iResult
	return 0

#二分查找法
#lOrder已经是有序的list,uItem是要查找的元素,返回一个恰当的index供插入
#tCompareFunc,可以不传,不传则以><来比较
#功能与C++的upper_bound相同(返回第一个“大于value”的元素位置；另一种解释是,可插入”元素值为value“且”不破坏有序性“的最后一个位置)
def binarySearchRight(lOrder,uItem,*tCompareFunc):
	iLow,iHigh = 0,len(lOrder)	#iHigh是pass the end的非法索引
	while iLow<iHigh:
		iMid=iLow+(iHigh-iLow)/2

		if tCompareFunc:
			iResult=multiCompare(uItem,lOrder[iMid],*tCompareFunc)
		elif uItem<lOrder[iMid]:
			iResult=-1
		else:#相等也认为是大于
			iResult=1

		if iResult<0:
			iHigh=iMid #即将插入的位置可能是iMid
		else:#相等也认为是大于
			iLow=iMid+1 #即将插入的位置可能是iMid+1
	return iLow

#二分查找法
#lOrder已经是有序的list,uItem是要查找的元素,返回一个恰当的index供插入
#tCompareFunc,可以不传,不传则以><来比较
#功能与C++的lower_bound相同(返回第一个 ”大于等于value“ 的元素位置。另一种解释是 可插入”元素值为value“且”不破坏有序性“的第一个位置)
def binarySearchLeft(lOrder,uItem,*tCompareFunc):
	iLow,iHigh=0,len(lOrder)#iHigh是pass the end的非法索引
	while iLow<iHigh:
		iMid=iLow+(iHigh-iLow)/2
		if tCompareFunc:
			iResult=multiCompare(uItem,lOrder[iMid],*tCompareFunc)
		elif uItem<=lOrder[iMid]:#相等也认为是小于
			iResult=-1
		else:
			iResult=1
		if iResult<=0:#相等也认为是小于
			iHigh=iMid #即将插入的位置可能是iMid
		else:
			iLow=iMid+1 #即将插入的位置可能是iMid+1
	return iLow

#二分查找法(发现第一个相等的就返回了)
#返回值如果是越界非法索引,表示没有找到
#功能与C++的binary_search相同
def binarySearchCenter(lOrder,uItem,*tCompareFunc):
	iLow,iHigh=0,len(lOrder)#iHigh是pass the end的非法索引
	while iLow<iHigh:
		iMid=iLow+(iHigh-iLow)/2
		if tCompareFunc:
			iResult=multiCompare(uItem,lOrder[iMid],*tCompareFunc)
		elif uItem<lOrder[iMid]:
			iResult=-1
		elif uItem>lOrder[iMid]:
			iResult=1
		else:
			iResult=0

		if iResult<0:
			iHigh=iMid
		elif iResult>0:
			iLow=iMid+1
		else:
			return iMid
	return len(lOrder)#越界非法索引,表示没有找到

#二分插入法，如果值相同，在所有相等的元素后面插入
#lOrder已经是有序的list,uItem是要插入的元素,
#tCompareFunc,可以不传,不传则以小于号来比较
def binaryInsertRight(lOrder,uItem,*tCompareFunc):
	iIndex=binarySearchRight(lOrder,uItem,*tCompareFunc)
	lOrder.insert(iIndex,uItem)
	return iIndex

#二分插入法，如果值相同，在当前位置插入
#lOrder已经是有序的list,uItem是要插入的元素,
#tCompareFunc,可以不传,不传则以小于号来比较
def binaryInsertLeft(lOrder,uItem,*tCompareFunc):
	iIndex=binarySearchLeft(lOrder,uItem,*tCompareFunc)
	lOrder.insert(iIndex,uItem)
	return iIndex

def mergeSort(mylist,low,mid,high,*tCompareFunc):#归并排序，随便网上拷一份，有更好的跟更清晰给份
	i = low
	j = mid + 1
	tmp = []
	while i <= mid and j <= high:
		if tCompareFunc:
			iResult=multiCompare(mylist[i],mylist[j],*tCompareFunc)
		elif mylist[i]<mylist[j]:
			iResult=-1
		else:#相等也认为是大于,因为要尽量往后面insert
			iResult=1
		if iResult<0:
			tmp.append(mylist[i])
			i = i + 1
		else:
			tmp.append(mylist[j])
			j = j + 1
	while i <= mid:
		tmp.append(mylist[i])
		i = i + 1
	while j <= high:
		tmp.append(mylist[j])
		j = j + 1
	return tmp