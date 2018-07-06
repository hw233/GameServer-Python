# -*- coding: utf-8 -*-

moduleList  = {}

def getModuleList():
	return moduleList

#npc法术导表开始
import perform.npcs.pf5101
import perform.npcs.pf5102
import perform.npcs.pf5103
import perform.npcs.pf5104
import perform.npcs.pf5105
import perform.npcs.pf5106
import perform.npcs.pf5107
import perform.npcs.pf5108
import perform.npcs.pf5109
import perform.npcs.pf5110
import perform.npcs.pf5111
import perform.npcs.pf5112
import perform.npcs.pf5113
import perform.npcs.pf5114
import perform.npcs.pf5115
import perform.npcs.pf5116
import perform.npcs.pf5117
import perform.npcs.pf5118
import perform.npcs.pf5119
import perform.npcs.pf5120
import perform.npcs.pf5121
import perform.npcs.pf5122
import perform.npcs.pf5123
import perform.npcs.pf5124
import perform.npcs.pf5125
import perform.npcs.pf5126
import perform.npcs.pf5127
import perform.npcs.pf5128
import perform.npcs.pf5129
import perform.npcs.pf5130
import perform.npcs.pf5131
import perform.npcs.pf5132
import perform.npcs.pf5133
import perform.npcs.pf5134
import perform.npcs.pf5135
import perform.npcs.pf5136
import perform.npcs.pf5137
import perform.npcs.pf5138
import perform.npcs.pf5139
import perform.npcs.pf5140
import perform.npcs.pf5141
import perform.npcs.pf5142
import perform.npcs.pf5143
import perform.npcs.pf5144
import perform.npcs.pf5145
import perform.npcs.pf5146
import perform.npcs.pf5147
import perform.npcs.pf5148
import perform.npcs.pf5149
import perform.npcs.pf5150
import perform.npcs.pf5151
import perform.npcs.pf5152
import perform.npcs.pf5153
import perform.npcs.pf5201
import perform.npcs.pf5202
import perform.npcs.pf5203
import perform.npcs.pf5204
import perform.npcs.pf5205
import perform.npcs.pf5206
import perform.npcs.pf5207
import perform.npcs.pf5208
import perform.npcs.pf5209
import perform.npcs.pf5210
import perform.npcs.pf5211
import perform.npcs.pf5212
import perform.npcs.pf5213
import perform.npcs.pf5214
import perform.npcs.pf5215
import perform.npcs.pf5216
import perform.npcs.pf5217
import perform.npcs.pf5218
import perform.npcs.pf5219
import perform.npcs.pf5220
import perform.npcs.pf5221
import perform.npcs.pf5222
import perform.npcs.pf5223
import perform.npcs.pf5224
import perform.npcs.pf5225
import perform.npcs.pf5226
import perform.npcs.pf5227
import perform.npcs.pf5228
import perform.npcs.pf5229
import perform.npcs.pf5230
import perform.npcs.pf5231
import perform.npcs.pf5232
import perform.npcs.pf5233
import perform.npcs.pf5234
import perform.npcs.pf5235
import perform.npcs.pf5236
import perform.npcs.pf5237
import perform.npcs.pf5238
import perform.npcs.pf5239
import perform.npcs.pf5240
import perform.npcs.pf5241
import perform.npcs.pf5242
import perform.npcs.pf5243
import perform.npcs.pf5244
import perform.npcs.pf5245
import perform.npcs.pf5246
import perform.npcs.pf5247
import perform.npcs.pf5248
import perform.npcs.pf5249
import perform.npcs.pf5250
import perform.npcs.pf5251
import perform.npcs.pf5252
import perform.npcs.pf5253
import perform.npcs.pf5301
import perform.npcs.pf5302
import perform.npcs.pf5304
import perform.npcs.pf5305
import perform.npcs.pf5306
import perform.npcs.pf5307
import perform.npcs.pf5309
import perform.npcs.pf5312
import perform.npcs.pf5313
import perform.npcs.pf5318
import perform.npcs.pf5319
import perform.npcs.pf5401
import perform.npcs.pf5402
import perform.npcs.pf5403
import perform.npcs.pf5404
import perform.npcs.pf5405
import perform.npcs.pf5406
import perform.npcs.pf5407
import perform.npcs.pf5408
import perform.npcs.pf5409
import perform.npcs.pf5410
import perform.npcs.pf5411
import perform.npcs.pf5412
import perform.npcs.pf5413
import perform.npcs.pf5414
import perform.npcs.pf5415
import perform.npcs.pf5416
import perform.npcs.pf5417
import perform.npcs.pf5418
import perform.npcs.pf5419
import perform.npcs.pf5420
import perform.npcs.pf5501
import perform.npcs.pf5502
import perform.npcs.pf5601
import perform.npcs.pf5602
import perform.npcs.pf5603
import perform.npcs.pf5604
import perform.npcs.pf5605
import perform.npcs.pf5606
import perform.npcs.pf5607
import perform.npcs.pf5608
import perform.npcs.pf5609
import perform.npcs.pf5610
import perform.npcs.pf5611
import perform.npcs.pf5612
import perform.npcs.pf5613
import perform.npcs.pf5614
import perform.npcs.pf5615
import perform.npcs.pf5616
import perform.npcs.pf5617
import perform.npcs.pf5618
import perform.npcs.pf5619
import perform.npcs.pf5620
import perform.npcs.pf5621
import perform.npcs.pf5622
import perform.npcs.pf5623
import perform.npcs.pf5624
import perform.npcs.pf5625
import perform.npcs.pf5626
import perform.npcs.pf5627
import perform.npcs.pf5628
import perform.npcs.pf5629
import perform.npcs.pf5630
import perform.npcs.pf5631
import perform.npcs.pf5632
import perform.npcs.pf5633
import perform.npcs.pf5634
import perform.npcs.pf5635
import perform.npcs.pf5636
import perform.npcs.pf5637
import perform.npcs.pf5638
import perform.npcs.pf5639
import perform.npcs.pf5640
import perform.npcs.pf5701
import perform.npcs.pf5702
import perform.npcs.pf5703
import perform.npcs.pf5704
import perform.npcs.pf5705
import perform.npcs.pf5706
import perform.npcs.pf5707
import perform.npcs.pf5708
import perform.npcs.pf5709
import perform.npcs.pf5710
import perform.npcs.pf5711
import perform.npcs.pf5712
import perform.npcs.pf5713
import perform.npcs.pf5714
import perform.npcs.pf5715
import perform.npcs.pf5716
import perform.npcs.pf5717
import perform.npcs.pf5718
import perform.npcs.pf5719
import perform.npcs.pf5720
import perform.npcs.pf5809
import perform.npcs.pf5810
import perform.npcs.pf5811
import perform.npcs.pf5812
import perform.npcs.pf5813
import perform.npcs.pf5814
import perform.npcs.pf5815
import perform.npcs.pf5816
import perform.npcs.pf5817
import perform.npcs.pf5820
import perform.npcs.pf5821
import perform.npcs.pf5849
import perform.npcs.pf5850
import perform.npcs.pf5851
import perform.npcs.pf5852
import perform.npcs.pf5853
import perform.npcs.pf5854
import perform.npcs.pf5855
import perform.npcs.pf5856
import perform.npcs.pf5857
import perform.npcs.pf5860
import perform.npcs.pf5861
import perform.npcs.pf5881
import perform.npcs.pf5882
import perform.npcs.pf5884
import perform.npcs.pf5885
import perform.npcs.pf5886
import perform.npcs.pf5887
import perform.npcs.pf5888
import perform.npcs.pf5889
import perform.npcs.pf6201
import perform.npcs.pf6202
import perform.npcs.pf6203
import perform.npcs.pf6204
import perform.npcs.pf6205
import perform.npcs.pf6206
import perform.npcs.pf6207
import perform.npcs.pf6208
import perform.npcs.pf6401
import perform.npcs.pf6402
import perform.npcs.pf6403
import perform.npcs.pf6404
import perform.npcs.pf6405
import perform.npcs.pf6406
import perform.npcs.pf6407
import perform.npcs.pf6408
import perform.npcs.pf6409
import perform.npcs.pf6410
import perform.npcs.pf6411
import perform.npcs.pf6412
import perform.npcs.pf6413
import perform.npcs.pf6414
import perform.npcs.pf6415
import perform.npcs.pf6416
import perform.npcs.pf6417
import perform.npcs.pf6418
import perform.npcs.pf6419
import perform.npcs.pf6420
import perform.npcs.pf6421

