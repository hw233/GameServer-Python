#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
'''策划数据导表指令'''

M=0x1	#must 不可以为空,策划必须填
D=0x2	#dict,字典类型
L=0x4	#list,列表类型
T=0x8	#tuple,元组类型(尽量不要用,要用L,即是list,原因是:单个元素的tuple也必须要有逗号,否则括号变成4则运算符,不再是tuple
		#策划容易填错,用list单个元素后面不加逗号,也还是list,不会出错)

I=0x10	#integer,整形
F=0x20	#float,浮点类型
N=0x40 #number,数值类型

S=0x80	#string,字符串类型
E=0x100	#expression lambda表达式

A=~0	#any,任意类型,可能字符串,可能整形,可能浮点,可以是list,tuple,dict

#单个sl文件来源的配置表
#其他解析方式的要独立写函数,需要读取多个sl文件的也要自已独立写
gdSingleSrcConfig={
	'roleExp':{'表名':'角色升级经验表','变量名':'gdData','sl':'roleExp.sl','py':'roleExpData.py'},
	'petExp':{'表名':'宠物升级经验表','变量名':'gdData','sl':'petExp.sl','py':'petExpData.py'},
	'petVariation':{'表名':'宠物特长资质表','变量名':'gdData','sl':'petVariation.sl','py':'petVariationData.py'},
	'pet':{'表名':'宠物表','变量名':'gdData','sl':'pet.sl','py':'petData.py'},
	'monsterBase':{'表名':'怪物基础表','变量名':'gdData','sl':'monsterBase.sl','py':'monsterBase.py'},

	'skillSchUpgrade':{'表名':'职业技能升级表','变量名':'gdData','sl':'skillSchUpgrade.sl','py':'skillSchUpgrade.py'},
	'skillGuildLearn':{'表名':'帮派技能学习表','变量名':'gdData','sl':'skillGuildLearn.sl','py':'skillGuildLearn.py'},
	'makeFood':{'表名':'烹饪表','变量名':'gdData','sl':'makeFood.sl','py':'makeFoodData.py'},
	'propsGroup':{'表名':'物品分组表','变量名':'gdData','sl':'propsGroup.sl','py':'propsGroupData.py'},
	'makeMedicine':{'表名':'炼丹表','变量名':'gdData','sl':'makeMedicine.sl','py':'makeMedicineData.py'},
	'petResetCost':{'表名':'宠物重置费用','变量名':'gdData','sl':'petResetCost.sl','py':'petResetCost.py'},
	'petSkillSlotsExp':{'表名':'宠物技能格开启经验表', '变量名':'gdData', 'sl':'petSkillSlotsExp.sl', 'py':'petSkillSlotsExp.py'},
	# 'buddy':{'表名':'助战伙伴','变量名':'gdData','sl':'buddy.sl','py':'buddyData.py'},
	
	'title':{'表名':'称号表', '变量名':'gdData', 'sl':'title.sl', 'py':'titleData.py'},
	'scene':{'表名':'场景表','变量名':'gdData','sl':'scene.sl','py':'sceneData.py'},
	'equip':{'表名':'装备表','变量名':'gdData','sl':'equip.sl','py':'equipData.py'},
	'npc':{'表名':'npc表','变量名':'gdData','sl':'npc.sl','py':'npcData.py'},
	'door':{'表名':'传送点表','变量名':'gdData','sl':'door.sl','py':'doorData.py'},
	'shop':{'表名':'商品表','变量名':'gdData','sl':'shop.sl','py':'shopData.py'},
	'taskType':{'表名':'任务类型表','变量名':'gdData','sl':'taskType.sl','py':'taskTypeData.py'},
	# 'buddyBase':{'表名':'伙伴属性配置表','变量名':'gdData','sl':'buddyBase.sl','py':'buddyBase.py'},
	'pointAllot':{'表名':'属性分配表','变量名':'gdData','sl':'pointAllot.sl','py':'pointAllot.py'},
	'lockPackage':{'表名':'背包开格子费用表','变量名':'gdData','sl':'lockPackage.sl','py':'lockPackageData.py'},
	'shapePartScope':{'表名':'造型部位随机范围表','变量名':'gdData','sl':'shapePartScope.sl','py':'shapePartScope.py'},
	'storage':{'表名':'仓库表','变量名':'gdData','sl':'storage.sl','py':'storageData.py'},
	'channel':{'表名':'频道配置表','变量名':'gdData','sl':'channel.sl','py':'channelData.py'},
	'robotData':{'表名':'机器人表','变量名':'attrData','sl':'robotData.sl','py':'robotData.py'},
	'openLevel':{'表名':'等级上限开启表','变量名':'gdData','sl':'openLevel.sl','py':'openLevelData.py'},
	'marketMall':{'表名':'商城配置表', '变量名':'gdData', 'sl':'marketMall.sl', 'py':'mallData.py'},
	'holiday':{'表名':'节日礼物','变量名':'gdData','sl':'holiday.sl','py':'holidayData.py'},
	'rankClassify':{'表名':'排行榜分类','变量名':'gdData','sl':'rankClassify.sl','py':'RankClassifyData.py'},
	'rank':{'表名':'排行榜','变量名':'gdData','sl':'rank.sl','py':'RankData.py'},
	'rankPet':{'表名':'宠物排行榜','变量名':'gdData','sl':'rankPet.sl','py':'RankPetData.py'},
	'dye':{'表名':'染色配置表','变量名':'gdData','sl':'dye.sl','py':'dyeData.py'},
	'sign':{'表名':'每日签到','变量名':'gdData','sl':'signIn.sl','py':'SignInData.py'},
	'guildSign':{'表名':'帮派签到','变量名':'gdData','sl':'guildSignIn.sl','py':'GuildSignInData.py'},
	'rareEquipScore':{'表名':'装备珍品评分表','变量名':'gdData','sl':'rareEquipScore.sl','py':'rareEquipScoreData.py'},
	'viewLink':{'表名':'界面链接','变量名':'gdData','sl':'viewLink.sl','py':'ViewLinkData.py'},
	'question':{'表名':'答题题库','变量名':'gdData','sl':'answer/question.sl','py':'QuestionData.py'},
	'questionFinal':{'表名':'金章之试题库','变量名':'gdData','sl':'answer/questionFinal.sl','py':'QuestionFinalData.py'},
	'holyPetExchange':{'表名':'宠物兑换表','变量名':'gdData','sl':'holyPetExchange.sl','py':'holyPetExchangeData.py'},
	'newRoleBorn':{'表名':'玩家出生点','变量名':'gdData','sl':'newRoleBorn.sl','py':'newRoleBornData.py'},
	'tougheningExp':{'表名':'历练经验表','变量名':'gdData','sl':'tougheningExp.sl','py':'tougheningExpData.py'},
}
#'全局导表'

