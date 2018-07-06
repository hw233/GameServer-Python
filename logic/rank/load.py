#-*-coding:utf-8-*-
from props.defines import *
from role.defines import *
import rank.roleFightPower
import rank.roleLv
import rank.guildFight
import rank.equipScore
import rank.petScore
import rank.racePoint
import rank.treasurePoint
import rank.fairylandTime
import rank.finalExam
import rank.firstExam
import rank.teamRacePoint


gdRankModInfo = {
	#综合实力榜
	101:{"mod":rank.roleFightPower, "name":"rank_school_all", "chineseName":"综合实力-总榜"},
	102:{"mod":rank.roleFightPower, "name":"rank_school_11", "school":11, "chineseName":"综合实力-蜀山"},
	103:{"mod":rank.roleFightPower, "name":"rank_school_12", "school":12, "chineseName":"综合实力-唐门"},
	104:{"mod":rank.roleFightPower, "name":"rank_school_13", "school":13, "chineseName":"综合实力-武林"},
	105:{"mod":rank.roleFightPower, "name":"rank_school_14", "school":14, "chineseName":"综合实力-苗疆"},
	106:{"mod":rank.roleFightPower, "name":"rank_school_15", "school":15, "chineseName":"综合实力-魔宫"},
	107:{"mod":rank.roleFightPower, "name":"rank_school_16", "school":16, "chineseName":"综合实力-佛门"},
	
	#练级狂人榜
	201:{"mod":rank.roleLv, "name":"rank_lv", "chineseName":"练级狂人榜"},
	
	#帮派排行榜
	301:{"mod":rank.guildFight, "name":"rank_guild", "chineseName":"帮派排行榜"},
	
	#装备排行榜
	401:{"mod":rank.equipScore, "name":"rank_equip_weapon", "chineseName":"装备-武器"},
	402:{"mod":rank.equipScore, "name":"rank_equip_clothes", "chineseName":"装备-衣服"},
	403:{"mod":rank.equipScore, "name":"rank_equip_head", "chineseName":"装备-帽子"},
	404:{"mod":rank.equipScore, "name":"rank_equip_necklace", "chineseName":"装备-饰品"},
	405:{"mod":rank.equipScore, "name":"rank_equip_blet", "chineseName":"装备-腰带"},
	406:{"mod":rank.equipScore, "name":"rank_equip_shoes", "chineseName":"装备-鞋子"},
	
	#宠物排行榜
	501:{"mod":rank.petScore, "name":"rank_pet_score_all", "chineseName":"宠物排行榜"},
	#宠物分类排行榜
	"pet_classify":{"mod":rank.petScore, "name":"rank_pet_score_{}", "chineseName":"宠物分类排行榜"},#rank_pet_score_宠物编号

	#竞技排行榜
	601:{"mod":rank.racePoint, "name":"rank_race_point", "chineseName":"竞技积分排行榜"},
	#组队竞技排行榜
	602:{"mod":rank.teamRacePoint, "name":"rank_teamrace_point_1", "chineseName":"组队竞技积分-化神组排行榜"},
	603:{"mod":rank.teamRacePoint, "name":"rank_teamrace_point_2", "chineseName":"组队竞技积分-元婴组排行榜"},
	604:{"mod":rank.teamRacePoint, "name":"rank_teamrace_point_3", "chineseName":"组队竞技积分-金丹组排行榜"},
	605:{"mod":rank.teamRacePoint, "name":"rank_teamrace_point_4", "chineseName":"组队竞技积分-筑基组排行榜"},

	#探宝排行
	701:{"mod":rank.treasurePoint, "name":"rank_treasure_point", "chineseName":"幸运探宝排行榜"},

	#试炼幻境
	801:{"mod":rank.fairylandTime, "name":"rank_race_fairyland", "chineseName":"试炼幻境排行榜"},

	#殿试/乡试
	901:{"mod":rank.finalExam, "name":"rank_finalExam", "chineseName":"殿试排行榜"},
	902:{"mod":rank.firstExam, "name":"rank_firstExam_20", "chineseName":"乡试排行榜"},
}


def getRankChineseName(iRankNo):
	return gdRankModInfo.get(iRankNo, {}).get("chineseName", "未知排行榜")

#综合实力榜
gdSchoolRank = {
	11:"rank_school_11",
	12:"rank_school_12",
	13:"rank_school_13",
	14:"rank_school_14",
	15:"rank_school_15",
	16:"rank_school_16",
}

#装备排行榜
gdEquipPosRank = {
	EQUIP_HEAD : "rank_equip_head",#头部
	EQUIP_NECKLACE : "rank_equip_necklace",#项链
	EQUIP_WEAPON : "rank_equip_weapon",#武器
	EQUIP_CLOTHES : "rank_equip_clothes",#衣服
	EQUIP_BELT : "rank_equip_blet",#裤子
	EQUIP_SHOES : "rank_equip_shoes",#鞋子
}