moduleList[5101] = perform.npcs.pf5101
moduleList[5102] = perform.npcs.pf5102
moduleList[5103] = perform.npcs.pf5103
moduleList[5104] = perform.npcs.pf5104
moduleList[5105] = perform.npcs.pf5105
moduleList[5106] = perform.npcs.pf5106
moduleList[5107] = perform.npcs.pf5107
moduleList[5108] = perform.npcs.pf5108
moduleList[5109] = perform.npcs.pf5109
moduleList[5110] = perform.npcs.pf5110
moduleList[5111] = perform.npcs.pf5111
moduleList[5112] = perform.npcs.pf5112
moduleList[5113] = perform.npcs.pf5113
moduleList[5114] = perform.npcs.pf5114
moduleList[5115] = perform.npcs.pf5115
moduleList[5116] = perform.npcs.pf5116
moduleList[5117] = perform.npcs.pf5117
moduleList[5118] = perform.npcs.pf5118
moduleList[5119] = perform.npcs.pf5119
moduleList[5120] = perform.npcs.pf5120
moduleList[5121] = perform.npcs.pf5121
moduleList[5122] = perform.npcs.pf5122
moduleList[5123] = perform.npcs.pf5123
moduleList[5124] = perform.npcs.pf5124
moduleList[5125] = perform.npcs.pf5125
moduleList[5126] = perform.npcs.pf5126
moduleList[5127] = perform.npcs.pf5127
moduleList[5128] = perform.npcs.pf5128
moduleList[5129] = perform.npcs.pf5129
moduleList[5130] = perform.npcs.pf5130
moduleList[5131] = perform.npcs.pf5131
moduleList[5132] = perform.npcs.pf5132
moduleList[5133] = perform.npcs.pf5133
moduleList[5134] = perform.npcs.pf5134
moduleList[5135] = perform.npcs.pf5135
moduleList[5136] = perform.npcs.pf5136
moduleList[5137] = perform.npcs.pf5137
moduleList[5138] = perform.npcs.pf5138
moduleList[5139] = perform.npcs.pf5139
moduleList[5140] = perform.npcs.pf5140
moduleList[5141] = perform.npcs.pf5141
moduleList[5142] = perform.npcs.pf5142
moduleList[5143] = perform.npcs.pf5143
moduleList[5144] = perform.npcs.pf5144
moduleList[5145] = perform.npcs.pf5145
moduleList[5146] = perform.npcs.pf5146
moduleList[5147] = perform.npcs.pf5147
moduleList[5148] = perform.npcs.pf5148
moduleList[5149] = perform.npcs.pf5149
moduleList[5150] = perform.npcs.pf5150
moduleList[5151] = perform.npcs.pf5151
moduleList[5152] = perform.npcs.pf5152
moduleList[5153] = perform.npcs.pf5153
moduleList[5201] = perform.npcs.pf5201
moduleList[5202] = perform.npcs.pf5202
moduleList[5203] = perform.npcs.pf5203
moduleList[5204] = perform.npcs.pf5204
moduleList[5205] = perform.npcs.pf5205
moduleList[5206] = perform.npcs.pf5206
moduleList[5207] = perform.npcs.pf5207
moduleList[5208] = perform.npcs.pf5208
moduleList[5209] = perform.npcs.pf5209
moduleList[5210] = perform.npcs.pf5210
moduleList[5211] = perform.npcs.pf5211
moduleList[5212] = perform.npcs.pf5212
moduleList[5213] = perform.npcs.pf5213
moduleList[5214] = perform.npcs.pf5214
moduleList[5215] = perform.npcs.pf5215
moduleList[5216] = perform.npcs.pf5216
moduleList[5217] = perform.npcs.pf5217
moduleList[5218] = perform.npcs.pf5218
moduleList[5219] = perform.npcs.pf5219
moduleList[5220] = perform.npcs.pf5220
moduleList[5221] = perform.npcs.pf5221
moduleList[5222] = perform.npcs.pf5222
moduleList[5223] = perform.npcs.pf5223
moduleList[5224] = perform.npcs.pf5224
moduleList[5225] = perform.npcs.pf5225
moduleList[5226] = perform.npcs.pf5226
moduleList[5227] = perform.npcs.pf5227
moduleList[5228] = perform.npcs.pf5228
moduleList[5229] = perform.npcs.pf5229
moduleList[5230] = perform.npcs.pf5230
moduleList[5231] = perform.npcs.pf5231
moduleList[5232] = perform.npcs.pf5232
moduleList[5233] = perform.npcs.pf5233
moduleList[5234] = perform.npcs.pf5234
moduleList[5235] = perform.npcs.pf5235
moduleList[5236] = perform.npcs.pf5236
moduleList[5237] = perform.npcs.pf5237
moduleList[5238] = perform.npcs.pf5238
moduleList[5239] = perform.npcs.pf5239
moduleList[5240] = perform.npcs.pf5240
moduleList[5241] = perform.npcs.pf5241
moduleList[5242] = perform.npcs.pf5242
moduleList[5243] = perform.npcs.pf5243
moduleList[5244] = perform.npcs.pf5244
moduleList[5245] = perform.npcs.pf5245
moduleList[5246] = perform.npcs.pf5246
moduleList[5247] = perform.npcs.pf5247
moduleList[5248] = perform.npcs.pf5248
moduleList[5249] = perform.npcs.pf5249
moduleList[5250] = perform.npcs.pf5250
moduleList[5251] = perform.npcs.pf5251
moduleList[5252] = perform.npcs.pf5252
moduleList[5253] = perform.npcs.pf5253
moduleList[5301] = perform.npcs.pf5301
moduleList[5302] = perform.npcs.pf5302
moduleList[5304] = perform.npcs.pf5304
moduleList[5305] = perform.npcs.pf5305
moduleList[5306] = perform.npcs.pf5306
moduleList[5307] = perform.npcs.pf5307
moduleList[5309] = perform.npcs.pf5309
moduleList[5312] = perform.npcs.pf5312
moduleList[5313] = perform.npcs.pf5313
moduleList[5318] = perform.npcs.pf5318
moduleList[5319] = perform.npcs.pf5319
moduleList[5401] = perform.npcs.pf5401
moduleList[5402] = perform.npcs.pf5402
moduleList[5403] = perform.npcs.pf5403
moduleList[5404] = perform.npcs.pf5404
moduleList[5405] = perform.npcs.pf5405
moduleList[5406] = perform.npcs.pf5406
moduleList[5407] = perform.npcs.pf5407
moduleList[5408] = perform.npcs.pf5408
moduleList[5409] = perform.npcs.pf5409
moduleList[5410] = perform.npcs.pf5410
moduleList[5411] = perform.npcs.pf5411
moduleList[5412] = perform.npcs.pf5412
moduleList[5413] = perform.npcs.pf5413
moduleList[5414] = perform.npcs.pf5414
moduleList[5415] = perform.npcs.pf5415
moduleList[5416] = perform.npcs.pf5416
moduleList[5417] = perform.npcs.pf5417
moduleList[5418] = perform.npcs.pf5418
moduleList[5419] = perform.npcs.pf5419
moduleList[5420] = perform.npcs.pf5420
moduleList[5501] = perform.npcs.pf5501
moduleList[5502] = perform.npcs.pf5502
moduleList[5601] = perform.npcs.pf5601
moduleList[5602] = perform.npcs.pf5602
moduleList[5603] = perform.npcs.pf5603
moduleList[5604] = perform.npcs.pf5604
moduleList[5605] = perform.npcs.pf5605
moduleList[5606] = perform.npcs.pf5606
moduleList[5607] = perform.npcs.pf5607
moduleList[5608] = perform.npcs.pf5608
moduleList[5609] = perform.npcs.pf5609
moduleList[5610] = perform.npcs.pf5610
moduleList[5611] = perform.npcs.pf5611
moduleList[5612] = perform.npcs.pf5612
moduleList[5613] = perform.npcs.pf5613
moduleList[5614] = perform.npcs.pf5614
moduleList[5615] = perform.npcs.pf5615
moduleList[5616] = perform.npcs.pf5616
moduleList[5617] = perform.npcs.pf5617
moduleList[5618] = perform.npcs.pf5618
moduleList[5619] = perform.npcs.pf5619
moduleList[5620] = perform.npcs.pf5620
moduleList[5621] = perform.npcs.pf5621
moduleList[5622] = perform.npcs.pf5622
moduleList[5623] = perform.npcs.pf5623
moduleList[5624] = perform.npcs.pf5624
moduleList[5625] = perform.npcs.pf5625
moduleList[5626] = perform.npcs.pf5626
moduleList[5627] = perform.npcs.pf5627
moduleList[5628] = perform.npcs.pf5628
moduleList[5629] = perform.npcs.pf5629
moduleList[5630] = perform.npcs.pf5630
moduleList[5631] = perform.npcs.pf5631
moduleList[5632] = perform.npcs.pf5632
moduleList[5633] = perform.npcs.pf5633
moduleList[5634] = perform.npcs.pf5634
moduleList[5635] = perform.npcs.pf5635
moduleList[5636] = perform.npcs.pf5636
moduleList[5637] = perform.npcs.pf5637
moduleList[5638] = perform.npcs.pf5638
moduleList[5639] = perform.npcs.pf5639
moduleList[5640] = perform.npcs.pf5640
moduleList[5701] = perform.npcs.pf5701
moduleList[5702] = perform.npcs.pf5702
moduleList[5703] = perform.npcs.pf5703
moduleList[5704] = perform.npcs.pf5704
moduleList[5705] = perform.npcs.pf5705
moduleList[5706] = perform.npcs.pf5706
moduleList[5707] = perform.npcs.pf5707
moduleList[5708] = perform.npcs.pf5708
moduleList[5709] = perform.npcs.pf5709
moduleList[5710] = perform.npcs.pf5710
moduleList[5711] = perform.npcs.pf5711
moduleList[5712] = perform.npcs.pf5712
moduleList[5713] = perform.npcs.pf5713
moduleList[5714] = perform.npcs.pf5714
moduleList[5715] = perform.npcs.pf5715
moduleList[5716] = perform.npcs.pf5716
moduleList[5717] = perform.npcs.pf5717
moduleList[5718] = perform.npcs.pf5718
moduleList[5719] = perform.npcs.pf5719
moduleList[5720] = perform.npcs.pf5720
moduleList[5809] = perform.npcs.pf5809
moduleList[5810] = perform.npcs.pf5810
moduleList[5811] = perform.npcs.pf5811
moduleList[5812] = perform.npcs.pf5812
moduleList[5813] = perform.npcs.pf5813
moduleList[5814] = perform.npcs.pf5814
moduleList[5815] = perform.npcs.pf5815
moduleList[5816] = perform.npcs.pf5816
moduleList[5817] = perform.npcs.pf5817
moduleList[5820] = perform.npcs.pf5820
moduleList[5821] = perform.npcs.pf5821
moduleList[5849] = perform.npcs.pf5849
moduleList[5850] = perform.npcs.pf5850
moduleList[5851] = perform.npcs.pf5851
moduleList[5852] = perform.npcs.pf5852
moduleList[5853] = perform.npcs.pf5853
moduleList[5854] = perform.npcs.pf5854
moduleList[5855] = perform.npcs.pf5855
moduleList[5856] = perform.npcs.pf5856
moduleList[5857] = perform.npcs.pf5857
moduleList[5860] = perform.npcs.pf5860
moduleList[5861] = perform.npcs.pf5861
moduleList[5881] = perform.npcs.pf5881
moduleList[5882] = perform.npcs.pf5882
moduleList[5884] = perform.npcs.pf5884
moduleList[5885] = perform.npcs.pf5885
moduleList[5886] = perform.npcs.pf5886
moduleList[5887] = perform.npcs.pf5887
moduleList[5888] = perform.npcs.pf5888
moduleList[5889] = perform.npcs.pf5889
moduleList[6201] = perform.npcs.pf6201
moduleList[6202] = perform.npcs.pf6202
moduleList[6203] = perform.npcs.pf6203
moduleList[6204] = perform.npcs.pf6204
moduleList[6205] = perform.npcs.pf6205
moduleList[6206] = perform.npcs.pf6206
moduleList[6207] = perform.npcs.pf6207
moduleList[6208] = perform.npcs.pf6208
moduleList[6401] = perform.npcs.pf6401
moduleList[6402] = perform.npcs.pf6402
moduleList[6403] = perform.npcs.pf6403
moduleList[6404] = perform.npcs.pf6404
moduleList[6405] = perform.npcs.pf6405
moduleList[6406] = perform.npcs.pf6406
moduleList[6407] = perform.npcs.pf6407
moduleList[6408] = perform.npcs.pf6408
moduleList[6409] = perform.npcs.pf6409
moduleList[6410] = perform.npcs.pf6410
moduleList[6411] = perform.npcs.pf6411
moduleList[6412] = perform.npcs.pf6412
moduleList[6413] = perform.npcs.pf6413
moduleList[6414] = perform.npcs.pf6414
moduleList[6415] = perform.npcs.pf6415
moduleList[6416] = perform.npcs.pf6416
moduleList[6417] = perform.npcs.pf6417
moduleList[6418] = perform.npcs.pf6418
moduleList[6419] = perform.npcs.pf6419
moduleList[6420] = perform.npcs.pf6420
moduleList[6421] = perform.npcs.pf6421
#npc法术导表结束