# for sName,v in gdSingleSrcConfig.iteritems():
# 	sCode='''def {}(ep):
# 	'{}'
# 	_execConfig(ep,'{}','{}','{}','{}','{}')'''

# 	sTableName=v['表名']
# 	sCode=sCode.format(v['函数名'],sTableName,sTableName,v['变量名'],v['sl'],v['py'],v['热更新名'])
# 	exec(sCode)

def daobiao(ep,sName): #pet
	'导表指令'
	if sName not in gdSingleSrcConfig:
		try:
			func = eval(sName)
		except:
			ep.rpcTips('没有{}表'.format(sName))
			return
		func(ep)
		return

	info=gdSingleSrcConfig[sName]
	sTableName=info['表名']
	sVarName=info['变量名']
	sSlName=info['sl']
	sPyName=info['py']
	sHotFixName=sPyName[:-3]
	_execConfig(ep,sTableName,sVarName,sSlName,sPyName,sHotFixName)

def _execConfig(ep,sTableName,sVarName,sSlName,sPyName,sHotFixName):#
	ps=txtParser.configparser.cTxtParser(sVarName,'data/sl/'+sSlName)
	mk=pyMaker.cPyMaker('data/py/'+sPyName,ps)
	mk.makeToPyFile()
	hotUpdate.update(sHotFixName)
	ep.rpcTips('生成'+sTableName+'OK')
	
