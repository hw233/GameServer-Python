#-*-coding:utf-8-*-
#作者:叶伟龙@龙川县赤光镇
import codecs
fSrc=open('keywords.uenc','r')

gSet=set([])
for iRow,sLineTxt in enumerate(fSrc):
    if iRow==0 and sLineTxt[:3]==codecs.BOM_UTF8:#去掉utf8的文件头
        sLineTxt=sLineTxt[3:]			
    sLineTxt=sLineTxt.strip('\n')
    sLineTxt=sLineTxt.strip('\r')
    sLineTxt=sLineTxt.strip()
    sLineTxt=sLineTxt.replace('"', '')
    sLineTxt=sLineTxt.replace(',', '')
    if sLineTxt.count('\t')==len(sLineTxt):#一行全是\t
        continue
    if not sLineTxt:
        continue
    gSet.add(sLineTxt)

fSrc.close()

fSrc=open('keywords.uenc','w')
for sText in gSet:
    fSrc.write('{}\n'.format(sText))

print 'down'
