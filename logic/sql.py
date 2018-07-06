#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#SQL统一放在这里,便于检查性能差的语句

#表名:一定要用小写,断词用下划线,因为很多常用的客户端无法创建出大写表名的表(SQLyog,MySQL Workbench)
#字段名:用小驼峰命名,遵循已有代码风格
#执行mysql对于字符类型请用单引号括起来.因为dumps后的字符串中已经有双引号

#注意事项：sql关键字请用大写,不要用select这样的小写,大写sublime text编辑器可以语法高亮
PROPS_SELECT='SELECT data FROM props WHERE roleId={}'
PROPS_UPDATE='UPDATE props SET data=\'{}\' WHERE roleId={}'
PROPS_INSERT='INSERT INTO props (roleId,data)VALUES({},\'{}\')'
PROPS_DELETE='DELETE FROM props WHERE roleId={}'

EQUIP_SELECT='SELECT data FROM equip WHERE roleId={}'
EQUIP_UPDATE='UPDATE equip SET data=\'{}\' WHERE roleId={}'
EQUIP_INSERT='INSERT INTO equip (roleId,data)VALUES({},\'{}\')'
EQUIP_DELETE='DELETE FROM equip WHERE roleId={}'

TASK_SELECT='SELECT data FROM task WHERE roleId={}'
TASK_UPDATE='UPDATE task SET data=\'{}\' WHERE roleId={}'
TASK_INSERT='INSERT INTO task (roleId,data)VALUES({},\'{}\')'
TASK_DELETE='DELETE FROM task WHERE roleId={}'

LAZY_SELECT='SELECT data FROM lazy WHERE roleId={}'
LAZY_UPDATE='UPDATE lazy SET data=\'{}\' WHERE roleId={}'
LAZY_INSERT='INSERT INTO lazy (roleId,data)VALUES({},\'{}\')'
LAZY_DELETE='DELETE FROM lazy WHERE roleId={}'

ACTIVE_SELECT='SELECT data FROM active WHERE roleId={}'
ACTIVE_UPDATE='UPDATE active SET data=\'{}\' WHERE roleId={}'
ACTIVE_INSERT='INSERT INTO active (roleId,data)VALUES({},\'{}\')'
ACTIVE_DELETE='DELETE FROM active WHERE roleId={}'

CYCLE_SELECT='SELECT data FROM cycle WHERE roleId={}'
CYCLE_UPDATE='UPDATE cycle SET data=\'{}\' WHERE roleId={}'
CYCLE_INSERT='INSERT INTO cycle (roleId,data)VALUES({},\'{}\')'
CYCLE_DELETE='DELETE FROM cycle WHERE roleId={}'

#技能
SKILL_SELECT='SELECT data FROM skill WHERE roleId={}'
SKILL_UPDATE='UPDATE skill SET data=\'{}\' WHERE roleId={}'
SKILL_INSERT='INSERT INTO skill (roleId,data)VALUES({},\'{}\')'
SKILL_DELETE='DELETE FROM skill WHERE roleId={}'

#阵法
LINEUP_SELECT='SELECT data FROM lineup WHERE roleId={}'
LINEUP_UPDATE='UPDATE lineup SET data=\'{}\' WHERE roleId={}'
LINEUP_INSERT='INSERT INTO lineup (roleId,data) VALUES({},\'{}\')'
LINEUP_DELETE='DELETE FROM lineup WHERE roleId={}'

ROLE_MULTI_FIELD1_SELECT='SELECT name,exp,lv,pro,wp,gold,status,leagueRank,arenaPoint,voucher FROM role_multi_field1 WHERE roleId={}'#后期加多一个是否已被删除标志
ROLE_MULTI_FIELD1_UPDATE='UPDATE role_multi_field1 SET exp={},lv={},pro={},wp={},gold={},arenaPoint={},voucher={} WHERE roleId={}'
ROLE_MULTI_FIELD1_INSERT='INSERT INTO role_multi_field1(registerAppId,userSource,account,roleId,name,exp,lv,pro,wp,gold,status,leagueRank,arenaPoint,voucher,createTime)VALUES(\'{}\',\'{}\',\'{}\',{},\'{}\',{},{},{},{},{},{},{},{},{},sysdate())'
ROLE_MULTI_FIELD1_DELETE='DELETE FROM role_multi_field1 WHERE roleId={}'
ROLE_SET_NAME='UPDATE role_multi_field1 SET name=\'{}\' WHERE roleId={}'

UPDATE_ROLE_LOGINTINE='UPDATE role_multi_field1 SET loginTime = sysdate() WHERE roleId={}'
UPDATE_ROLE_LOGOUTTINE='UPDATE role_multi_field1 SET logoutTime = sysdate() WHERE roleId={}'

ALL_ROLE_ID_SELECT='SELECT roleId,lv,gold FROM role_multi_field1'

