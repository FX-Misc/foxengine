# -*- coding: utf-8 -*-

#完整的演示脚本

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    

def prepare_configs(seller,pman,dman):
    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    
    #svama3
    configs.append(config(buyer=fcustom(svama3,fast=6,mid=42,slow=69,sma=22,ma_standard=227,extend_days=13)))   #mm:(30880, 16830, 545, 4)
    configs.append(config(buyer=fcustom(svama3,fast= 31,mid= 26,slow= 28,sma=  9,ma_standard=250,extend_days=  9))) 	#balance=4375,times= 54    #
    configs.append(config(buyer=fcustom(svama3,fast= 28,mid= 93,slow= 76,sma=113,ma_standard=195,extend_days=  5))) 	#balance=2854,times=  9    #
    configs.append(config(buyer=fcustom(svama3,fast= 15,mid= 30,slow= 69,sma= 25,ma_standard=225,extend_days= 11))) 	#balance=2676,times= 58
    configs.append(config(buyer=fcustom(svama3,fast= 23,mid= 58,slow= 13,sma= 61,ma_standard= 55,extend_days= 13))) 	#balance=24595,times=  4
    configs.append(config(buyer=fcustom(svama3,fast= 29,mid= 58,slow= 12,sma= 65,ma_standard=250,extend_days= 13))) 	#balance=98932,times=  2   #
    configs.append(config(buyer=fcustom(svama3,fast= 31,mid= 22,slow= 13,sma= 61,ma_standard=250,extend_days= 13))) 	#balance=4228,times= 30    #
    configs.append(config(buyer=fcustom(svama3,fast= 27,mid= 26,slow= 76,sma= 89,ma_standard=190,extend_days=  5))) 	#balance=3885,times= 24
    configs.append(config(buyer=fcustom(svama3,fast=  7,mid= 23,slow= 66,sma= 77,ma_standard=195,extend_days= 19))) 	#balance=3092,times= 68    
    configs.append(config(buyer=fcustom(svama3,fast= 29,mid= 26,slow=143,sma= 79,ma_standard=175,extend_days= 19))) 	#balance=4901,times= 11
    configs.append(config(buyer=fcustom(svama3,fast= 25,mid= 18,slow=133,sma= 97,ma_standard=245,extend_days=  3))) 	#balance=6223,times= 10    #
    configs.append(config(buyer=fcustom(svama3,fast= 29,mid= 19,slow=144,sma= 95,ma_standard=175,extend_days=  3))) 	#balance=17630,times= 19   #
    configs.append(config(buyer=fcustom(svama3,fast= 29,mid= 19,slow=144,sma= 95,ma_standard=175,extend_days= 35))) 	#balance=84058,times=  4   #
    configs.append(config(buyer=fcustom(svama3,fast= 17,mid= 26,slow=141,sma= 95,ma_standard=245,extend_days=  3))) 	#balance=3092,times= 13    #
    configs.append(config(buyer=fcustom(svama3,fast=  2,mid= 53,slow=137,sma= 79,ma_standard=125,extend_days=  5))) 	#balance=60395,times=  2
    configs.append(config(buyer=fcustom(svama3,fast= 15,mid= 58,slow=114,sma=109,ma_standard=230,extend_days= 13))) 	#balance=23711,times=  3   #
    configs.append(config(buyer=fcustom(svama3,fast=  3,mid= 83,slow=138,sma= 51,ma_standard=190,extend_days= 13))) 	#balance=6080,times=  5    #
    configs.append(config(buyer=fcustom(svama3,fast= 30,mid= 83,slow=143,sma= 97,ma_standard=175,extend_days= 19))) 	#balance=21681,times=  7   #
    configs.append(config(buyer=fcustom(svama3,fast= 10,mid= 94,slow=156,sma= 73,ma_standard=210,extend_days=  5))) 	#balance=8197,times=  6    #
    configs.append(config(buyer=fcustom(svama3,fast= 14,mid= 72,slow=139,sma= 57,ma_standard=185,extend_days= 19))) 	#balance=7576,times= 10
    configs.append(config(buyer=fcustom(svama3,fast= 29,mid=  5,slow=171,sma= 47,ma_standard=155,extend_days= 31))) 	#balance=3784,times=  3
    configs.append(config(buyer=fcustom(svama3,fast= 35,mid= 27,slow=187,sma=111,ma_standard= 80,extend_days= 31))) 	#balance=2849,times=  3
    configs.append(config(buyer=fcustom(svama3,fast=  2,mid= 90,slow=175,sma= 11,ma_standard=195,extend_days= 13))) 	#balance=8442,times=  2    #
    configs.append(config(buyer=fcustom(svama3,fast= 37,mid= 67,slow=106,sma= 87,ma_standard=245,extend_days=  9))) 	#balance=6402,times=  4    #
    configs.append(config(buyer=fcustom(svama3,fast= 43,mid= 27,slow= 76,sma= 97,ma_standard=215,extend_days=  5))) 	#balance=5421,times= 23    #
    configs.append(config(buyer=fcustom(svama3,fast= 42,mid= 25,slow= 76,sma= 97,ma_standard=195,extend_days=  5))) 	#balance=3049,times= 19
    configs.append(config(buyer=fcustom(svama3,fast= 43,mid= 30,slow= 12,sma= 89,ma_standard=215,extend_days=  9))) 	#balance=2981,times= 25    #
    configs.append(config(buyer=fcustom(svama3,fast= 42,mid= 30,slow= 76,sma= 97,ma_standard=195,extend_days= 35))) 	#balance=5359,times=  5    #
    configs.append(config(buyer=fcustom(svama3,fast= 39,mid= 57,slow=196,sma=101,ma_standard=180,extend_days= 17))) 	#balance=7971,times= 18
    configs.append(config(buyer=fcustom(svama3,fast= 14,mid= 67,slow=253,sma= 65,ma_standard=190,extend_days= 19))) 	#balance=8201,times=  6    #
    configs.append(config(buyer=fcustom(svama3,fast=  3,mid= 73,slow=254,sma= 63,ma_standard=190,extend_days= 19))) 	#balance=11944,times=  5   #
    configs.append(config(buyer=fcustom(svama3,fast=  2,mid= 19,slow=233,sma= 81,ma_standard=245,extend_days= 15))) 	#balance=3648,times= 42
    configs.append(config(buyer=fcustom(svama3,fast= 13,mid= 19,slow=240,sma= 95,ma_standard=255,extend_days=  3))) 	#balance=5750,times= 26    #
    configs.append(config(buyer=fcustom(svama3,fast= 10,mid= 30,slow=204,sma= 97,ma_standard=230,extend_days=  7))) 	#balance=11440,times=  7   #
    configs.append(config(buyer=fcustom(svama3,fast= 32,mid= 23,slow= 45,sma=117,ma_standard= 70,extend_days= 31))) 	#balance=86512,times= 12
    configs.append(config(buyer=fcustom(svama3,fast= 32,mid= 23,slow= 45,sma=117,ma_standard= 70,extend_days= 27))) 	#balance=524364,times= 10    
    configs.append(config(buyer=fcustom(svama3,fast=  7,mid= 29,slow= 43,sma= 87,ma_standard= 55,extend_days=  5))) 	#balance=3553,times= 28
    configs.append(config(buyer=fcustom(svama3,fast= 28,mid= 90,slow= 55,sma= 43,ma_standard=250,extend_days= 11))) 	#balance=3355,times=  9
    configs.append(config(buyer=fcustom(svama3,fast= 27,mid= 62,slow= 49,sma= 73,ma_standard=205,extend_days= 31))) 	#balance=3872,times= 16
    configs.append(config(buyer=fcustom(svama3,fast=  1,mid= 83,slow=256,sma= 63,ma_standard=190,extend_days= 23))) 	#balance=4627,times=  6    #
    configs.append(config(buyer=fcustom(svama3,fast= 10,mid= 95,slow=204,sma= 97,ma_standard=235,extend_days=  5))) 	#balance=5846,times= 13    #
    configs.append(config(buyer=fcustom(svama3,fast= 15,mid= 94,slow=209,sma= 25,ma_standard=205,extend_days= 31))) 	#balance=11924,times=  9   #
    configs.append(config(buyer=fcustom(svama3,fast= 15,mid= 94,slow=205,sma= 61,ma_standard=210,extend_days= 13))) 	#balance=37160,times=  2   #
    configs.append(config(buyer=fcustom(svama3,fast= 23,mid= 75,slow=222,sma= 19,ma_standard=180,extend_days= 25))) 	#balance=4287,times=  7    #
    configs.append(config(buyer=fcustom(svama3,fast= 40,mid= 87,slow=196,sma=101,ma_standard=180,extend_days= 17))) 	#balance=4122,times= 10    #

    #svama2
    configs.append(config(buyer=fcustom(svama2,fast=  6,slow=171,sma=105,ma_standard=244))) 	#balance=2854,times=  7
    configs.append(config(buyer=fcustom(svama2,fast=  5,slow=160,sma=  6,ma_standard=232))) 	#balance=15205,times=  7
    configs.append(config(buyer=fcustom(svama2,fast= 15,slow=  7,sma= 92,ma_standard=232))) #   #balance=69244,times=  2
    configs.append(config(buyer=fcustom(svama2,fast= 18,slow= 57,sma= 11,ma_standard=245))) 	#balance=2900,times=  4
    configs.append(config(buyer=fcustom(svama2,fast=  8,slow= 66,sma=114,ma_standard= 92))) 	#balance=3082,times= 33
    configs.append(config(buyer=fcustom(svama2,fast=  3,slow= 60,sma= 54,ma_standard=254))) #	#balance=6066,times=  7
    configs.append(config(buyer=fcustom(svama2,fast=  4,slow= 91,sma=122,ma_standard= 80))) 	#balance=6461,times= 13
    configs.append(config(buyer=fcustom(svama2,fast=  3,slow= 97,sma=115,ma_standard= 83))) 	#balance=6713,times=  9
    configs.append(config(buyer=fcustom(svama2,fast=  8,slow= 82,sma= 44,ma_standard=231))) 	#balance=60945,times= 12
    configs.append(config(buyer=fcustom(svama2,fast= 26,slow= 88,sma= 73,ma_standard=238))) 	#balance=2760,times= 35
    configs.append(config(buyer=fcustom(svama2,fast= 27,slow=175,sma= 85,ma_standard= 72))) 	#balance=5523,times= 36
    configs.append(config(buyer=fcustom(svama2,fast=  5,slow=160,sma=  6,ma_standard=232))) 	#balance=15205,times=  7
    configs.append(config(buyer=fcustom(svama2,fast=  8,slow=164,sma=122,ma_standard= 78))) 	#balance=2727,times= 28
    configs.append(config(buyer=fcustom(svama2,fast=  5,slow=166,sma= 53,ma_standard= 79))) 	#balance=3572,times= 15
    configs.append(config(buyer=fcustom(svama2,fast=  8,slow=196,sma= 46,ma_standard=214))) 	#balance=11796,times= 15
    configs.append(config(buyer=fcustom(svama2,fast=  3,slow=210,sma=119,ma_standard=213))) # 	#balance=20383,times= 12
    configs.append(config(buyer=fcustom(svama2,fast=  2,slow=241,sma= 43,ma_standard=152))) 	#balance=30649,times=  7
    configs.append(config(buyer=fcustom(svama2,fast=  2,slow=209,sma= 53,ma_standard=200))) #balance=524165,times=5    
    configs.append(config(buyer=fcustom(svama2,fast= 21,slow=235,sma= 73,ma_standard=237))) 	#balance=2390,times= 24
    configs.append(config(buyer=fcustom(svama2,fast= 37,slow=200,sma=104,ma_standard=215))) 	#balance=2151,times= 33
    configs.append(config(buyer=fcustom(svama2,fast=  4,slow=128,sma=120,ma_standard= 80))) 	#balance=4648,times= 12
    configs.append(config(buyer=fcustom(svama2,fast= 14,slow=128,sma=120,ma_standard= 84))) 	#balance=5205,times= 28
    configs.append(config(buyer=fcustom(svama2,fast= 15,slow=112,sma=108,ma_standard=231))) 	#balance=19177,times=  6
    configs.append(config(buyer=fcustom(svama2,fast= 37,slow=112,sma= 46,ma_standard=232))) 	#balance=3039,times=  4

    #以下为svama2s
    configs.append(config(buyer=fcustom(svama2s,fast= 13,slow= 79,sma= 41,ma_standard=231,extend_days= 23))) 	#balance=2406,times= 20
    configs.append(config(buyer=fcustom(svama2s,fast=  8,slow= 98,sma= 64,ma_standard=232,extend_days= 27))) 	#balance=2557,times= 19
    configs.append(config(buyer=fcustom(svama2s,fast= 13,slow= 95,sma= 65,ma_standard=231,extend_days= 23))) 	#balance=2565,times= 10
    configs.append(config(buyer=fcustom(svama2s,fast=  4,slow=100,sma= 63,ma_standard=254,extend_days= 16))) 	#balance=2766,times=  6
    configs.append(config(buyer=fcustom(svama2s,fast= 16,slow= 57,sma=127,ma_standard=230,extend_days=  5))) 	#balance=2333,times= 20
    configs.append(config(buyer=fcustom(svama2s,fast= 14,slow= 56,sma= 85,ma_standard=230,extend_days= 25))) 	#balance=2798,times= 13
    configs.append(config(buyer=fcustom(svama2s,fast= 16,slow=162,sma=101,ma_standard=105,extend_days=  9))) 	#balance=3265,times= 67
    configs.append(config(buyer=fcustom(svama2s,fast=  3,slow= 56,sma= 75,ma_standard=130,extend_days= 19))) 	#balance=2687,times= 43
    configs.append(config(buyer=fcustom(svama2s,fast=  7,slow=155,sma=121,ma_standard=105,extend_days= 17))) 	#balance=7728,times= 34
    configs.append(config(buyer=fcustom(svama2s,fast= 28,slow=233,sma= 59,ma_standard=230,extend_days=  9))) 	#balance=3470,times=  8
    configs.append(config(buyer=fcustom(svama2s,fast= 48,slow=121,sma=111,ma_standard=230,extend_days= 25))) 	#balance=4076,times=  9
    configs.append(config(buyer=fcustom(svama2s,fast=  1,slow= 79,sma=121,ma_standard= 95,extend_days=  9))) 	#balance=5103,times= 10
    configs.append(config(buyer=fcustom(svama2s,fast=  8,slow= 98,sma= 40,ma_standard=232,extend_days= 27))) 	#balance=6217,times= 20
    configs.append(config(buyer=fcustom(svama2s,fast= 15,slow= 95,sma= 57,ma_standard=232,extend_days= 23))) 	#balance=10557,times= 15

    #vama3
    configs.append(config(buyer=fcustom(vama3,fast=  3,mid= 51,slow= 67,pre_length= 11,ma_standard=225,extend_days= 19))) 	#balance=2032,times= 10
    configs.append(config(buyer=fcustom(vama3,fast= 23,mid= 92,slow=143,pre_length=176,ma_standard=180,extend_days=  5))) 	#balance=7901,times=  2#
    configs.append(config(buyer=fcustom(vama3,fast= 23,mid= 60,slow= 15,pre_length= 51,ma_standard= 65,extend_days=  9))) 	#balance=2242,times=  4
    configs.append(config(buyer=fcustom(vama3,fast=  7,mid= 56,slow= 14,pre_length= 51,ma_standard=180,extend_days=  9))) 	#balance=10663,times=  2
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 36,slow= 44,pre_length=  1,ma_standard=240,extend_days=  5))) 	#balance=7077,times=  4
    configs.append(config(buyer=fcustom(vama3,fast= 12,mid= 34,slow= 11,pre_length= 86,ma_standard=110,extend_days= 15))) 	#balance=55347,times=  3    #
    configs.append(config(buyer=fcustom(vama3,fast= 14,mid= 69,slow= 20,pre_length= 41,ma_standard=140,extend_days= 29))) 	#balance=20983,times=  3    #
    configs.append(config(buyer=fcustom(vama3,fast= 44,mid= 92,slow=  5,pre_length=106,ma_standard= 85,extend_days=  9))) 	#balance=4094,times=  3
    configs.append(config(buyer=fcustom(vama3,fast= 15,mid= 73,slow= 31,pre_length= 46,ma_standard=135,extend_days=  5))) 	#balance=6570,times=  4 #
    configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 73,slow= 35,pre_length=101,ma_standard=135,extend_days= 21))) 	#balance=124860,times=  5   #
    configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 73,slow= 36,pre_length=106,ma_standard=125,extend_days= 21))) 	#balance=3285,times= 12
    configs.append(config(buyer=fcustom(vama3,fast=  3,mid= 69,slow=206,pre_length=151,ma_standard=225,extend_days= 33))) 	#balance=7356,times= 16
    configs.append(config(buyer=fcustom(vama3,fast= 44,mid= 70,slow=198,pre_length= 26,ma_standard=125,extend_days=  7))) 	#balance=15266,times= 12
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 86,slow=197,pre_length= 36,ma_standard=240,extend_days= 21))) 	#balance=25984,times=  5
    configs.append(config(buyer=fcustom(vama3,fast= 35,mid= 86,slow=197,pre_length= 11,ma_standard=240,extend_days= 21))) 	#balance=10150,times=  7
    configs.append(config(buyer=fcustom(vama3,fast= 35,mid= 97,slow=197,pre_length= 61,ma_standard=130,extend_days= 11))) 	#balance=18697,times=  8
    configs.append(config(buyer=fcustom(vama3,fast= 19,mid= 14,slow=198,pre_length=181,ma_standard=100,extend_days= 15))) 	#balance=2405,times=  8
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 59,slow=195,pre_length=  6,ma_standard=180,extend_days= 21))) 	#balance=3782,times=  3
    configs.append(config(buyer=fcustom(vama3,fast=  4,mid= 76,slow=212,pre_length=121,ma_standard=125,extend_days= 27))) 	#balance=9067,times= 16
    configs.append(config(buyer=fcustom(vama3,fast=  2,mid= 69,slow=212,pre_length=121,ma_standard=230,extend_days= 25))) 	#balance=20464,times= 12
    configs.append(config(buyer=fcustom(vama3,fast= 15,mid= 76,slow=211,pre_length= 36,ma_standard=200,extend_days= 23))) 	#balance=17956,times=  6    #
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid= 67,slow=218,pre_length=126,ma_standard=235,extend_days= 25))) 	#balance=3774,times=  9
    configs.append(config(buyer=fcustom(vama3,fast=  9,mid= 87,slow=219,pre_length=141,ma_standard= 30,extend_days= 21))) 	#balance=3771,times= 15
    configs.append(config(buyer=fcustom(vama3,fast= 27,mid= 46,slow=221,pre_length=191,ma_standard=140,extend_days= 35))) 	#balance=2530,times= 25
    configs.append(config(buyer=fcustom(vama3,fast= 36,mid=  7,slow=225,pre_length=171,ma_standard= 20,extend_days= 13))) 	#balance=2308,times= 27
    configs.append(config(buyer=fcustom(vama3,fast=  3,mid= 89,slow=159,pre_length=181,ma_standard=125,extend_days= 11))) 	#balance=134234,times=  7
    configs.append(config(buyer=fcustom(vama3,fast=  4,mid= 73,slow=155,pre_length=161,ma_standard=215,extend_days= 21))) 	#balance=68023,times= 11
    configs.append(config(buyer=fcustom(vama3,fast=  4,mid= 76,slow=163,pre_length=101,ma_standard=215,extend_days= 21))) 	#balance=208798,times=  7
    configs.append(config(buyer=fcustom(vama3,fast= 28,mid= 85,slow=184,pre_length= 66,ma_standard=235,extend_days= 17))) 	#balance=13420,times=  7    #
    configs.append(config(buyer=fcustom(vama3,fast= 20,mid= 68,slow=163,pre_length=101,ma_standard=215,extend_days= 21))) 	#balance=744790,times= 11   
    configs.append(config(buyer=fcustom(vama3,fast= 14,mid= 59,slow=177,pre_length=161,ma_standard=225,extend_days=  5))) 	#balance=545800,times=  2   #
    configs.append(config(buyer=fcustom(vama3,fast= 38,mid= 17,slow=183,pre_length=176,ma_standard= 35,extend_days=  3))) 	#balance=2970,times=  6
    configs.append(config(buyer=fcustom(vama3,fast= 43,mid= 51,slow=163,pre_length=171,ma_standard=225,extend_days= 15))) 	#balance=34268,times=  3
    configs.append(config(buyer=fcustom(vama3,fast= 47,mid=  3,slow=167,pre_length= 41,ma_standard= 55,extend_days= 17))) 	#balance=2647,times= 10
    configs.append(config(buyer=fcustom(vama3,fast=  7,mid= 28,slow=251,pre_length=176,ma_standard=165,extend_days=  5))) 	#balance=2383,times=  5 #
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid= 39,slow=254,pre_length=151,ma_standard=255,extend_days= 33))) 	#balance=3471,times= 22
    configs.append(config(buyer=fcustom(vama3,fast=  8,mid= 93,slow=255,pre_length=  6,ma_standard=215,extend_days= 15))) 	#balance=2928,times=  9 #
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid= 60,slow=139,pre_length=161,ma_standard=190,extend_days= 25))) 	#balance=10939,times= 20
    configs.append(config(buyer=fcustom(vama3,fast= 27,mid= 76,slow=120,pre_length= 66,ma_standard=170,extend_days= 19))) 	#balance=21618,times= 16
    configs.append(config(buyer=fcustom(vama3,fast= 34,mid= 69,slow=148,pre_length= 66,ma_standard=230,extend_days=  5))) 	#balance=5113,times= 10 #
    configs.append(config(buyer=fcustom(vama3,fast= 44,mid= 76,slow=148,pre_length= 66,ma_standard=205,extend_days=  7))) 	#balance=67606,times=  9
    configs.append(config(buyer=fcustom(vama3,fast= 35,mid= 72,slow=120,pre_length=101,ma_standard=225,extend_days= 27))) 	#balance=3849,times= 36
    configs.append(config(buyer=fcustom(vama3,fast= 43,mid= 97,slow=129,pre_length= 76,ma_standard=140,extend_days= 15))) 	#balance=13260,times=  7
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid= 30,slow=120,pre_length=106,ma_standard=220,extend_days= 25))) 	#balance=2616,times= 41
    configs.append(config(buyer=fcustom(vama3,fast= 31,mid= 28,slow=143,pre_length=171,ma_standard=180,extend_days= 21))) 	#balance=3553,times=  4
    configs.append(config(buyer=fcustom(vama3,fast= 37,mid=  4,slow=149,pre_length=116,ma_standard=200,extend_days= 11))) 	#balance=2412,times=  8
    configs.append(config(buyer=fcustom(vama3,fast= 35,mid= 69,slow=101,pre_length= 21,ma_standard=240,extend_days= 11))) 	#balance=12330,times=  5    #
    configs.append(config(buyer=fcustom(vama3,fast= 13,mid= 20,slow= 81,pre_length=111,ma_standard=255,extend_days= 17))) 	#balance=3245,times= 64
    configs.append(config(buyer=fcustom(vama3,fast= 11,mid= 28,slow= 99,pre_length= 21,ma_standard=160,extend_days= 29))) 	#balance=2760,times= 54
    configs.append(config(buyer=fcustom(vama3,fast= 47,mid= 36,slow= 91,pre_length=136,ma_standard= 15,extend_days=  5))) 	#balance=2208,times= 23
    configs.append(config(buyer=fcustom(vama3,fast= 13,mid= 51,slow= 67,pre_length= 11,ma_standard=230,extend_days= 27))) 	#balance=6762,times= 11
    configs.append(config(buyer=fcustom(vama3,fast= 25,mid= 51,slow= 67,pre_length= 11,ma_standard=230,extend_days= 15))) 	#balance=13094,times=  9

    #vama2
    configs.append(config(buyer=fcustom(vama2,fast= 34,slow= 38,pre_length= 46,ma_standard=250))) 	#balance=2831,times=  9
    configs.append(config(buyer=fcustom(vama2,fast=  6,slow=152,pre_length= 71,ma_standard=225))) 	#balance=4537,times=  7
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow=151,pre_length=151,ma_standard=235))) 	#balance=885500,times=  3#
    configs.append(config(buyer=fcustom(vama2,fast=  5,slow=164,pre_length= 31,ma_standard=195))) 	#balance=6366,times= 16
    configs.append(config(buyer=fcustom(vama2,fast=  6,slow=161,pre_length= 66,ma_standard=255))) 	#balance=4347,times= 13
    configs.append(config(buyer=fcustom(vama2,fast=  8,slow=169,pre_length= 66,ma_standard=235))) 	#balance=4984,times= 18
    configs.append(config(buyer=fcustom(vama2,fast= 24,slow=161,pre_length= 66,ma_standard=225))) 	#balance=2672,times= 21
    configs.append(config(buyer=fcustom(vama2,fast= 24,slow=152,pre_length=  1,ma_standard=225))) 	#balance=6746,times=  7
    configs.append(config(buyer=fcustom(vama2,fast= 46,slow=152,pre_length= 71,ma_standard=225))) 	#balance=9830,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  1,slow=208,pre_length= 46,ma_standard=250))) 	#balance=517134,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow=234,pre_length= 46,ma_standard=250))) 	#balance=89137,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  6,slow=223,pre_length=186,ma_standard=240))) 	#balance=7581,times= 10
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow=198,pre_length= 46,ma_standard=245))) 	#balance=517134,times=  4    
    configs.append(config(buyer=fcustom(vama2,fast=  6,slow=248,pre_length=131,ma_standard= 90))) 	#balance=3502,times= 22
    configs.append(config(buyer=fcustom(vama2,fast=  8,slow=228,pre_length= 61,ma_standard=255))) 	#balance=11032,times= 10
    configs.append(config(buyer=fcustom(vama2,fast= 16,slow=193,pre_length= 76,ma_standard= 35))) 	#balance=3300,times= 24
    configs.append(config(buyer=fcustom(vama2,fast= 42,slow=219,pre_length=196,ma_standard=175))) 	#balance=5216,times= 22
    configs.append(config(buyer=fcustom(vama2,fast=  1,slow=100,pre_length=151,ma_standard=210))) 	#balance=18190,times=  3#
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 97,pre_length= 26,ma_standard=205))) 	#balance=10453,times=  2#
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 40,pre_length= 46,ma_standard=250))) 	#balance=54369,times=  5#
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 31,pre_length=151,ma_standard=225))) 	#balance=13337,times= 21
    configs.append(config(buyer=fcustom(vama2,fast=  4,slow= 42,pre_length= 26,ma_standard=250))) 	#balance=277724,times=  5#
    configs.append(config(buyer=fcustom(vama2,fast=  4,slow= 48,pre_length= 51,ma_standard=145))) 	#balance=2831,times= 13
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 58,pre_length=  6,ma_standard=245))) 	#balance=31915,times=  4
    configs.append(config(buyer=fcustom(vama2,fast=  1,slow= 55,pre_length= 46,ma_standard=245))) 	#balance=40533,times=  6#
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 55,pre_length=151,ma_standard=225))) 	#balance=9026,times= 12
    configs.append(config(buyer=fcustom(vama2,fast= 16,slow= 51,pre_length= 36,ma_standard=225))) 	#balance=4046,times= 41
    configs.append(config(buyer=fcustom(vama2,fast= 26,slow= 61,pre_length=166,ma_standard=185))) 	#balance=3357,times= 49
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 67,pre_length= 46,ma_standard=245))) 	#balance=21599,times=  7
    configs.append(config(buyer=fcustom(vama2,fast=  5,slow= 60,pre_length= 41,ma_standard=235))) 	#balance=6412,times= 17#
    configs.append(config(buyer=fcustom(vama2,fast=  9,slow= 66,pre_length= 81,ma_standard=200))) 	#balance=4967,times= 28
    configs.append(config(buyer=fcustom(vama2,fast= 18,slow= 61,pre_length= 66,ma_standard=125))) 	#balance=5270,times= 43
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 27,pre_length=151,ma_standard=225))) 	#balance=9395,times= 23
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow= 23,pre_length=151,ma_standard=225))) 	#balance=71538,times= 17
    configs.append(config(buyer=fcustom(vama2,fast=  1,slow= 23,pre_length=151,ma_standard=225))) 	#balance=9613,times= 18
    configs.append(config(buyer=fcustom(vama2,fast= 23,slow=127,pre_length= 36,ma_standard=190))) 	#balance=3913,times= 25
    configs.append(config(buyer=fcustom(vama2,fast= 13,slow=140,pre_length=156,ma_standard=235))) 	#balance=4472,times= 28
    configs.append(config(buyer=fcustom(vama2,fast=  2,slow=136,pre_length=141,ma_standard=225))) 	#balance=51614,times=  4#
    configs.append(config(buyer=fcustom(vama2,fast=  6,slow=131,pre_length= 26,ma_standard=235))) 	#balance=4702,times= 16
    configs.append(config(buyer=fcustom(vama2,fast=  4,slow= 89,pre_length= 21,ma_standard=230))) 	#balance=4130,times= 16
    configs.append(config(buyer=fcustom(vama2,fast=  9,slow= 84,pre_length=151,ma_standard=215))) 	#balance=12419,times= 23
    
    #ma3
    configs.append(config(buyer=fcustom(ma3,fast= 32,mid=  7,slow= 92,ma_standard=185,extend_days= 29))) 	#balance=3332,times=719
    configs.append(config(buyer=fcustom(ma3,fast= 32,mid= 13,slow= 92,ma_standard=160,extend_days= 27))) 	#balance=5137,times=488
    configs.append(config(buyer=fcustom(ma3,fast= 32,mid= 15,slow= 92,ma_standard=165,extend_days= 27))) 	#balance=6678,times=393
    configs.append(config(buyer=fcustom(ma3,fast= 19,mid= 36,slow=160,ma_standard=165,extend_days= 31))) 	#balance=2125,times=1455
    configs.append(config(buyer=fcustom(ma3,fast= 19,mid= 31,slow=155,ma_standard=225,extend_days= 25))) 	#balance=2290,times=1716
    configs.append(config(buyer=fcustom(ma3,fast= 19,mid= 26,slow=160,ma_standard=240,extend_days= 31))) 	#balance=2504,times=1478
    configs.append(config(buyer=fcustom(ma3,fast= 23,mid= 26,slow=150,ma_standard=240,extend_days= 31))) 	#balance=2857,times=1622
    configs.append(config(buyer=fcustom(ma3,fast= 24,mid= 31,slow=157,ma_standard=240,extend_days= 31))) 	#balance=3147,times=1340

    return configs