#门派法术导表开始
import perform.school.pf1111
import perform.school.pf1112
import perform.school.pf1113
import perform.school.pf1121
import perform.school.pf1122
import perform.school.pf1123
import perform.school.pf1131
import perform.school.pf1132
import perform.school.pf1133
import perform.school.pf1191
import perform.school.pf1211
import perform.school.pf1212
import perform.school.pf1213
import perform.school.pf1221
import perform.school.pf1222
import perform.school.pf1223
import perform.school.pf1231
import perform.school.pf1232
import perform.school.pf1233
import perform.school.pf1291
import perform.school.pf1311
import perform.school.pf1312
import perform.school.pf1313
import perform.school.pf1321
import perform.school.pf1322
import perform.school.pf1323
import perform.school.pf1331
import perform.school.pf1332
import perform.school.pf1333
import perform.school.pf1411
import perform.school.pf1412
import perform.school.pf1413
import perform.school.pf1421
import perform.school.pf1422
import perform.school.pf1423
import perform.school.pf1431
import perform.school.pf1432
import perform.school.pf1433
import perform.school.pf1511
import perform.school.pf1512
import perform.school.pf1513
import perform.school.pf1521
import perform.school.pf1522
import perform.school.pf1523
import perform.school.pf1531
import perform.school.pf1532
import perform.school.pf1533
import perform.school.pf1611
import perform.school.pf1612
import perform.school.pf1613
import perform.school.pf1621
import perform.school.pf1622
import perform.school.pf1623
import perform.school.pf1631
import perform.school.pf1632
import perform.school.pf1633
import perform.school.pf1691