def anlei(ep):
	'''暗雷表
	'''
	psList = []
	psList.append(txtParser.configparser.cTxtParser('sceneFight','data/sl/anlei/scenefight.sl'))
	psList.append(txtParser.multiparser.cTxtParser('fightInfo','data/sl/anlei/fight.sl'))
	psList.append(txtParser.configparser.cTxtParser('ableInfo','data/sl/anlei/able.sl'))
	psList.append(txtParser.configparser.cTxtParser('rewardInfo','data/sl/anlei/reward.sl'))
	psList.append(txtParser.multiparser.cTxtParser('rewardPropsInfo','data/sl/anlei/rewardprops.sl'))
	mk=pyMaker.cPyMaker('data/py/anleiData.py',*psList)
	mk.makeToPyFile()
	hotUpdate.update('anleiData')
	ep.rpcTips('生成暗雷数据OK')
	
def magicTime(ep):
	'''法术动画时间表
	'''
	psList = []
	psList.append(txtParser.configparser.cTxtParser('performData','data/sl/magicTime/performData.sl'))
	psList.append(txtParser.configparser.cTxtParser('shapeData','data/sl/magicTime/shapeData.sl'))
	mk=pyMaker.cPyMaker('data/py/magicTimeData.py', *psList)
	mk.makeToPyFile()
	hotUpdate.update('magicTimeData')
	ep.rpcTips('生成法术动画时间表OK')
	
def maketask(ep, taskId):
	'''任务导表
	'''
	import makeData.mktask
	makeData.mktask.make(ep, taskId)
	
def makeact(ep, activityName):
	'''活动导表
	'''
	import makeData.mkactivity
	makeData.mkactivity.make(ep, activityName)
	
def skillNpc(ep):
	'''npc技能表
	'''
	import pyMaker.skillNpcMaker
	import pyMaker.performNpcMaker

	parser = txtParser.configparser.cTxtParser("main", "data/sl/skillNpc.sl")
	
	maker = pyMaker.skillNpcMaker.PyMaker(parser)
	maker.makeToPyFile()
	maker = pyMaker.performNpcMaker.PyMaker(parser)
	maker.makeToPyFile()

	ep.rpcTips("生成npc技能数据OK")

def skillSch(ep):
	'''门派技能表
	'''
	import pyMaker.skillSchMaker
	import pyMaker.performSchMaker
	
	parser = txtParser.configparser.cTxtParser("main", "data/sl/skillSch.sl")
	
	maker = pyMaker.skillSchMaker.PyMaker(parser)
	maker.makeToPyFile()
	maker = pyMaker.performSchMaker.PyMaker(parser)
	maker.makeToPyFile()
	
	_execConfig(ep, "门派技能表", "gdData", "skillSch.sl", "skillSchData.py", "skillSchData")
	
	ep.rpcTips("生成门派技能数据OK")
	
def skillGuild(ep):
	'''帮派技能表
	'''
	import pyMaker.skillGuildMaker
	parser = txtParser.configparser.cTxtParser("main", "data/sl/skillGuild.sl")
	maker = pyMaker.skillGuildMaker.PyMaker(parser)
	maker.makeToPyFile()
	_execConfig(ep, "帮派技能表", "gdData", "skillGuild.sl", "skillGuildData.py", "skillGuildData")
	ep.rpcTips("生成帮派技能数据OK")
	
def skillEquip(ep):
	'''装备技能表(特技特效)
	'''
	import pyMaker.skillEquipMaker
	import pyMaker.performEquipMaker

	parser = txtParser.configparser.cTxtParser("main", "data/sl/skillEquip.sl")
	
	maker = pyMaker.skillEquipMaker.PyMaker(parser)
	maker.makeToPyFile()
	maker = pyMaker.performEquipMaker.PyMaker(parser)
	maker.makeToPyFile()
	
	_execConfig(ep, "特技特效", "gdData", "skillEquip.sl", "skillEquipData.py", "skillEquipData")

	ep.rpcTips("生成装备技能表(特技特效)数据OK")
	
