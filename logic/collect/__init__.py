# -*- coding: utf-8 -*-
import requests
import json
import math

#室外收集玩法
if 'gbOnce' not in globals():
	gbOnce=True
	if 'mainService' in SYS_ARGV or 'centerService' in SYS_ARGV:
		gMainCollectObj = None
	if 'centerService' in SYS_ARGV:
		gCenterCollectObj = None
		gRoleInfoMngObj = None

def init():
	print "collect init..."
	global gMainCollectObj
	if 'mainService' in SYS_ARGV:
		# global gMainCollectObj
		gMainCollectObj = collect.mainCollect.cMainCollect()
		
	if 'centerService' in SYS_ARGV:
		# collect.centerCollect.initEventId()
		collect.centerCollect.initCenterStorageScheduler()
		
		gMainCollectObj = collect.mainCollect.cMainCollect()

		global gCollectSingletonObj
		gCollectSingletonObj =  collect.centerCollect.cCollectSingleton()
		gCollectSingletonObj.loadFromDB()
		
		global gCenterCollectObj
		gCenterCollectObj = collect.centerCollect.cCenterCollectMng()
		gCenterCollectObj.loadAllFromDB()
		gCenterCollectObj.autoCheckTimeOutEvent()

		global gRoleInfoMngObj
		gRoleInfoMngObj = collect.centerCollect.cRoleInfoMng()
		gRoleInfoMngObj.loadAllFromDB()
		# gRoleInfoMngObj.autoCheckTimeOut()



def getMainCollectObj():
	return gMainCollectObj

def getCenterCollectObj():
	return gCenterCollectObj

def CollectLog(str='', path='',):
	if not config.IS_INNER_SERVER:
		return
	if not path:
		path = "Collect"
	log.log(path, str)
	print str

#腾讯地图WebService API开发者密钥
#V3TBZ-R4F3X-EG44R-ZLED4-LNNZK-6LFTN
# '''http://apis.map.qq.com/ws/distance/v1/?mode=driving&from=39.983171,116.308479&to=39.996060,116.353455;39.949227,116.394310&key=OB4BZ-D4W3U-B7VVO-4PJWW-6TKDJ-WPB77'''
gsQQMapHttp = 'http://apis.map.qq.com/ws/distance/v1/?mode=driving&from={},{}&to={},{}&key=V3TBZ-R4F3X-EG44R-ZLED4-LNNZK-6LFTN'
gsQQMapKey = "V3TBZ-R4F3X-EG44R-ZLED4-LNNZK-6LFTN"
def getQQMapDistance(tStartPos, tEndPos):
	'''根据两个经纬度获取两个点的直线距离
	'''
	url = gsQQMapHttp.format(tStartPos[0], tStartPos[1], tEndPos[0], tEndPos[1])
	response = requests.get(url)
	dResult = json.loads(response.text)
	lElements = dResult.get("result", {}).get("elements", [])
	if lElements:
		return int(lElements[0].get("distance", -1))
	return -1#"坑爹的腾讯竟然算不出来"

EARTH_RADIUS = 6378137 #赤道半径(单位m)
#google地图提供的方法
def getEarthDistance(lon1, lat1, lon2, lat2): 
	# 经度1，纬度1，经度2，纬度2
	lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
	c = 2 * math.asin(math.sqrt(a)) 
	return int(c * EARTH_RADIUS)

#转化为弧度(rad)   
def rad(d):
	return d * math.pi / 180.0  
	
# 基于余弦定理求两经纬度距离 
# @param lon1 第一点的经度 
# @param lat1 第一点的纬度 
# @param lon2 第二点的经度 
# @param lat2 第二点的纬度 
# @return 返回的距离，单位km 
def getLineDistance(lon1, lat1, lon2, lat2):
	radLon1 = rad(lon1)
	radLon2 = rad(lon2)
	radLat1 = rad(lat1)
	radLat2 = rad(lat2)

	if radLat1 < 0:
		radLat1 = math.pi / 2 + abs(radLat1)#south  
	if radLat1 > 0:
		radLat1 = math.pi / 2 - abs(radLat1)#north  
	if radLon1 < 0:
		radLon1 = math.pi * 2 - abs(radLon1)#west  
	if radLat2 < 0:
		radLat2 = math.pi / 2 + abs(radLat2)#south  
	if radLat2 > 0:
		radLat2 = math.pi / 2 - abs(radLat2)#north  
	if radLon2 < 0:
		radLon2 = math.pi * 2 - abs(radLon2)#west  

	x1 = EARTH_RADIUS * math.cos(radLon1) * math.sin(radLat1) 
	y1 = EARTH_RADIUS * math.sin(radLon1) * math.sin(radLat1)
	z1 = EARTH_RADIUS * math.cos(radLat1)

	x2 = EARTH_RADIUS * math.cos(radLon2) * math.sin(radLat2) 
	y2 = EARTH_RADIUS * math.sin(radLon2) * math.sin(radLat2)
	z2 = EARTH_RADIUS * math.cos(radLat2)

 	d = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)+ (z1 - z2) * (z1 - z2))
	theta = math.acos((EARTH_RADIUS * EARTH_RADIUS + EARTH_RADIUS * EARTH_RADIUS - d * d) / (2 * EARTH_RADIUS * EARTH_RADIUS))
	dist = theta * EARTH_RADIUS
	return int(dist)