def prepare_order(sdata):
    d_posort('g5',sdata.values(),distance=5)        
    d_posort('g20',sdata.values(),distance=20)    
    d_posort('g120',sdata.values(),distance=120)     
    d_posort('g250',sdata.values(),distance=250)     

def run_body(sdata,dates,begin,end,xbegin):
    
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller = atr_seller_factory(stop_times=2000,trace_times=3000)
    #seller = csc_func

    configs = prepare_configs(seller,pman,dman)
    batch(configs,sdata,dates,xbegin,cmediator=myMediator)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_configs('atr_ev.txt',configs,xbegin,end)

def run_merge_body(sdata,dates,begin,end,xbegin):
    
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller = atr_seller_factory(stop_times=2000,trace_times=3000)
    #seller = csc_func

    configs = prepare_configs(seller,pman,dman)
    result,strade = merge(configs,sdata,dates,xbegin,pman,dman,cmediator=myMediator)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    
    save_merged('atr_merged.txt',result,strade,xbegin,end)

def run_mm_body(sdata,dates,begin,end,xbegin):
    from time import time
    tbegin = time()

    #kvs = dict(fast=15,mid=94,slow=209,sma=24,ma_standard=202,extend_days=30)
    #seller = fcustom(atr_seller,**kvs) #atr_seller_factory(stop_times=1500)
    seller = atr_seller_factory()
    myMediator=MM_Mediator
    configs = prepare_configs(seller,None,None)
    
    mm_batch(configs,sdata,dates,xbegin)

    tend = time()
    print u'计算耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_mm_configs('mm_ev.txt',configs,xbegin,end)
    #save_configs('atr_ev_mm_test.txt',configs,begin,end)

def run_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata)
    run_body(sdata,dates,begin,end,xbegin)

def run_merge_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata)
    run_merge_body(sdata,dates,begin,end,xbegin)


def run_mm_main(dates,sdata,idata,catalogs,begin,end,xbegin):
    prepare_order(sdata)    
    run_mm_body(sdata,dates,begin,end,xbegin)




if __name__ == '__main__':
    logging.basicConfig(filename="run.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    begin,end = 20010101,20050901
    xbegin = 20020601
    from time import time
    tbegin = time()
    
    dates,sdata,idata,catalogs = prepare_all(begin,end,[],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601988','SH600050'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601988'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH601398'],[ref_code])        
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SZ000630'],[ref_code])        
    #dates,sdata,idata,catalogs = prepare_all(begin,end,get_codes(),[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,get_codes(source='SZSE'),[ref_code])
    tend = time()
    print u'数据准备耗时: %s' % (tend-tbegin)    
    import psyco
    psyco.full()

    run_main(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_merge(dates,sdata,idata,catalogs,begin,end,xbegin)
    #run_mm_main(dates,sdata,idata,catalogs,begin,end,xbegin)
