#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
def getConfig(iNo,sKey,uDefault=0):
	if iNo not in gdData:
		raise PlannerError,'不存在编号为{}的npc'.format(iNo)
	return gdData[iNo].get(sKey,uDefault)

#导表开始
gdData={
	10101:{"名字":"齐漱溟","称号":"蜀山掌教","造型":"4502(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1070,8,44,4],"对白编号":[101010,101011,101012],"类型":"导师","职业":11,"旁边":[1070,12,42]},
	10102:{"名字":"唐缺","称号":"唐门掌门","造型":"4006(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1040,59,9,6],"对白编号":[101020,101021,101022],"类型":"导师","职业":12,"旁边":[1040,54,7]},
	10103:{"名字":"林燕南","称号":"武林盟盟主","造型":"4003(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1030,68,53,4],"对白编号":[101030,101031,101032],"类型":"导师","职业":13,"旁边":[1030,73,48]},
	10104:{"名字":"鸠盘婆","称号":"苗疆大族长","造型":"4509(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1060,50,44,4],"对白编号":[101040,101041,101042],"类型":"导师","职业":14,"旁边":[1060,55,41]},
	10105:{"名字":"尸毗老人","称号":"魔宫至尊","造型":"4502(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2040,87,70,4],"对白编号":[101050,101051,101052],"类型":"导师","职业":15,"旁边":[2040,90,64]},
	10106:{"名字":"白眉禅师","称号":"佛门方丈","造型":"1611(0,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2030,66,97,6],"对白编号":[101060,101061,101062,101063],"类型":"导师","职业":16,"旁边":[2030,59,96]},
	10201:{"名字":"卖货郎","造型":"2005(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1130,21,52,4],"对白编号":[102010,102011,102012],"类型":"商店"},
	10202:{"名字":"染娘子","称号":"染色师","造型":"2002(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1130,51,18,4],"对白编号":[102020,102021],"类型":"染色"},
	10203:{"名字":"岳擎天","称号":"铁匠","造型":"2001(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1130,59,57,6],"对白编号":[102030,102031,102032],"类型":"商店"},
	10204:{"名字":"唐百草","称号":"药剂师","造型":"2004(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1130,16,41,4],"对白编号":[102040,102041,102042,102043],"类型":"商店"},
	10205:{"名字":"徐商贾","称号":"交易所","造型":"4504(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1130,180,75,6],"对白编号":[102050,102051,102052],"类型":"交易"},
	10206:{"名字":"花想容","称号":"节日礼物","造型":"3009(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1130,65,93,6],"对白编号":[102060],"类型":"节日礼物"},
	10207:{"名字":"江大桥","称号":"竞技场","造型":"2007(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1130,135,31,6],"对白编号":[102070,102071,102072],"类型":"竞技场"},
	10208:{"名字":"齐霞儿","称号":"异兽仙子","造型":"4508(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1130,75,33,4],"对白编号":[102080,102081,102082],"类型":"宠物任务"},
	10209:{"名字":"史镖头","称号":"运镖","造型":"2003(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1130,55,48,6],"对白编号":[102090],"类型":"运镖"},
	10210:{"名字":"凌云僧","称号":"接引道人","造型":"4004(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1130,169,116,6],"对白编号":[102100],"类型":"传送","传送":(2030,13,105,4)},
	10211:{"名字":"慧珠","称号":"探宝仙子","造型":"1621(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1130,144,96,6],"对白编号":[102110,102111],"类型":"探宝"},
	10212:{"名字":"云游脚僧","称号":"副本","造型":"1611(0,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1130,80,84,6],"对白编号":[102120],"类型":"副本"},
	10213:{"名字":"宝相夫人","称号":"兑换神兽","造型":"4508(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1030,33,58,6],"对白编号":[102130,102131],"类型":"兑换神兽"},
	10214:{"名字":"上官红","称号":"天问主事","造型":"4002(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1030,101,60,4],"对白编号":[102140],"类型":"投注献花"},
	10215:{"名字":"红尘道姑","称号":"入世修行","造型":"2002(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1030,18,39,6],"对白编号":[102150],"类型":"任务链"},
	10216:{"名字":"鬼阵子","称号":"阵眼兑换","造型":"2009(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1030,70,37,2],"对白编号":[102160],"类型":"兑换阵眼"},
	20201:{"名字":"周云从","造型":"2005(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1130,35,66,6],"对白编号":[202010,202011,202012]},
	20202:{"名字":"张玉珍","造型":"4508(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1130,49,68,6],"对白编号":[202020,202021,202022]},
	20203:{"名字":"老陈","称号":"猎户","造型":"2003(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1130,26,106,6],"对白编号":[202030,202031]},
	20204:{"名字":"小猴子","造型":"3007(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1130,25,107,6],"对白编号":[202040,202041]},
	20205:{"名字":"富家小姐","造型":"1221(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1130,148,44,6],"对白编号":[202050,202051,202052]},
	20206:{"名字":"万里追","称号":"衙役","造型":"4003(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1130,93,71,4],"对白编号":[202060,202061,202062]},
	20207:{"名字":"异兽","造型":"3004(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1130,71,32,2],"对白编号":[202070,202071,202072]},
	20208:{"名字":"周府台","造型":"4504(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1130,144,81,6],"对白编号":[202080,202081,202082]},
	10301:{"名字":"玄皇极","称号":"全知道人","造型":"4006(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1030,56,25,6],"对白编号":[103010,103011,103012],"类型":"每日答题"},
	20301:{"名字":"小虎儿","造型":"2006(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1030,87,40,6],"对白编号":[203010,203011,203012,203013,203014,203015]},
	20302:{"名字":"小翠儿","造型":"2008(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1030,85,38,2],"对白编号":[203020,203021,203022,203023,203024]},
	20303:{"名字":"莫道","称号":"游方僧","造型":"1611(0,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1030,28,34,6],"对白编号":[203030,203031,203032]},
	20304:{"名字":"黄阿佬","称号":"私盐贩子","造型":"2007(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1030,88,59,4],"对白编号":[203040,203041,203042]},
	10401:{"名字":"顽石大师","称号":"降魔","造型":"1621(1,1,1,1,1,1)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1130,142,68,4],"对白编号":[104010,104011,104012],"类型":"降魔"},
	10402:{"名字":"餐霞大师","称号":"秘册","造型":"3009(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1130,165,56,8],"对白编号":[104020,104021,104022],"类型":"宝图"},
	20401:{"名字":"芝仙","造型":"3006(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1140,10,51,4],"对白编号":[204010,204011,204012]},
	20402:{"名字":"吴文琪","称号":"女空空","造型":"4002(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1140,59,14,6],"对白编号":[204020,204021,204022,204023]},
	20501:{"名字":"笑和尚","造型":"4004(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1070,8,11,4],"对白编号":[205010,205011,205012]},
	10601:{"名字":"唐问","造型":"2007(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[1040,19,22,6],"对白编号":[106010,106011,106012],"类型":"五宝"},
	20601:{"名字":"唐解元","造型":"4504(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1040,22,38,4],"对白编号":[206010,206011,206012]},
	20602:{"名字":"钱永健","称号":"唐门弟子","造型":"4502(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1040,67,45,6],"对白编号":[206020,206021,206022]},
	20603:{"名字":"健步雀","造型":"3005(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1040,56,25,6],"对白编号":[206030,206031]},
	20701:{"名字":"小妖甲","造型":"3008(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1060,77,18,6],"对白编号":[207010,207011]},
	20702:{"名字":"小妖乙","造型":"3006(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1060,17,21,4],"对白编号":[207020,207021]},
	20801:{"名字":"知非禅师","称号":"金佛寺方丈","造型":"1611(0,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[2030,34,80,5],"对白编号":[208010,208011,208012]},
	20802:{"名字":"绝尊者","造型":"4005(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[2030,30,54,4],"对白编号":[208020,208021,208022]},
	20803:{"名字":"老猴子","造型":"3007(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[2030,21,19,4],"对白编号":[208030,208031,208032]},
	20901:{"名字":"石翁仲","造型":"5001(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[2040,93,17,6],"对白编号":[209010,209011,209012]},
	20902:{"名字":"杀手","造型":"2007(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[2040,42,19,6],"对白编号":[209020,209021,209022]},
	20903:{"名字":"小女孩","造型":"2008(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[2040,46,19,6],"对白编号":[209030,209031,209032]},
	10901:{"名字":"九海诚","称号":"幻境守门人","造型":"4504(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2040,108,62,6],"对白编号":[109010],"类型":"试炼幻境"},
	21001:{"名字":"宣老头","造型":"2010(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1150,27,47,4],"对白编号":[210010,210011]},
	21002:{"名字":"郎不申","称号":"衙役","造型":"4003(0,1,0,0,0,0)","染色":"0,0,0,0,0","小地图颜色":2,"坐标":[1150,94,20,6],"对白编号":[210020,210021]},
	30001:{"名字":"蜀山男1","造型":"1111(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,46,57,1],"对白编号":[300001]},
	30002:{"名字":"蜀山男2","造型":"1111(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,49,57,2],"对白编号":[300001]},
	30003:{"名字":"蜀山男3","造型":"1111(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,52,57,3],"对白编号":[300001]},
	30004:{"名字":"蜀山男4","造型":"1111(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,55,57,4],"对白编号":[300001]},
	30005:{"名字":"蜀山男5","造型":"1111(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,58,57,5],"对白编号":[300001]},
	30006:{"名字":"蜀山男6","造型":"1111(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,61,57,1],"动作":2,"对白编号":[300001]},
	30007:{"名字":"蜀山男7","造型":"1111(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,64,57,2],"动作":2,"对白编号":[300001]},
	30008:{"名字":"蜀山男8","造型":"1111(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,67,57,3],"动作":2,"对白编号":[300001]},
	30009:{"名字":"蜀山男9","造型":"1111(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,70,57,4],"动作":2,"对白编号":[300001]},
	30010:{"名字":"蜀山男10","造型":"1111(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,73,57,5],"动作":2,"对白编号":[300001]},
	30011:{"名字":"蜀山女1","造型":"1121(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,86,55,1],"对白编号":[300001]},
	30012:{"名字":"蜀山女2","造型":"1121(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,88,54,2],"对白编号":[300001]},
	30013:{"名字":"蜀山女3","造型":"1121(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,90,53,3],"对白编号":[300001]},
	30014:{"名字":"蜀山女4","造型":"1121(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,92,52,4],"对白编号":[300001]},
	30015:{"名字":"蜀山女5","造型":"1121(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,94,51,5],"对白编号":[300001]},
	30016:{"名字":"蜀山女6","造型":"1121(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,96,50,1],"动作":2,"对白编号":[300001]},
	30017:{"名字":"蜀山女7","造型":"1121(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,98,49,2],"动作":2,"对白编号":[300001]},
	30018:{"名字":"蜀山女8","造型":"1121(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,100,48,3],"动作":2,"对白编号":[300001]},
	30019:{"名字":"蜀山女9","造型":"1121(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,102,47,4],"动作":2,"对白编号":[300001]},
	30020:{"名字":"蜀山女10","造型":"1121(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,104,46,5],"动作":2,"对白编号":[300001]},
	30021:{"名字":"唐门男1","造型":"1211(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,106,40,1],"对白编号":[300001]},
	30022:{"名字":"唐门男2","造型":"1211(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,106,38,2],"对白编号":[300001]},
	30023:{"名字":"唐门男3","造型":"1211(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,106,36,3],"对白编号":[300001]},
	30024:{"名字":"唐门男4","造型":"1211(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,106,34,4],"对白编号":[300001]},
	30025:{"名字":"唐门男5","造型":"1211(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,106,32,5],"对白编号":[300001]},
	30026:{"名字":"唐门男6","造型":"1211(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,106,30,1],"动作":2,"对白编号":[300001]},
	30027:{"名字":"唐门男7","造型":"1211(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,106,28,2],"动作":2,"对白编号":[300001]},
	30028:{"名字":"唐门男8","造型":"1211(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,106,26,3],"动作":2,"对白编号":[300001]},
	30029:{"名字":"唐门男9","造型":"1211(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,106,24,4],"动作":2,"对白编号":[300001]},
	30030:{"名字":"唐门男10","造型":"1211(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,106,22,5],"动作":2,"对白编号":[300001]},
	30031:{"名字":"唐门女1","造型":"1221(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,106,20,1],"对白编号":[300001]},
	30032:{"名字":"唐门女2","造型":"1221(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,96,16,2],"对白编号":[300001]},
	30033:{"名字":"唐门女3","造型":"1221(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,93,16,3],"对白编号":[300001]},
	30034:{"名字":"唐门女4","造型":"1221(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,90,16,4],"对白编号":[300001]},
	30035:{"名字":"唐门女5","造型":"1221(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,87,16,5],"对白编号":[300001]},
	30036:{"名字":"唐门女6","造型":"1221(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,84,16,1],"动作":2,"对白编号":[300001]},
	30037:{"名字":"唐门女7","造型":"1221(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,81,16,2],"动作":2,"对白编号":[300001]},
	30038:{"名字":"唐门女8","造型":"1221(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,78,16,3],"动作":2,"对白编号":[300001]},
	30039:{"名字":"唐门女9","造型":"1221(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,75,16,4],"动作":2,"对白编号":[300001]},
	30040:{"名字":"唐门女10","造型":"1221(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,72,16,5],"动作":2,"对白编号":[300001]},
	30041:{"名字":"武林男1","造型":"1311(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,70,16,1],"对白编号":[300001]},
	30042:{"名字":"武林男2","造型":"1311(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,68,16,2],"对白编号":[300001]},
	30043:{"名字":"武林男3","造型":"1311(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,66,16,3],"对白编号":[300001]},
	30044:{"名字":"武林男4","造型":"1311(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,64,16,4],"对白编号":[300001]},
	30045:{"名字":"武林男5","造型":"1311(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,62,16,5],"对白编号":[300001]},
	30046:{"名字":"武林男6","造型":"1311(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,60,16,1],"动作":2,"对白编号":[300001]},
	30047:{"名字":"武林男7","造型":"1311(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,58,16,2],"动作":2,"对白编号":[300001]},
	30048:{"名字":"武林男8","造型":"1311(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,56,16,3],"动作":2,"对白编号":[300001]},
	30049:{"名字":"武林男9","造型":"1311(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,54,16,4],"动作":2,"对白编号":[300001]},
	30050:{"名字":"武林男10","造型":"1311(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,52,16,5],"动作":2,"对白编号":[300001]},
	30051:{"名字":"武林女1","造型":"1321(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,50,18,1],"对白编号":[300001]},
	30052:{"名字":"武林女2","造型":"1321(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,47,19,2],"对白编号":[300001]},
	30053:{"名字":"武林女3","造型":"1321(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,44,20,3],"对白编号":[300001]},
	30054:{"名字":"武林女4","造型":"1321(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,41,21,4],"对白编号":[300001]},
	30055:{"名字":"武林女5","造型":"1321(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,38,22,5],"对白编号":[300001]},
	30056:{"名字":"武林女6","造型":"1321(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,35,23,1],"动作":2,"对白编号":[300001]},
	30057:{"名字":"武林女7","造型":"1321(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,32,24,2],"动作":2,"对白编号":[300001]},
	30058:{"名字":"武林女8","造型":"1321(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,29,25,3],"动作":2,"对白编号":[300001]},
	30059:{"名字":"武林女9","造型":"1321(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,26,26,4],"动作":2,"对白编号":[300001]},
	30060:{"名字":"武林女10","造型":"1321(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,23,27,5],"动作":2,"对白编号":[300001]},
	30061:{"名字":"苗疆男1","造型":"1411(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,18,29,1],"对白编号":[300001]},
	30062:{"名字":"苗疆男2","造型":"1411(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,18,30,2],"对白编号":[300001]},
	30063:{"名字":"苗疆男3","造型":"1411(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,19,31,3],"对白编号":[300001]},
	30064:{"名字":"苗疆男4","造型":"1411(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,20,32,4],"对白编号":[300001]},
	30065:{"名字":"苗疆男5","造型":"1411(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,21,33,5],"对白编号":[300001]},
	30066:{"名字":"苗疆男6","造型":"1411(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,22,34,1],"动作":2,"对白编号":[300001]},
	30067:{"名字":"苗疆男7","造型":"1411(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,23,35,2],"动作":2,"对白编号":[300001]},
	30068:{"名字":"苗疆男8","造型":"1411(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,24,36,3],"动作":2,"对白编号":[300001]},
	30069:{"名字":"苗疆男9","造型":"1411(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,25,37,4],"动作":2,"对白编号":[300001]},
	30070:{"名字":"苗疆男10","造型":"1411(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,26,38,5],"动作":2,"对白编号":[300001]},
	30071:{"名字":"苗疆女1","造型":"1421(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,28,40,1],"对白编号":[300001]},
	30072:{"名字":"苗疆女2","造型":"1421(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,29,41,2],"对白编号":[300001]},
	30073:{"名字":"苗疆女3","造型":"1421(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,30,42,3],"对白编号":[300001]},
	30074:{"名字":"苗疆女4","造型":"1421(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,31,43,4],"对白编号":[300001]},
	30075:{"名字":"苗疆女5","造型":"1421(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,32,44,5],"对白编号":[300001]},
	30076:{"名字":"苗疆女6","造型":"1421(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,33,45,1],"动作":2,"对白编号":[300001]},
	30077:{"名字":"苗疆女7","造型":"1421(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,34,46,2],"动作":2,"对白编号":[300001]},
	30078:{"名字":"苗疆女8","造型":"1421(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,35,47,3],"动作":2,"对白编号":[300001]},
	30079:{"名字":"苗疆女9","造型":"1421(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,36,48,4],"动作":2,"对白编号":[300001]},
	30080:{"名字":"苗疆女10","造型":"1421(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,37,49,5],"动作":2,"对白编号":[300001]},
	30081:{"名字":"魔宫男1","造型":"1511(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,46,55,1],"对白编号":[300001]},
	30082:{"名字":"魔宫男2","造型":"1511(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,49,55,2],"对白编号":[300001]},
	30083:{"名字":"魔宫男3","造型":"1511(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,52,55,3],"对白编号":[300001]},
	30084:{"名字":"魔宫男4","造型":"1511(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,55,55,4],"对白编号":[300001]},
	30085:{"名字":"魔宫男5","造型":"1511(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,58,55,5],"对白编号":[300001]},
	30086:{"名字":"魔宫男6","造型":"1511(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,61,55,1],"动作":2,"对白编号":[300001]},
	30087:{"名字":"魔宫男7","造型":"1511(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,64,55,2],"动作":2,"对白编号":[300001]},
	30088:{"名字":"魔宫男8","造型":"1511(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,67,55,3],"动作":2,"对白编号":[300001]},
	30089:{"名字":"魔宫男9","造型":"1511(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,70,55,4],"动作":2,"对白编号":[300001]},
	30090:{"名字":"魔宫男10","造型":"1511(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,73,55,5],"动作":2,"对白编号":[300001]},
	30091:{"名字":"魔宫女1","造型":"1521(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,96,14,1],"对白编号":[300001]},
	30092:{"名字":"魔宫女2","造型":"1521(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,93,14,2],"对白编号":[300001]},
	30093:{"名字":"魔宫女3","造型":"1521(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,90,14,3],"对白编号":[300001]},
	30094:{"名字":"魔宫女4","造型":"1521(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,87,14,4],"对白编号":[300001]},
	30095:{"名字":"魔宫女5","造型":"1521(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,84,14,5],"对白编号":[300001]},
	30096:{"名字":"魔宫女6","造型":"1521(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,81,14,1],"动作":2,"对白编号":[300001]},
	30097:{"名字":"魔宫女7","造型":"1521(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,78,14,2],"动作":2,"对白编号":[300001]},
	30098:{"名字":"魔宫女8","造型":"1521(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,75,14,3],"动作":2,"对白编号":[300001]},
	30099:{"名字":"魔宫女9","造型":"1521(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,72,14,4],"动作":2,"对白编号":[300001]},
	30100:{"名字":"魔宫女10","造型":"1521(1,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,70,14,5],"动作":2,"对白编号":[300001]},
	30101:{"名字":"佛门男1","造型":"1611(0,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,68,14,1],"对白编号":[300001]},
	30102:{"名字":"佛门男2","造型":"1611(0,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,66,14,2],"对白编号":[300001]},
	30103:{"名字":"佛门男3","造型":"1611(0,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,64,14,3],"对白编号":[300001]},
	30104:{"名字":"佛门男4","造型":"1611(0,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,62,14,4],"对白编号":[300001]},
	30105:{"名字":"佛门男5","造型":"1611(0,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,60,14,5],"对白编号":[300001]},
	30106:{"名字":"佛门男6","造型":"1611(0,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,58,14,1],"动作":2,"对白编号":[300001]},
	30107:{"名字":"佛门男7","造型":"1611(0,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,56,14,2],"动作":2,"对白编号":[300001]},
	30108:{"名字":"佛门男8","造型":"1611(0,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,54,14,3],"动作":2,"对白编号":[300001]},
	30109:{"名字":"佛门男9","造型":"1611(0,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,52,14,4],"动作":2,"对白编号":[300001]},
	30110:{"名字":"佛门男10","造型":"1611(0,1,1,1,1,0)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,50,14,5],"动作":2,"对白编号":[300001]},
	30111:{"名字":"佛门女1","造型":"1621(1,1,1,1,1,1)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,37,24,1],"对白编号":[300001]},
	30112:{"名字":"佛门女2","造型":"1621(1,1,1,1,1,1)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,39,25,2],"对白编号":[300001]},
	30113:{"名字":"佛门女3","造型":"1621(1,1,1,1,1,1)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,41,26,3],"对白编号":[300001]},
	30114:{"名字":"佛门女4","造型":"1621(1,1,1,1,1,1)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,43,27,4],"对白编号":[300001]},
	30115:{"名字":"佛门女5","造型":"1621(1,1,1,1,1,1)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,45,28,5],"对白编号":[300001]},
	30116:{"名字":"佛门女6","造型":"1621(1,1,1,1,1,1)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,47,29,1],"动作":2,"对白编号":[300001]},
	30117:{"名字":"佛门女7","造型":"1621(1,1,1,1,1,1)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,49,30,2],"动作":2,"对白编号":[300001]},
	30118:{"名字":"佛门女8","造型":"1621(1,1,1,1,1,1)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,51,31,3],"动作":2,"对白编号":[300001]},
	30119:{"名字":"佛门女9","造型":"1621(1,1,1,1,1,1)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,53,32,4],"动作":2,"对白编号":[300001]},
	30120:{"名字":"佛门女10","造型":"1621(1,1,1,1,1,1)","染色":"0,0,0,0,0","小地图颜色":1,"坐标":[2010,55,33,5],"动作":2,"对白编号":[300001]},
}
#导表结束

import npc
def afterHotUpdate():
	npc.init()#重新建立编号与模块的映射关系
