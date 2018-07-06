#-*-coding:utf-8-*-
#作者:马昭@曹县闫店楼镇
#内部员工账号
"""

0	内部测试账号
1	战法牧账号
2	腾讯账号
3	当乐
4	uc九游
"""

gtData=(
	#马昭
	('1','rerfgd45245'),
	('2','rerfgd45245'),
	('3','rerfgd45245'),
	('4','rerfgd45245'),
	('5','rerfgd45245'),
	('6','rerfgd45245'),

	

)



def isStaff(sUserSrc,sAccount):#是不是内部员工,内部员工在周维护时可以提前进入游戏体验.
	if gm.group(sUserSrc,sAccount)!=instruction.FAKE:#有gm权限的一定是内部员工
		return True
	return (sUserSrc,sAccount) in gtData

import gm
import md5
import instruction