def testDistance():
	print "\t\t\t\t\t\t\t",'腾讯的结果'
	print "\t\t\t\t\t\t\t",(39.983171,116.308479),(39.996060,116.353455),"直线距离=",getQQMapDistance((39.983171,116.308479), (39.996060,116.353455))
	print "\t\t\t\t\t\t\t",(40.983171,116.308479),(40.986060,116.353455),"直线距离=",getQQMapDistance((40.983171,116.308479), (40.986060,116.353455))
	print "\t\t\t\t\t\t\t",(113.401721,23.124081),(113.403467,23.122537),"直线距离=",getQQMapDistance((113.401721,23.124081), (113.403467,23.122537)) 
	print "\n"
	print "\t\t\t\t\t\t\t",'getEarthDistance的结果'
	print "\t\t\t\t\t\t\t",(39.983171,116.308479),(39.996060,116.353455),"直线距离=",getEarthDistance(39.983171,116.308479, 39.996060,116.353455)
	print "\t\t\t\t\t\t\t",(40.983171,116.308479),(40.986060,116.353455),"直线距离=",getEarthDistance(40.983171,116.308479, 40.986060,116.353455)
	print "\t\t\t\t\t\t\t",(113.401721,23.124081),(113.403467,23.122537),"直线距离=",getEarthDistance(113.401721,23.124081, 113.403467,23.122537)
	print "\n"
	print "\t\t\t\t\t\t\t",'getLineDistance的结果'
	print "\t\t\t\t\t\t\t",(39.983171,116.308479),(39.996060,116.353455),"直线距离=",getLineDistance(39.983171,116.308479, 39.996060,116.353455)
	print "\t\t\t\t\t\t\t",(40.983171,116.308479),(40.986060,116.353455),"直线距离=",getLineDistance(40.983171,116.308479, 40.986060,116.353455)
	print "\t\t\t\t\t\t\t",(113.401721,23.124081),(113.403467,23.122537),"直线距离=",getLineDistance(113.401721,23.124081, 113.403467,23.122537)


# testDistance()

ONE_KM_LATITUDE = 1.0/111.0 	#1000米纬度
ONE_KM_LONGITUDE = 1.0/111.0 	#1000米经度

def getRandLatAndLongitude(fLatitude, fLongitude, iRandStart=100, iRandEnd=1000, iAngle=0, iDistance=0):
	'''以（fLatitude, fLongitude）为中心随机返回(iRandStart, iRandEnd)米的经纬度
	'''
	if not iAngle:
		iAngle = random.random() * 360	#随机角度
	if not iDistance:
		iDistance = rand(iRandStart, iRandEnd) / 1000.0 #随机距离（单位：公里）
	else:
		iDistance = iDistance/1000.0
	fRandLatitude = fLatitude + math.sin(iAngle) * iDistance * ONE_KM_LATITUDE
	fRandLongitude = fLongitude + math.cos(iAngle) * iDistance * ONE_KM_LONGITUDE * math.cos(fLongitude)
	# print "getRandLatAndLongitude=",fLatitude,fLongitude,iRandStart,iRandEnd
	# print iAngle,iDistance,fRandLatitude,fRandLongitude
	# print "getLineDistance=",getLineDistance(fLatitude, fLongitude, fRandLatitude, fRandLongitude)
	return fRandLatitude,fRandLongitude


def onLogin(who, bReLogin):
	collect.service4terminal.rpcCollectLeftCount(who)
	who.denyTeam.pop("collect_go", None)
	if hasattr(who, "enterCollect"):
		delattr(who, "enterCollect")


import random
from common import *
import log
import config
import ujson
import collect.mainCollect
import collect.centerCollect
import collect.service4terminal