def skillPractice(ep):
	'''修炼技能
	'''
	import pyMaker.skillPracticeMaker
	import pyMaker.performPracticeMaker

	parser = txtParser.configparser.cTxtParser("main", "data/sl/skillPractice.sl")
	
	maker = pyMaker.skillPracticeMaker.PyMaker(parser)
	maker.makeToPyFile()
	maker = pyMaker.performPracticeMaker.PyMaker(parser)
	maker.makeToPyFile()

	ep.rpcTips("生成修炼技能数据OK")

def props(ep):
	'''物品表
	'''
	ps = txtParser.propsparser.cTxtParser("gdData","data/sl/props.sl")
	mk = pyMaker.cPyMaker('data/py/propsData.py',ps)
	mk.makeToPyFile()
	hotUpdate.update('propsData')
	ep.rpcTips('生成物品表OK')

def levelmedicine(ep):
	'''等级药表
	'''
	ps = txtParser.propsparser.cTxtParser("gdData","data/sl/levelmedicine.sl")
	mk = pyMaker.cPyMaker('data/py/levelmedicineData.py',ps)
	mk.makeToPyFile()
	hotUpdate.update('levelmedicineData')
	ep.rpcTips('生成等级药表OK')

def food(ep):
	'''食品表
	'''
	ps = txtParser.propsparser.cTxtParser("gdData","data/sl/food.sl")
	mk = pyMaker.cPyMaker('data/py/foodData.py',ps)
	mk.makeToPyFile()
	hotUpdate.update('foodData')
	ep.rpcTips('生成食品表OK')

def buff(ep):
	'''buff表
	'''
	parser = txtParser.configparser.cTxtParser("main", "data/sl/buff.sl")
	maker = pyMaker.buffmaker.PyMaker(parser)
	maker.makeToPyFile()
	ep.rpcTips("生成buff数据OK")

def makeLaunch(ep):
	'奖励投放表'
	lDataType = [I,I,I,I,I,I,S]
	ps=txtParser.launchParser.cTxtParser('gdData','data/sl/launch.sl',lDataType)
	mk=pyMaker.cPyMaker('data/py/launchData.py',ps)
	mk.makeToPyFile()
	hotUpdate.update('launchData')
	ep.rpcTips('生成投放表OK')



def randName(ep):
	'生成随机名字表'
	psList = []
	psList.append(txtParser.randnameparser.cTxtParser('gdFamilyName','data/sl/randomName/familyName.sl'))
	psList.append(txtParser.randnameparser.cTxtParser('gdMaleName','data/sl/randomName/maleName.sl'))
	psList.append(txtParser.randnameparser.cTxtParser('gdFemaleName','data/sl/randomName/femaleName.sl'))
	mk=pyMaker.cPyMaker('data/py/randNameData.py',*psList)
	mk.makeToPyFile()
	hotUpdate.update('randNameData')
	ep.rpcTips('生成随机名字表OK')
	import client4center
	client4center.getCenterEndPoint().rpcHotUpdate2center('randNameData')

#生成屏蔽词表
def makeInvalidWord(ep):
	lDataType = [S]
	ps=txtParser.randnameparser.cTxtParser('gtDeny','data/sl/InvalidWord.sl',lDataType)
	mk=pyMaker.cPyMaker('data/py/InvalidWordData.py',ps)
	mk.makeToPyFile()
	hotUpdate.update('InvalidWordData')
	ep.rpcTips('生成屏蔽词表OK')


#生成npc对白
def makeNpcDialog(ep):
	lDataType = [I,I,S,S]
	import txtParser.npcdialogparser
	ps=txtParser.npcdialogparser.cTxtParser('gdData','data/sl/NpcDialog.sl',lDataType)
	mk=pyMaker.cPyMaker('data/py/NpcDlgData.py',ps)
	mk.makeToPyFile()
	hotUpdate.update('NpcDlgData')
	ep.rpcTips('生成npc对白表成功.')

