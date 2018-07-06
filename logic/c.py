#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#c -> const,系统常量,如果要被策划控制的数据不要放到这里
import sys

LINE_SEP="\n"

INIT_LV=0 #角色初始等级

SQL_TIMEOUT=2 #mysql执行超时秒数
MAX_ROLE_ID=2**30 #最大的角色id.(其他场景实体的id在这个基础上进行递增)

WEAR_EQUIP_POS_START=1 #穿在身上的装备区起始位置
WEAR_EQUIP_POS_STOP=8 #穿在身上的装备区结束位置

UNKNOWN=0 #未知的
INVALID=0 #非法的,无效的
#职业
PRO1,PRO2,PRO3,PRO4,PRO5,PRO10=1,2,3,4,5,10
PRO_STR={UNKNOWN:'任意职业',PRO1:'战士',PRO2:'弓箭手',PRO3:'法师',PRO4:'刺客',PRO5:'bb',PRO10:'古代人'}

#性别
MALE,FEMALE=1,2

#战斗属性
ATT				=1	#攻击
DEF				=2	#防御
CRIT			=3 	#暴击
HIT				=4 	#命中
DODGE			=5 	#闪避
SPIRIT			=6	#精神
HP_MAX			=7	#气血上限
MP_MAX			=8 	#魔法上限


ATTR_MAP1={'att':'攻击','def':'防御','crit':'暴击','hit':'命中','dodge':'闪避','spi':'精神','hpMax':'生命','mpMax':'魔法值'}
ATTR_MAP2={UNKNOWN:'未知属性',ATT:'攻击',DEF:'防御',CRIT:'暴击',HIT:'命中',DODGE:'闪避',SPIRIT:'精神',HP_MAX:'生命',MP_MAX:'魔法值'}
ATTR_MAP3={ATT:'att',DEF:'def',CRIT:'crit',HIT:'hit',DODGE:'dodge',SPIRIT:'spi',HP_MAX:'hpMax',MP_MAX:'mpMax'}
ATTR_MAP4={'att':ATT,'def':DEF,'crit':CRIT,'hit':HIT,'dodge':DODGE,'spi':SPIRIT,'hpMax':HP_MAX,'mpMax':MP_MAX}
ATTR_MAP5={'baseAtt':ATT,'baseHit':HIT,'baseDodge':DODGE}
ATTR_MAP6={'attaSpi':SPIRIT,'attaMpMax':MP_MAX,'attaCrit':CRIT}

#已穿上的装备
WEAR_EQUIP_POS_START	=1
WEAR_EQUIP_POS_STOP	= 8

EQUIP_WEAPON = 1 #武器
EQUIP_HAT  = 2 #帽子
EQUIP_FROCK = 3 #衣服
EQUIP_NECKLACE = 4 #项链
EQUIP_TROUSERS = 5 #裤子
EQUIP_SHOES = 6 #鞋子


EQUIP_STR={UNKNOWN:'未知',EQUIP_WEAPON:'武器',EQUIP_NECKLACE:'项链',EQUIP_FROCK:'衣服',EQUIP_TROUSERS:'裤子',EQUIP_HAT:'帽子',EQUIP_SHOES:'鞋子'}

PLAYER=1 #玩家
NPC=2 
MONSTER=3 #怪物
DOOR=4 #传送门


#全部赋值到 __builtins__ 模块中去.


#上限值,为了好理解,用一个变量来代替,用来配置一些大于某个值时用到
MAX=sys.maxint

#出生默认角色名
BORN_NAME='你'

#道具类型
# VOUCHER=1 #绑钻
PROPS_EQUIP=2

#新建角色出生场景
NEW_ROLE_BORN_NO=1130
NEW_ROLE_BORN_POS=101,63

EXP=4 #经验
GOLD=77 #游戏币
DIAMOND=88 #元宝/RMB/钻石
VOUCHER=99 #绑钻

#虚拟物品
VIR_ITEM={EXP:'经验',GOLD:'元宝',DIAMOND:'钻石',VOUCHER:'绑钻',}
VIR_ITEM_DESC={EXP:'经验',GOLD:'阿尔特里亚大陆通用的货币，永不贬值！',DIAMOND:'大陆上层社会流通的货币，是尊贵身份的象征。',VOUCHER:'绑钻',}
VIR_ICON={EXP:4,GOLD:77,DIAMOND:3,VOUCHER:3,}#包裹
