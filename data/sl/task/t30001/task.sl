﻿编号	父任务编号	目标类型_S	图标	标题_S	简介_S	详情_S	奖励描述_S	前往脚本_S	初始化脚本_S
30001		寻人	0	师门-传话	传话给$target	替师父向$target传话，切莫耽误			E(9001,1001)
30002		巡逻战斗	1	师门-收集物品	去$scene收集$props	师门$props消耗过大，去$scene收集一些。			L(9003,1),ANLEI(1001,1002,9004)
30003		寻物	0	师门-寻找物品	去帮师父找个$props来(拥有$process)，上交高于$quality品质，可以获得额外经验奖励	师父准备斩妖除魔，急需$props（高于$quality品质），带上战场，快去准备！			B(1002,lv),E(master,1003),QU30
30004		寻物	0	师门-寻找物品	去帮师父找个$props来(拥有$process)	师父准备闭关炼药，急需$props作为药引，才能修炼丹药，请尽快找回来。			B(1001,lv),E(master,1004)
30005		寻人	1	师门-教训恶霸	恶霸$target又在为祸乡民，是时候出手教训了。	恶霸$target心术不正，学了点微末道术就出来鱼肉百姓，要好好教训他们了。			NE(9014,1005)
30006		寻人	0	师门-拜访别派	拜访别派掌门$target，熟悉别派能力	在世界上行走，知己知彼很重要，熟悉其他门派的长短处更是重中之重。			B(1003,notSchool)
30007		寻人	1	师门-清除叛徒	背叛师门的$target被发现行踪，前往消灭他	$target曾作出欺师灭祖的事情来，这些年一直在躲藏，如今有人发现他的踪迹，速去清理门户。			B(1004,school)
30008		寻人	1	师门-清除叛徒	背叛师门的$target被发现行踪，前往消灭他	$target曾作出欺师灭祖的事情来，这些年一直在躲藏，如今有人发现他的踪迹，速去清理门户。			B(1005,school)
30009		寻人	1	师门-清除叛徒	背叛师门的$target被发现行踪，前往消灭他	$target曾作出欺师灭祖的事情来，这些年一直在躲藏，如今有人发现他的踪迹，速去清理门户。			B(1006,school)
30010		寻人	1	师门-清除叛徒	背叛师门的$target被发现行踪，前往消灭他	$target曾作出欺师灭祖的事情来，这些年一直在躲藏，如今有人发现他的踪迹，速去清理门户。			B(1007,school)
30011		寻人	1	师门-清除叛徒	背叛师门的$target被发现行踪，前往消灭他	$target曾作出欺师灭祖的事情来，这些年一直在躲藏，如今有人发现他的踪迹，速去清理门户。			B(1008,school)
30000	30000	寻人	0	师门任务指引	师傅有重要的任务要交给你，请尽快找他	师傅有重要的任务要交给你，请尽快找他			E(master,3001)