def makeKeyWord(ep):
	'屏蔽字列表'	
	ps=txtParser.randnameparser.cTxtParser('gtDeny','data/sl/keywords.sl')
	mk=pyMaker.cPyMaker('data/py/keyWordsData.py',ps)
	mk.makeToPyFile()
	hotUpdate.update('keyWordsData')
	ep.rpcTips('生成屏蔽字列表ok')
	
def lineup(ep):
	'''阵法表
	'''
	psList = []
	psList.append(txtParser.configparser.cTxtParser('lineupList','data/sl/lineup/lineup.sl'))
	psList.append(txtParser.configparser.cTxtParser('effectList','data/sl/lineup/effect.sl'))
	psList.append(txtParser.configparser.cTxtParser('effectRatioList','data/sl/lineup/effectRatio.sl'))
	psList.append(txtParser.configparser.cTxtParser('lineupEyeList','data/sl/lineup/lineupeye.sl'))
	psList.append(txtParser.configparser.cTxtParser('upgradeList','data/sl/lineup/upgrade.sl'))
	psList.append(txtParser.configparser.cTxtParser('expPropsList','data/sl/lineup/expprops.sl'))
	psList.append(txtParser.listparser.cTxtParser('skillList','data/sl/lineup/skill.sl'))
	mk=pyMaker.lineupmaker.PyMaker('data/py/lineupData.py',*psList)
	mk.makeToPyFile()
	hotUpdate.update('lineupData')
	ep.rpcTips('生成阵法数据OK')

def state(ep):
	'''状态表
	'''
	parser = txtParser.configparser.cTxtParser("main", "data/sl/state.sl")
	maker = pyMaker.statemaker.PyMaker(parser)
	maker.makeToPyFile()
	ep.rpcTips("生成状态配置数据OK")

def teamTarget(ep):
	parser = txtParser.teamTargetParser.cTxtParser("gdData", "data/sl/teamTarget.sl")
	maker=pyMaker.cPyMaker('data/py/teamTargetData.py', parser)
	maker.makeToPyFile()
	hotUpdate.update('teamTargetData')
	ep.rpcTips("生成组队目标数据OK")

def petWash(ep):
	'''异兽洗炼导表
	'''
	psList = []
	psList.append(txtParser.configparser.cTxtParser("gdGrowLevelRate", "data/sl/pet/growLevelRate.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdSixAttrLevelRate", "data/sl/pet/sixAttrLevelRate.sl"))
	psList.append(txtParser.singleparser.cTxtParser("gdRandomSkills", "data/sl/pet/randomSkills.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdSkillBookExp", "data/sl/pet/skillBookAddExp.sl"))
	mk = pyMaker.cPyMaker("data/py/petWashData.py", *psList)
	mk.makeToPyFile()
	hotUpdate.update("petWashData")
	ep.rpcTips("生成异兽洗炼数据OK")

def equipSesks(ep):
	'''打造特技特效库导表
	'''
	psList = []
	psList.append(txtParser.configparser.cTxtParser("gdData", "data/sl/equipSesks.sl"))
	mk = pyMaker.cPyMaker("data/py/sesksData.py", *psList)
	mk.makeToPyFile()
	hotUpdate.update("sesksData")
	ep.rpcTips("生成装备特技特效数据OK")
	
def listener(ep):
	'''监听器表
	'''
	import makeData.pyMaker.listenerMaker
	import listener
	parser = txtParser.configparser.cTxtParser("main", "data/sl/listener.sl")
	parser.excelMulti = True
	maker = makeData.pyMaker.listenerMaker.PyMaker(parser)
	maker.makeToPyFile()
	ep.rpcTips("生成监听器表数据OK")
	listener.init()

