#-*-coding:utf-8-*-

ROLE_NAME_SELECT = 'SELECT name,pageNo FROM role_name'
ROLE_NAME_INSERT = 'INSERT INTO role_name(roleId,pageNo,name)VALUES({},{},\'{}\')'
ROLE_NAME_UPDATE = 'UPDATE role_name SET name = \'{}\' WHERE roleId = {} AND pageNo = {}'

EVENT_SELECT_ALL='SELECT * FROM event_info'
EVENT_SELECT='SELECT data FROM event_info WHERE eventId={}'
EVENT_UPDATE='UPDATE event_info SET data=\'{}\' WHERE eventId={}'
EVENT_INSERT='INSERT INTO event_info (eventId,data)VALUES({},\'{}\')'
EVENT_DELETE='DELETE FROM event_info WHERE eventId={}'
EVENT_MAXID='SELECT max(eventId) from event_info'

ROLEINFO_SELECT_ALL='SELECT * FROM role_info'
ROLEINFO_SELECT='SELECT data FROM role_info WHERE roleId={}'
ROLEINFO_UPDATE='UPDATE role_info SET data=\'{}\' WHERE roleId={}'
ROLEINFO_INSERT='INSERT INTO role_info (roleId,data)VALUES({},\'{}\')'
ROLEINFO_DELETE='DELETE FROM role_info WHERE roleId={}'

SINGLETON_SELECT='SELECT data FROM singleton WHERE name=\'{}\''
SINGLETON_UPDATE='UPDATE singleton SET data=\'{}\' WHERE name=\'{}\''
SINGLETON_INSERT='INSERT INTO singleton (name,data)VALUES(\'{}\',\'{}\')'
SINGLETON_DELETE='DELETE FROM singleton WHERE name=\'{}\''#按理没有删除的需求

RESUME_SELECT='SELECT data FROM resume WHERE roleId={}'
RESUME_UPDATE='UPDATE resume SET data=\'{}\' WHERE roleId={}'
RESUME_INSERT='INSERT INTO resume (roleId,data)VALUES({},\'{}\')'
RESUME_DELETE='DELETE FROM resume WHERE roleId={}'