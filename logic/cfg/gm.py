#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
import md5
import instruction

"""
各种用户来源
1000	内部测试账号
1		战法牧账号
2		腾讯账号
3		当乐
4		uc九游

"""

#(用户来源,账号):所属用户组
#一个用户可以属于多个用户组
gdGm={
	# #马昭
	('1000','123'):instruction.ADMIN|instruction.FAKE,#

	# ('1000','1026517067'):instruction.ADMIN|instruction.FAKE,	#账号:15920112342 密码:asdfghjkl
	# ('1000','781182612'):instruction.ADMIN|instruction.FAKE,	#盛大要求新加的账号
	# ('1000','933237548'):instruction.ADMIN|instruction.FAKE,	#
	# ('1000','41864641'):instruction.ADMIN|instruction.FAKE,
	# ('1000','40393157'):instruction.ADMIN|instruction.FAKE,
	# ('1000','802489894'):instruction.ADMIN|instruction.FAKE,
	# ('1000','1019981013'):instruction.ADMIN|instruction.FAKE,
	# ('1000','41784954'):instruction.ADMIN|instruction.FAKE,
	# ('1000','29552120'):instruction.ADMIN|instruction.FAKE,
	
	('1','asdfasdfasfadsf'):instruction.ADMIN|instruction.FAKE,#qq:462624080
	('2','asdfa65746'):instruction.ADMIN|instruction.FAKE,#
	('3','43527yha'):instruction.ADMIN|instruction.FAKE,#
	('1000','835577001'):instruction.ADMIN|instruction.FAKE,#	#测试人员
	#李四
	('1000','6353'):instruction.ADMIN|instruction.FAKE,#
	('1','gsfdghgs'):instruction.ADMIN|instruction.FAKE,#qq:3425453525
	('2','wretwrtw'):instruction.ADMIN|instruction.FAKE,#
	('3','twt453453435'):instruction.ADMIN|instruction.FAKE,#
	#张三
	('1000','552345'):instruction.FAKE|instruction.FAKE,#
	('1','234525'):instruction.FAKE|instruction.FAKE,#qq:56757456536
	('2','23452345'):instruction.FAKE|instruction.FAKE,#
	('3','3635635'):instruction.FAKE|instruction.FAKE,#

}

import db4ms

def autoInit():
	sSQl='SELECT userSource,account FROM gm'
	rs=db4ms.gConnectionPool.query(sSQl).rows
	for tAccount in rs:
		gdGm[tAccount]=instruction.ADMIN|instruction.FAKE

def addGmAccountByRoleId(iRoleID, sOwner, sReason):
	if not sOwner:
		return '使用者不能为空'
	sSQl='SELECT userSource,account FROM role_multi_field1 WHERE roleId={}'.format(iRoleID)
	rs=db4ms.gConnectionPool.query(sSQl).rows
	if not rs:
		return '角色ID:{}错误'.format(iRoleID)
	return addGmAccount(rs[0][0],rs[0][1], sOwner, sReason)
		
def addGmAccount(sUserSource,sAccount,sOwner,sReason):#增加GM账号
	if not sOwner:
		return '使用者不能为空'
	if (sUserSource,sAccount) in gdGm:
		return '该账号也拥有GM权限'
	gdGm[(sUserSource,sAccount)]=instruction.ADMIN|instruction.FAKE
	sSQl='INSERT INTO gm VALUES(\'{}\',\'{}\',\'{}\',\'{}\')'.format(sUserSource,sAccount,sOwner,sReason)
	db4ms.gConnectionPool.query(sSQl)
	return '增加GM账号成功'

def delGmAccountByRoleId(iRoleID):
	sSQl='SELECT userSource,account FROM role_multi_field1 WHERE roleId={}'.format(iRoleID)
	rs=db4ms.gConnectionPool.query(sSQl).rows
	if not rs:
		return '角色ID:{}错误'.format(iRoleID)
	return delGmAccount(rs[0][0], rs[0][1])

def delGmAccountByOwner(sOwner):
	sSQl='SELECT userSource,account FROM gm WHERE owner=\'{}\''.format(sOwner)
	rs=db4ms.gConnectionPool.query(sSQl).rows
	if not rs:
		return '没有对应的GM账号信息'
	for tAccount in rs:
		delGmAccount(*tAccount)
	return '删除GM账号成功'

def delGmAccount(sUserSource,sAccount,*tArgs):#删除GM账号
	if (sUserSource,sAccount) not in gdGm:
		return '该账号不是GM账号'
	gdGm.pop((sUserSource,sAccount), None)
	sSQl='DELETE FROM GM WHERE userSource=\'{}\' and account=\'{}\''.format(sUserSource,sAccount)
	db4ms.gConnectionPool.query(sSQl)
	return '删除GM账号成功'

def group(sUserSrc,sAccount):#获得用户所在的组
	t=(sUserSrc,sAccount)
	return gdGm.get(t,instruction.FAKE)