def achv(ep):
	'''成就表
	'''
	import makeData.pyMaker.achvMaker
	parser = txtParser.configparser.cTxtParser("main", "data/sl/achv.sl")
	maker = makeData.pyMaker.achvMaker.PyMaker(parser)
	maker.makeToPyFile()
	ep.rpcTips("生成成就表数据OK")
	
def pointsExchange(ep):
	psList = []
	psList.append(txtParser.multiparser.cTxtParser('gdData','data/sl/pointsExchange.sl'))
	mk=pyMaker.cPyMaker('data/py/pointsExchangeData.py',*psList)
	mk.makeToPyFile()
	hotUpdate.update('pointsExchangeData')
	ep.rpcTips('生成积分兑换数据OK')

def words(ep):
	'''闲话表
	'''
	psList = []
	psList.append(txtParser.singleparser.cTxtParser("gdProbability", "data/sl/words/probability.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdPetWords", "data/sl/words/petWords.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdBuddyWords", "data/sl/words/buddyWords.sl"))
	mk = pyMaker.cPyMaker("data/py/wordsData.py", *psList)
	mk.makeToPyFile()
	hotUpdate.update("wordsData")
	ep.rpcTips("生成闲话表OK")

def pratice(ep):
	'''修炼技能等级数据
	'''
	psList = []
	psList.append(txtParser.configparser.cTxtParser("gdPraticeExp", "data/sl/pratice/praticelExp.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdGuildLevel", "data/sl/pratice/guildLevel.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdRoleLevel", "data/sl/pratice/roleLevel.sl"))
	mk = pyMaker.cPyMaker("data/py/skillPraticeLevelData.py", *psList)
	mk.makeToPyFile()
	hotUpdate.update("skillPraticeLevelData")
	ep.rpcTips("生成修炼技能等级数据OK")

def trade(ep):
	'''交易中心表
	'''
	psList = []
	psList.append(txtParser.tradeparser1.cTxtParser("gdCashGoodsList", "data/sl/trade/cashgoods.sl"))
	psList.append(txtParser.tradeparser2.cTxtParser("gdCashGoods", "data/sl/trade/cashgoods.sl"))
	psList.append(txtParser.tradeparser1.cTxtParser("gdTradeCashGoodsList", "data/sl/trade/tradecashgoods.sl"))
	psList.append(txtParser.tradeparser2.cTxtParser("gdTradeCashGoods", "data/sl/trade/tradecashgoods.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdStallExtend", "data/sl/trade/stallextend.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdFood", "data/sl/trade/food.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdMedicine", "data/sl/trade/medicine.sl"))
	mk = pyMaker.cPyMaker("data/py/tradeGoodsData.py", *psList)
	mk.makeToPyFile()
	hotUpdate.update("tradeGoodsData")
	ep.rpcTips("生成交易中心表OK")

def guild(ep):
	'''帮派导表
	'''
	import makeData.pyMaker.guildNpcMaker
	import makeData.pyMaker.guildDoorMaker

	psList = []
	psList.append(txtParser.configparser.cTxtParser("gdGuildMember", "data/sl/guild/guildMember.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdGuildMaintain", "data/sl/guild/guildMaintain.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdGuildUpgrade", "data/sl/guild/guildUpgrade.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdGuildWeight", "data/sl/guild/guildWeight.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdGuildDepot", "data/sl/guild/guildDepot.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdGuildDoor", "data/sl/guild/guildDoor.sl"))
	maker = pyMaker.cPyMaker("data/py/guildData.py", *psList)
	maker.makeToPyFile()
	
	parser = txtParser.configparser.cTxtParser("main", "data/sl/guild/guildNpc.sl")
	maker = pyMaker.guildNpcMaker.PyMaker(parser)
	maker.makeToPyFile()

# 	parser = txtParser.configparser.cTxtParser("main", "data/sl/guild/guildDoor.sl")
# 	maker = pyMaker.guildDoorMaker.PyMaker(parser)
# 	maker.makeToPyFile()
	ep.rpcTips("生成帮派导表OK")

