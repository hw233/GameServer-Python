# -*- coding: utf-8 -*-

# 邮件类型
MAIL_TYPE_TRADE = 1 # 交易
MAIL_TYPE_GUILD = 2 # 仙盟
MAIL_TYPE_SYS = 3 # 系统

# 邮件类型名称
typeNameList = {
	MAIL_TYPE_TRADE: "交易",
	MAIL_TYPE_GUILD: "仙盟",
	MAIL_TYPE_SYS: "系统",
}

# 各类型的邮件数上限
countLimitList = {
	MAIL_TYPE_TRADE: 30,
	MAIL_TYPE_GUILD: 30,
	MAIL_TYPE_SYS: 20,
}