SEARCH_ROLE_NAME='SELECT roleId FROM role_multi_field1 WHERE name like \'{}%\''
SEARCH_ROLE_ID='SELECT roleId FROM role_multi_field1 WHERE roleId={}'
ROLE_NAME_SELECT='SELECT name FROM role_multi_field1'
EXIST_ROLE_NAME='SELECT roleId FROM role_multi_field1 WHERE name=\'{}\'' #角色名是否已经存在,name列要做索引
ROLE_LIST='SELECT roleId,name,pro,lv,wp FROM role_multi_field1 WHERE userSource=\'{}\' AND account=\'{}\'' #角色列表

ACCOUNT_JSON_INSERT='INSERT INTO account_json(userSource,account,data)VALUES(\'{}\',\'{}\',\'{}\')'
ACCOUNT_JSON_SELECT='SELECT data FROM account_json WHERE userSource=\'{}\' AND account=\'{}\''
ACCOUNT_JSON_UPDATE='UPDATE account_json SET data=\'{}\' WHERE userSource=\'{}\' AND account=\'{}\''
ACCOUNT_JSON_DELETE='DELETE FROM account_json WHERE userSource=\'{}\' AND account=\'{}\''

ACCOUNT_MULTI_FIELD_SELECT='SELECT diamond,vipLv,vipExp FROM account_multi_field WHERE userSource=\'{}\' AND account=\'{}\''#后期加多一个是否已被删除标志
ACCOUNT_MULTI_FIELD_UPDATE='UPDATE account_multi_field SET diamond={},vipLv={},vipExp={} WHERE userSource=\'{}\' AND account=\'{}\''
ACCOUNT_MULTI_FIELD_INSERT='INSERT INTO account_multi_field(userSource,account,diamond,vipLv,vipExp,createTime)VALUES(\'{}\',\'{}\',{},{},{},sysdate())'
ACCOUNT_MULTI_FIELD_DELETE='DELETE FROM account_multi_field WHERE userSource=\'{}\' AND account=\'{}\''

SINGLETON_SELECT='SELECT data FROM singleton WHERE name=\'{}\''
SINGLETON_UPDATE='UPDATE singleton SET data=\'{}\' WHERE name=\'{}\''
SINGLETON_INSERT='INSERT INTO singleton (name,data)VALUES(\'{}\',\'{}\')'
SINGLETON_DELETE='DELETE FROM singleton WHERE name=\'{}\''#按理没有删除的需求

MAX_ROLE_ID='SELECT max(roleId) FROM lazy WHERE mod(roleId,{})={}' #最大角色id
MAX_GUILD_ID='SELECT max(guildId) FROM guild WHERE mod(guildId,{})={}' #最大公会id

MAIL_SELECT='SELECT data FROM mail WHERE roleId={}'
MAIL_UPDATE='UPDATE mail SET data=\'{}\' WHERE roleId={}'
MAIL_INSERT='INSERT INTO mail (roleId,data)VALUES({},\'{}\')'
MAIL_DELETE='DELETE FROM mail WHERE roleId={}'

GOLD_COIN_SELECT='SELECT data FROM gold_coin WHERE roleId={}'
GOLD_COIN_UPDATE='UPDATE gold_coin SET data=\'{}\' WHERE roleId={}'
GOLD_COIN_INSERT='INSERT INTO gold_coin (roleId,data)VALUES({},\'{}\')'
GOLD_COIN_DELETE='DELETE FROM gold_coin WHERE roleId={}'


RESUME_SELECT='SELECT data FROM resume WHERE roleId={}'
RESUME_UPDATE='UPDATE resume SET data=\'{}\' WHERE roleId={}'
RESUME_INSERT='INSERT INTO resume (roleId,data)VALUES({},\'{}\')'
RESUME_DELETE='DELETE FROM resume WHERE roleId={}'

FRIEND_SELECT='SELECT data FROM friend WHERE roleId={}'
FRIEND_UPDATE='UPDATE friend SET data=\'{}\' WHERE roleId={}'
FRIEND_INSERT='INSERT INTO friend (roleId,data)VALUES({},\'{}\')'
FRIEND_DELETE='DELETE FROM friend WHERE roleId={}'

TITLE_SELECT='SELECT data FROM title WHERE roleId={}'
TITLE_UPDATE='UPDATE title SET data=\'{}\' WHERE roleId={}'
TITLE_INSERT='INSERT INTO title (roleId,data)VALUES({},\'{}\')'
TITLE_DELETE='DELETE FROM title WHERE roleId={}'

GUILD_SELECT='SELECT data FROM guild WHERE guildId={}'
GUILD_UPDATE='UPDATE guild SET data=\'{}\' WHERE guildId={}'
GUILD_INSERT='INSERT INTO guild (guildId,data)VALUES({},\'{}\')'
GUILD_DELETE='DELETE FROM guild WHERE guildId={}'

BUFF_INSERT='INSERT INTO buff (roleId,data)VALUES({},\'{}\')'
BUFF_SELECT='SELECT data FROM buff WHERE roleId={}'
BUFF_UPDATE='UPDATE buff SET data=\'{}\' WHERE roleId={}'
BUFF_DELETE='DELETE FROM buff WHERE roleId={}'