def giftBag(ep):
	'''礼包导表
	'''
	psList = []
	psList.append(txtParser.giftbagparser.cTxtParser("gdGiftBag", "data/sl/giftBag/bag.sl"))
	psList.append(txtParser.giftbagparser.cTxtParser("gdBranch", "data/sl/giftBag/branch.sl"))
	psList.append(txtParser.giftbagparser.cTxtParser("gdgembag", "data/sl/giftBag/gembag.sl"))
	mk = pyMaker.cPyMaker("data/py/giftBagData.py", *psList)
	mk.makeToPyFile()
	hotUpdate.update("giftBagData")
	ep.rpcTips("礼包导表OK")

def buddy(ep):
	'''伙伴导表
	'''
	psList = []
	psList.append(txtParser.configparser.cTxtParser("gdBuddy", "data/sl/buddy/buddy.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdBase", "data/sl/buddy/base.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdQuality", "data/sl/buddy/quality.sl"))
	psList.append(txtParser.buddyparser.cTxtParser("gdMajor", "data/sl/buddy/major.sl"))
	psList.append(txtParser.buddyparser.cTxtParser("gdRelation", "data/sl/buddy/relation.sl"))
	psList.append(txtParser.listparser.cTxtParser("glSkillList", "data/sl/buddy/skilllist.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdCost", "data/sl/buddy/cost.sl"))
	psList.append(txtParser.configparser.cTxtParser("gdMax", "data/sl/buddy/max.sl"))
	mk = pyMaker.cPyMaker("data/py/buddyData.py", *psList)
	mk.makeToPyFile()
	hotUpdate.update("buddyData")
	ep.rpcTips("伙伴导表OK")

def getAllMethod():#获取全部方法,供makeAll指令使用
	for sName,obj in globals().iteritems():
		if sName.startswith('_'):#一些系统生成的属性是双下划线开头的,我们的自己的私有的是单下划线,都跳过
			continue
		if type(obj)!=types.FunctionType:
			continue
		if not sName.startswith('make'):#不是以make前缀开始的函数
			continue
		yield obj
	
def makeCollect(ep):
	'''室外收集导表
	'''
	import makeData.mkcollect
	makeData.mkcollect.make(ep)

	import client4center
	client4center.getCenterEndPoint().rpcHotUpdate2center('collect.mainCollect')
	
def makeAnswer(ep):
	'''答题奖励导表
	'''
	psList = []
	srcPath = "data/sl/answer/{}.sl" 
	psList.append(makeData.txtParser.configparser.cTxtParser("rewardInfo", srcPath.format("reward"), ignore=True))
	psList.append(makeData.txtParser.multiparser.cTxtParser("rewardPropsInfo", srcPath.format("rewardprops"), ignore=True))
	psList.append(makeData.txtParser.kvParser.cTxtParser("configInfo", srcPath.format("config"), ignore=True))
	psList.append(makeData.txtParser.chatparser.cTxtParser("chatInfo", srcPath.format("chat"), ignore=True))
	psList.append(makeData.txtParser.kvParser.cTxtParser("questionTypeInfo", srcPath.format("questionType"), ignore=True))
	psList.append(makeData.txtParser.configparser.cTxtParser("npcInfo", srcPath.format("npc"), ignore=True))
	maker = makeData.pyMaker.answerMaker.PyMaker(*psList)
	maker.makeToPyFile()

	daobiao(ep, "question")
	daobiao(ep, "questionFinal")
	import answer
	answer.initQuestionType()
	ep.rpcTips("生成答题数据OK")

def chat(ep):
	'''对白
	'''
	psList = []
	psList.append(txtParser.chatparser.cTxtParser('gdData','data/sl/chat.sl'))
	mk=pyMaker.lineupmaker.PyMaker('data/py/chatData.py',*psList)
	mk.makeToPyFile()
	hotUpdate.update('chatData')
	ep.rpcTips('生成对白数据OK')

def treasureShop(ep):
	'''珍品阁表
	'''
	psList = []
	psList.append(txtParser.treasureshopparser.cTxtParser("gdTreasureShopData", "data/sl/treasureShop.sl"))
	mk = pyMaker.cPyMaker("data/py/treasureShopData.py", *psList)
	mk.makeToPyFile()
	hotUpdate.update("treasureShopData")
	ep.rpcTips("生成珍品阁表OK")

