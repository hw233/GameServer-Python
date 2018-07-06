# -*- coding: utf-8 -*-

# 队员状态
TEAM_STATE_NONE = -1  # 不是队员
TEAM_STATE_NORMAL = 0  # 正常
TEAM_STATE_LEAVE = 1  # 暂离
TEAM_STATE_OFFLINE = 2  # 离线

# 队员进入任务和离开任务的方式
ENTER_TASK_ADD = 0 # 加入队伍
ENTER_TASK_BACK = 1 # 归队
LEAVE_TASK_REMOVE = 0 # 离队
LEAVE_TASK_LEAVE = 1 # 暂离
LEAVE_TASK_OFFLINE = 2 # 离线

MEMBER_LIMIT = 5 # 队伍人数上限
JOIN_LIMIT = 10 # 申请人数上限
