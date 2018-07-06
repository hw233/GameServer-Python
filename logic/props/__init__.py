# -*-coding:utf-8-*-
# 作者:马昭@曹县闫店楼镇
		
def create(propsNo):
	mod = props.load.getModule(propsNo)
	return mod.cProps(propsNo)

def new(propsNo, *tArgs, **dArgs):
	obj = create(propsNo)
	obj.onBorn(*tArgs, **dArgs)
	return obj

def createAndLoad(propsNo, dData):
	obj = create(propsNo)
	obj.load(dData)
	return obj

def fork(oProps, iStack=0):  # 复制全部属性，重新设置数量和重生,0表示叠加数量原样复制
	obj = createAndLoad(oProps.no(), copy.deepcopy(oProps.save()))
	if iStack != 0:  # 叠加数量不相同的情况下才重新生成id
		obj.setStack(iStack)
		obj.iUid = block.sysActive.gActive.genPropsId()
	return obj

if 'gdCacheProps' not in globals():
	gdCacheProps = {}

def getCacheProps(propsNo, *tArgs, **dArgs):  # 有时需要访问信息,生成一个对象放在内存中,避免每次都生成,提高性能
	obj = gdCacheProps.get(propsNo)
	if tArgs or dArgs  or not obj:  # 有特殊参数的要每次都生成
		obj = new(propsNo, *tArgs, **dArgs)
		if not tArgs and not dArgs:  # 只缓存不带附加参数的对象
			gdCacheProps[propsNo] = obj
	return obj

def getPropsName(propsNo):
	propsObj = getCacheProps(propsNo)
	return propsObj.name

def init():
	props.load.initModule()

def sendPropsForNewbie(who):
	# import props.equip
	# import block.numenBag
	lProps = [202040]
	for iProps in lProps:
		oProps = props.new(iProps)
		oProps.bind()
		who.propsCtn.addItem(oProps)

	# lMed = [221301,221302,221303,221304]
	# for iMed in lMed:
	# 	oMed = props.new(iMed,quality=50)
	# 	who.propsCtn.addItem(oMed)

	# lEquip = [100000,100001,100002,100003]
	# for iEquip in lEquip:
	# 	oEquip = props.new(iEquip)
	# 	dAdd = props.equip.creatAddAttr(oEquip.no())
	# 	oEquip.set("addAttr",dAdd)
	# 	iFive = props.equip.creatFive()
	# 	oEquip.set("five",iFive)
	# 	oEquip.set("life",20)
	# 	who.propsCtn.addItem(oEquip)

	# lEquip = [100050,100051,100052,100053]
	# for iEquip in lEquip:
	# 	oEquip = props.new(iEquip)
	# 	oEquip.set("life",0)
	# 	who.propsCtn.addItem(oEquip)

	# for iEquip in lProps:
	# 	oProps = props.new(iEquip)
	# 	who.tempCtn.addItem(oProps)
	# who.set("numenBag",1)
	
	# for iEquip in [200003, 202001, 202012, 221001, 222001, 224101,202006,221301,221302,221303,221304,100000,100001,100002,100003]:
	# 	oProps = props.new(iEquip)
	# 	who.storage.addItem(oProps)

# def onUpLevel(who):
# 	if who.level == 5:
# 		oProps = new(201001)
# 		oProps.bind()
# 		who.propsCtn.addItem(oProps)

import copy
import ujson
import c
import block.sysActive
import props.load