#宠物容器
PET_CTN_SELECT='SELECT data FROM pet WHERE roleId={}'
PET_CTN_UPDATE='UPDATE pet SET data=\'{}\' WHERE roleId={}'
PET_CTN_INSERT='INSERT INTO pet (roleId,data)VALUES({},\'{}\')'
PET_CTN_DELETE='DELETE FROM pet WHERE roleId={}'

#助战伙伴
BUDDY_CTN_SELECT='SELECT data FROM buddy WHERE roleId={}'
BUDDY_CTN_UPDATE='UPDATE buddy SET data=\'{}\' WHERE roleId={}'
BUDDY_CTN_INSERT='INSERT INTO buddy (roleId,data)VALUES({},\'{}\')'
BUDDY_CTN_DELETE='DELETE FROM buddy WHERE roleId={}'

#活动
ACTIVITY_SELECT='SELECT data FROM activity WHERE activityId={}'
ACTIVITY_UPDATE='UPDATE activity SET data=\'{}\' WHERE activityId={}'
ACTIVITY_INSERT='INSERT INTO activity (activityId,data)VALUES({},\'{}\')'
ACTIVITY_DELETE='DELETE FROM activity WHERE activityId={}'

#仓库
STORAGE_SELECT='SELECT data FROM storage WHERE roleId={}'
STORAGE_UPDATE='UPDATE storage SET data=\'{}\' WHERE roleId={}'
STORAGE_INSERT='INSERT INTO storage (roleId,data)VALUES({},\'{}\')'
STORAGE_DELETE='DELETE FROM storage WHERE roleId={}'

#临时背包
NUMEN_BAG_SELECT='SELECT data FROM numen_bag WHERE roleId={}'
NUMEN_BAG_UPDATE='UPDATE numen_bag SET data=\'{}\' WHERE roleId={}'
NUMEN_BAG_INSERT='INSERT INTO numen_bag (roleId,data)VALUES({},\'{}\')'
NUMEN_BAG_DELETE='DELETE FROM numen_bag WHERE roleId={}'

#状态
STATE_SELECT='SELECT data FROM state WHERE roleId={}'
STATE_UPDATE='UPDATE state SET data=\'{}\' WHERE roleId={}'
STATE_INSERT='INSERT INTO state (roleId, data)VALUES({}, \'{}\')'
STATE_DELETE='DELETE FROM state WHERE roleId={}'

#对白
WORDS_SELECT='SELECT data FROM words WHERE roleId={}'
WORDS_UPDATE='UPDATE words SET data=\'{}\' WHERE roleId={}'
WORDS_INSERT='INSERT INTO words (roleId, data)VALUES({}, \'{}\')'
WORDS_DELETE='DELETE FROM words WHERE roleId={}'

#离线玩家
OFFLINE_SELECT='SELECT data FROM offline WHERE roleId={}'
OFFLINE_UPDATE='UPDATE offline SET data=\'{}\' WHERE roleId={}'
OFFLINE_INSERT='INSERT INTO offline (roleId,data)VALUES({},\'{}\')'
OFFLINE_DELETE='DELETE FROM offline WHERE roleId={}'

#阵眼
EYE_SELECT='SELECT data FROM eye WHERE roleId={}'
EYE_UPDATE='UPDATE eye SET data=\'{}\' WHERE roleId={}'
EYE_INSERT='INSERT INTO eye (roleId,data)VALUES({},\'{}\')'
EYE_DELETE='DELETE FROM eye WHERE roleId={}'

#成就
ACHV_SELECT='SELECT data FROM achv WHERE roleId={}'
ACHV_UPDATE='UPDATE achv SET data=\'{}\' WHERE roleId={}'
ACHV_INSERT='INSERT INTO achv (roleId,data)VALUES({},\'{}\')'
ACHV_DELETE='DELETE FROM achv WHERE roleId={}'

#坐骑
RIDE_CTN_SELECT='SELECT data FROM ride WHERE roleId={}'
RIDE_CTN_UPDATE='UPDATE ride SET data=\'{}\' WHERE roleId={}'
RIDE_CTN_INSERT='INSERT INTO ride (roleId,data)VALUES({},\'{}\')'
RIDE_CTN_DELETE='DELETE FROM ride WHERE roleId={}'

'''
1. ujson把字符串是转为双引号"括起来的
2. mysql与ujson都是用\表示转义字符的前导符.

	a. 对于" ,入库没问题,出库有问题.ujson会转义成\"返回.mysql执行时又会把\给去掉,比如{"content":""abc"},被ujson反序列化时会失败.

	b. 对于' ,入库有问题.ujson对单引号就不转义了,原样返回,但是执行sql时出错,和外层的sql语句本身的'误匹配了
		例如: UPDATE resume SET data='{2:"abc'xyz"}' WHERE roleId=211

	c. 对于\ ,入库没问题,出库有问题.ujson会转成\\ ,但是入库时被mysql转成\了,{"content":"\zzz"},被ujson反序列化时,不认识\z会报错

	d. 对于/ ,没有问题,入库与出库都没有问题.



'''