moduleList[1111] = perform.school.pf1111
moduleList[1112] = perform.school.pf1112
moduleList[1113] = perform.school.pf1113
moduleList[1121] = perform.school.pf1121
moduleList[1122] = perform.school.pf1122
moduleList[1123] = perform.school.pf1123
moduleList[1131] = perform.school.pf1131
moduleList[1132] = perform.school.pf1132
moduleList[1133] = perform.school.pf1133
moduleList[1191] = perform.school.pf1191
moduleList[1211] = perform.school.pf1211
moduleList[1212] = perform.school.pf1212
moduleList[1213] = perform.school.pf1213
moduleList[1221] = perform.school.pf1221
moduleList[1222] = perform.school.pf1222
moduleList[1223] = perform.school.pf1223
moduleList[1231] = perform.school.pf1231
moduleList[1232] = perform.school.pf1232
moduleList[1233] = perform.school.pf1233
moduleList[1291] = perform.school.pf1291
moduleList[1311] = perform.school.pf1311
moduleList[1312] = perform.school.pf1312
moduleList[1313] = perform.school.pf1313
moduleList[1321] = perform.school.pf1321
moduleList[1322] = perform.school.pf1322
moduleList[1323] = perform.school.pf1323
moduleList[1331] = perform.school.pf1331
moduleList[1332] = perform.school.pf1332
moduleList[1333] = perform.school.pf1333
moduleList[1411] = perform.school.pf1411
moduleList[1412] = perform.school.pf1412
moduleList[1413] = perform.school.pf1413
moduleList[1421] = perform.school.pf1421
moduleList[1422] = perform.school.pf1422
moduleList[1423] = perform.school.pf1423
moduleList[1431] = perform.school.pf1431
moduleList[1432] = perform.school.pf1432
moduleList[1433] = perform.school.pf1433
moduleList[1511] = perform.school.pf1511
moduleList[1512] = perform.school.pf1512
moduleList[1513] = perform.school.pf1513
moduleList[1521] = perform.school.pf1521
moduleList[1522] = perform.school.pf1522
moduleList[1523] = perform.school.pf1523
moduleList[1531] = perform.school.pf1531
moduleList[1532] = perform.school.pf1532
moduleList[1533] = perform.school.pf1533
moduleList[1611] = perform.school.pf1611
moduleList[1612] = perform.school.pf1612
moduleList[1613] = perform.school.pf1613
moduleList[1621] = perform.school.pf1621
moduleList[1622] = perform.school.pf1622
moduleList[1623] = perform.school.pf1623
moduleList[1631] = perform.school.pf1631
moduleList[1632] = perform.school.pf1632
moduleList[1633] = perform.school.pf1633
moduleList[1691] = perform.school.pf1691
#门派法术导表结束



