# -*- coding: utf-8 -*-
import activity.test
import activity.fengyao
import activity.guaji
import activity.buddy
import activity.center
import activity.pk
import activity.race
import activity.escort
import activity.guildFight
import activity.treasure
import activity.instance
import activity.fairyland
import activity.schoolFight
import activity.guildRobber
import activity.guildMaze
import activity.teamRace
import activity.star
import activity.triones
import activity.fiveBoss

import answer.day
import answer.quick
import answer.firstExam
import answer.finalExam
import answer.betFlower
import answer.ring
import answer.treasure

activityInfoList = {
	1: {"mod":activity.test, "name":"test"},
	100: {"mod":activity.fengyao, "name":"fengyao"},
	101: {"mod":activity.guaji, "name":"guaji"},
	# 102: {"mod":activity.buddy, "name":"buddy"},
	103: {"mod":activity.center, "name":"center"},
	104: {"mod":activity.pk, "name":"pk"},
	105: {"mod":activity.race, "name":"race"},
	106: {"mod":activity.escort, "name":"escort"},
	107: {"mod":activity.guildFight, "name":"guildFight"},
	108: {"mod":activity.instance, "name":"instance"},
	109: {"mod":activity.treasure, "name":"treasure"},
	110: {"mod":activity.fairyland, "name":"fairyland"},
	111: {"mod":activity.schoolFight, "name":"schoolFight"},
	112: {"mod":activity.guildRobber, "name":"guildRobber"},
	113: {"mod":activity.star, "name":"star"},
	114: {"mod":activity.triones, "name":"triones"},
	115: {"mod":activity.guildMaze, "name":"guildMaze"},
	116: {"mod":activity.fiveBoss, "name":"fiveBoss"},
	118: {"mod":activity.teamRace, "name":"teamRace"},

	120: {"mod":answer.day, "name":"answerDay"},
	121: {"mod":answer.quick, "name":"answerQuick"},
	122: {"mod":answer.firstExam, "name":"firstExam"},
	123: {"mod":answer.finalExam, "name":"finalExam"},
	124: {"mod":answer.betFlower, "name":"betFlower"},
	125: {"mod":answer.ring, "name":"taskRingAnswer"},
	126: {"mod":answer.treasure, "name":"treasureAnswer"},
}