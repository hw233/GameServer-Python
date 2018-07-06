#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇

def getConfig(wordstype, iNo, iKey, uDefault=""):
	if wordstype == 1:
		return getPetWords(iNo,iKey,uDefault)
	elif wordstype == 2:
		return getBuddyWords(iNo,iKey,uDefault)

def getPetWords(iNo,iKey,uDefault=""):
	if iNo not in gdPetWords:
		raise PlannerError,'没有编号为{}的宠物默认闲话'.format(iNo)
	return gdPetWords[iNo].get(words.defines.eventToStr[iKey],uDefault)

def getBuddyWords(iNo,iKey,uDefault=""):
	if iNo not in gdBuddyWords:
		raise PlannerError,'没有编号为{}的伙伴默认闲话'.format(iNo)
	return gdBuddyWords[iNo].get(words.defines.eventToStr[iKey],uDefault)

def getProbability(sKey,uDefault=0):
	return gdProbability.get(sKey,uDefault)

#导表开始
gdProbability={
	"登场":0.1,
	"换宠":0.5,
	"出招":0.05,
	"挨打":0.05,
	"保护":0.5,
	"倒地":0.2,
	"主人倒地":0.2,
	"使用道具":0.5,
	"逃跑失败":0.5,
}

gdPetWords={
	1001:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1002:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1003:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1004:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1005:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1006:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1007:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1008:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1009:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1010:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1011:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1012:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1013:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1014:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1015:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1016:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1017:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1018:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1019:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	1020:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	2001:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	2002:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	2003:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
	2004:{"登场":"吼！该到我上场了","出招":"有机可乘！","挨打":"啊！真痛","保护":"不要害怕，有我在呢！","倒地":"可恨……","主人倒地":"主、主人啊！","使用道具":"先吃点药品吧","逃跑失败":"倒霉，要赶快跑啊！"},
}

gdBuddyWords={
	1001:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	1002:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	1003:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	1004:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	2001:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	2002:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	2003:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	2004:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	3001:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	3002:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	3003:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	3004:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	4001:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	4002:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	4003:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	4004:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	5001:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	5002:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	5003:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
	5004:{"登场":"这里是我的战场","出招":"看我降魔除妖！","挨打":"哼，这点伤……","保护":"放心，有我","倒地":"我、我还能打……","主人倒地":"接下来交给我吧","使用道具":"先休息一下","逃跑失败":"倒霉！"},
}
#导表结束


import words.defines