#装备法术导表开始
import perform.equip.pf3301
import perform.equip.pf3302
import perform.equip.pf3303
import perform.equip.pf3304
import perform.equip.pf3305
import perform.equip.pf3201
import perform.equip.pf3202
import perform.equip.pf3203
import perform.equip.pf3204
import perform.equip.pf3205
import perform.equip.pf3206
import perform.equip.pf3101
import perform.equip.pf3102
import perform.equip.pf3103
import perform.equip.pf3104
import perform.equip.pf3105
import perform.equip.pf3501
import perform.equip.pf3502
import perform.equip.pf3503
import perform.equip.pf3504
import perform.equip.pf3505
import perform.equip.pf3601
import perform.equip.pf3602
import perform.equip.pf3603
import perform.equip.pf3604
import perform.equip.pf3401
import perform.equip.pf3402
import perform.equip.pf3403
import perform.equip.pf3404
import perform.equip.pf3405
import perform.equip.pf3901
import perform.equip.pf3902
import perform.equip.pf4001
import perform.equip.pf4002
import perform.equip.pf4003
import perform.equip.pf4004
import perform.equip.pf4005
import perform.equip.pf4006
import perform.equip.pf4007
import perform.equip.pf4008
import perform.equip.pf4009
import perform.equip.pf4010
import perform.equip.pf4011
import perform.equip.pf4012
import perform.equip.pf4013
import perform.equip.pf4014
import perform.equip.pf4015
import perform.equip.pf4016
import perform.equip.pf4017
import perform.equip.pf4018
import perform.equip.pf4019
import perform.equip.pf4020
import perform.equip.pf4021
import perform.equip.pf4022
import perform.equip.pf4023
import perform.equip.pf4024
import perform.equip.pf4025
import perform.equip.pf4026
import perform.equip.pf4027
import perform.equip.pf4028
import perform.equip.pf4029
import perform.equip.pf4030
import perform.equip.pf4031
import perform.equip.pf4032
import perform.equip.pf4033
import perform.equip.pf4034
import perform.equip.pf4035
import perform.equip.pf4036
import perform.equip.pf4037
import perform.equip.pf4038
import perform.equip.pf4039

