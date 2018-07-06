#-*-coding:utf-8-*-

WORDS_STAR=1      #登场
WORDS_COMMAND=2   #出招
WORDS_VIC=3       #挨打
WORDS_PROTECT=4   #保护
WORDS_DEAD=5      #倒地
WORDS_PROPS=6     #使用道具
WORDS_ESCAPE=7    #逃跑
WORDS_ROLE_DEAD=8 #主人倒地
WORDS_MONSTER_DEAD=10#怪物倒地
WORDS_BUFF_REMOVE=11#BUFF消失

eventToStr = {
	WORDS_STAR:"登场",
	WORDS_COMMAND:"出招",
	WORDS_VIC:"挨打",
	WORDS_PROTECT:"保护",
	WORDS_DEAD:"倒地",
	WORDS_PROPS:"使用道具",
	WORDS_ESCAPE:"逃跑失败",
	WORDS_ROLE_DEAD:"主人倒地",
	WORDS_MONSTER_DEAD:"怪物倒地",
	WORDS_BUFF_REMOVE:"BUFF消失"
}

strToEvent = {
	"登场":WORDS_STAR,
	"换宠":WORDS_STAR,
	"出招":WORDS_COMMAND,
	"挨打":WORDS_VIC,
	"保护":WORDS_PROTECT,
	"倒地":WORDS_DEAD,
	"使用道具":WORDS_PROPS,
	"逃跑失败":WORDS_ESCAPE,
}