def ride(ep):
	'''坐骑
	'''
	psList = []
	psList.append(txtParser.configparser.cTxtParser("rideData", "data/sl/ride.sl"))
	psList.append(txtParser.configparser.cTxtParser("rideBuyPointData", "data/sl/rideBuyPoint.sl"))
	psList.append(txtParser.kvParser.cTxtParser("rideConfig", "data/sl/rideConfig.sl"))

	mk = pyMaker.cPyMaker("data/py/rideData.py", *psList)
	mk.makeToPyFile()
	hotUpdate.update("rideData")
	ep.rpcTips("生成坐骑配置表OK")
	
def fiveEl(ep):
	'''五行数据
	'''
	import makeData.pyMaker.fiveElMaker
	psList = []
	psList.append(txtParser.dictParser.cTxtParser("kezhi", "data/sl/fiveEl/kezhi.sl"))
	mk = makeData.pyMaker.fiveElMaker.PyMaker('data/py/fiveElData.py', *psList)
	mk.makeToPyFile()
	hotUpdate.update('fiveElData')
	ep.rpcTips('生成五行数据OK')

def grade(ep):
	'''评分导表
	'''
	import makeData.pyMaker.gradeMaker
	psList = []
	psList.append(txtParser.kvParser.cTxtParser("mapEquipBase", "data/sl/mapEquipBase.sl"))
	psList.append(txtParser.kvParser.cTxtParser("mapWeaponSchool", "data/sl/mapWeaponSchool.sl"))
	psList.append(txtParser.kvParser.cTxtParser("dPetAptitudeFactor", "data/sl/dPetAptitudeFactor.sl"))
	psList.append(txtParser.configparser.cTxtParser('dPetTypeFactor','data/sl/dPetTypeFactor.sl'))
	maker = makeData.pyMaker.gradeMaker.PyMaker(*psList)
	maker.makeToPyFile()
	hotUpdate.update("grade")
	ep.rpcTips("生成评分配置表OK")

def makePetPointAllot(ep):
	'''异兽属性分配方案表
	'''
	psList = []
	psList.append(txtParser.multiparser.cTxtParser("gdData","data/sl/petPointAllot.sl"))
	mk=pyMaker.cPyMaker("data/py/petPointAllot.py",*psList)
	mk.makeToPyFile()
	ep.rpcTips("异兽属性分配方案表")

def baseConfig(ep):
	'''基础配置表
	'''
	psList = []
	psList.append(makeData.txtParser.kvParser.cTxtParser("gdData", "data/sl/baseConfig.sl"))
	mk = pyMaker.cPyMaker("data/py/baseConfigData.py", *psList)
	mk.makeToPyFile()
	hotUpdate.update('baseConfigData')
	ep.rpcTips('生成基础配置表OK')

import sys
import types
import hotUpdate
import txtParser
import txtParser.launchParser
import txtParser.configparser
import txtParser.pricelistparser
import txtParser.trapdistributeparser
import txtParser.mstdistributeparser
import txtParser.randnameparser
import txtParser.ExchangeParser
import txtParser.msttrapdistributeparser
import txtParser.activityLaunchParser
import txtParser.equipRandomParser
import txtParser.multiparser
import txtParser.singleparser
import txtParser.groupparser
import txtParser.chatparser
import txtParser.propsparser
import txtParser.teamTargetParser
import pyMaker
import pyMaker.activitymaker
import pyMaker.buffmaker
import pyMaker.lineupmaker
import pyMaker.statemaker
import txtParser.configparser
import txtParser.tradeparser1
import txtParser.tradeparser2
import txtParser.listparser
import txtParser.giftbagparser
import makeData.pyMaker.answerMaker
import makeData.txtParser.kvParser
import txtParser.buddyparser
import txtParser.treasureshopparser
import txtParser.dictParser