moduleList[3301] = perform.equip.pf3301
moduleList[3302] = perform.equip.pf3302
moduleList[3303] = perform.equip.pf3303
moduleList[3304] = perform.equip.pf3304
moduleList[3305] = perform.equip.pf3305
moduleList[3201] = perform.equip.pf3201
moduleList[3202] = perform.equip.pf3202
moduleList[3203] = perform.equip.pf3203
moduleList[3204] = perform.equip.pf3204
moduleList[3205] = perform.equip.pf3205
moduleList[3206] = perform.equip.pf3206
moduleList[3101] = perform.equip.pf3101
moduleList[3102] = perform.equip.pf3102
moduleList[3103] = perform.equip.pf3103
moduleList[3104] = perform.equip.pf3104
moduleList[3105] = perform.equip.pf3105
moduleList[3501] = perform.equip.pf3501
moduleList[3502] = perform.equip.pf3502
moduleList[3503] = perform.equip.pf3503
moduleList[3504] = perform.equip.pf3504
moduleList[3505] = perform.equip.pf3505
moduleList[3601] = perform.equip.pf3601
moduleList[3602] = perform.equip.pf3602
moduleList[3603] = perform.equip.pf3603
moduleList[3604] = perform.equip.pf3604
moduleList[3401] = perform.equip.pf3401
moduleList[3402] = perform.equip.pf3402
moduleList[3403] = perform.equip.pf3403
moduleList[3404] = perform.equip.pf3404
moduleList[3405] = perform.equip.pf3405
moduleList[3901] = perform.equip.pf3901
moduleList[3902] = perform.equip.pf3902
moduleList[4001] = perform.equip.pf4001
moduleList[4002] = perform.equip.pf4002
moduleList[4003] = perform.equip.pf4003
moduleList[4004] = perform.equip.pf4004
moduleList[4005] = perform.equip.pf4005
moduleList[4006] = perform.equip.pf4006
moduleList[4007] = perform.equip.pf4007
moduleList[4008] = perform.equip.pf4008
moduleList[4009] = perform.equip.pf4009
moduleList[4010] = perform.equip.pf4010
moduleList[4011] = perform.equip.pf4011
moduleList[4012] = perform.equip.pf4012
moduleList[4013] = perform.equip.pf4013
moduleList[4014] = perform.equip.pf4014
moduleList[4015] = perform.equip.pf4015
moduleList[4016] = perform.equip.pf4016
moduleList[4017] = perform.equip.pf4017
moduleList[4018] = perform.equip.pf4018
moduleList[4019] = perform.equip.pf4019
moduleList[4020] = perform.equip.pf4020
moduleList[4021] = perform.equip.pf4021
moduleList[4022] = perform.equip.pf4022
moduleList[4023] = perform.equip.pf4023
moduleList[4024] = perform.equip.pf4024
moduleList[4025] = perform.equip.pf4025
moduleList[4026] = perform.equip.pf4026
moduleList[4027] = perform.equip.pf4027
moduleList[4028] = perform.equip.pf4028
moduleList[4029] = perform.equip.pf4029
moduleList[4030] = perform.equip.pf4030
moduleList[4031] = perform.equip.pf4031
moduleList[4032] = perform.equip.pf4032
moduleList[4033] = perform.equip.pf4033
moduleList[4034] = perform.equip.pf4034
moduleList[4035] = perform.equip.pf4035
moduleList[4036] = perform.equip.pf4036
moduleList[4037] = perform.equip.pf4037
moduleList[4038] = perform.equip.pf4038
moduleList[4039] = perform.equip.pf4039
#装备法术导表结束

#修炼法术导表开始
import perform.practice.pf6101
import perform.practice.pf6102
import perform.practice.pf6103
import perform.practice.pf6104
import perform.practice.pf6105
import perform.practice.pf6106
import perform.practice.pf6107
import perform.practice.pf6108

moduleList[6101] = perform.practice.pf6101
moduleList[6102] = perform.practice.pf6102
moduleList[6103] = perform.practice.pf6103
moduleList[6104] = perform.practice.pf6104
moduleList[6105] = perform.practice.pf6105
moduleList[6106] = perform.practice.pf6106
moduleList[6107] = perform.practice.pf6107
moduleList[6108] = perform.practice.pf6108
#修炼法术导表结束