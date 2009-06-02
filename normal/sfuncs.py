# -*- coding: utf-8 -*-

#指定股票的测试运行脚本

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *
from wolfox.fengine.core.d1ex import tmax,derepeatc,derepeatc_v,equals,msum
from wolfox.fengine.core.d1match import *
from wolfox.fengine.core.d1indicator import cmacd,score2
from wolfox.foxit.base.tutils import linelog
from time import time

import logging
logger = logging.getLogger('wolfox.fengine.normal.sfuncs')    

def tsvama2(stock,fast,slow):
    t = stock.transaction
    svap,v2i = stock.svap_ma_67 
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama2.__name__,stock.code))
    return gand(stock.golden,msvap,stock.above)

def tsvama2a(stock,fast=20,slow=100):
    ''' svama两线交叉
        加vfilter
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67 
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)

    ss = cross_fast_slow
    msvap = transform(ss,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama2.__name__,stock.code))

    vdiff,vdea = cmacd(t[VOLUME])

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = vma_s < vma_l * 7/8
 
    linelog('%s:%s' % (tsvama2a.__name__,stock.code))
    return gand(stock.golden,msvap,stock.above,vfilter)


def tsvama2b(stock,fast=20,slow=170):
    ''' svama两线交叉
        另加smacd,vfilter
    '''
    t = stock.transaction
    svap,v2i = stock.svap_ma_67 
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)

    sdiff,sdea = cmacd(svap)
    ss = gand(cross_fast_slow,strend(sdiff-sdea)>0)
    #ss = cross_fast_slow
    msvap = transform(ss,v2i,len(t[VOLUME]))
    linelog('%s:%s' % (tsvama2.__name__,stock.code))

    vdiff,vdea = cmacd(t[VOLUME])

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = vma_s < vma_l * 7/8
 
    linelog('%s:%s' % (tsvama2b.__name__,stock.code))
    return gand(stock.golden,msvap,stock.above,vfilter)


def pmacd(stock):
    t = stock.transaction
    pdiff,pdea = cmacd(t[CLOSE])
    dcross = gand(cross(pdea,pdiff),strend(pdiff)>0,strend(pdea>0))
    linelog(stock.code)
    #return gand(dcross,stock.golden,stock.above,cs,pdea>0,pdea<12000)
    return gand(dcross,stock.thumb,stock.above,stock.silver,pdea>0,pdea<12000)

def nhigh(stock):#60高点
    t = stock.transaction
    mline = rollx(tmax(t[HIGH],60)) #以昨日的60高点为准
    dcross = cross(mline,t[HIGH])>0    
    g = gand(stock.g5>=stock.g20,stock.thumb)
    #linelog(stock.code)
    return gand(g,stock.silver,dcross,strend(stock.ma60)>0,stock.above)

def xma60(stock):
    ''' 碰到ma60后回升
        cs,g = gand(stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)    ##最佳
        评估:总盈亏值=13321,交易次数=45 期望值=6040
                总盈亏率(1/1000)=13321,平均盈亏率(1/1000)=296,盈利交易率(1/1000)=622
                赢利次数=28,赢利总值=14170
                亏损次数=17,亏损总值=849
                平盘次数=0
        
        #金手指
        评估:总盈亏值=33283,交易次数=173        期望值=2493
                总盈亏率(1/1000)=33283,平均盈亏率(1/1000)=192,盈利交易率(1/1000)=526
                赢利次数=91,赢利总值=39607
                亏损次数=82,亏损总值=6324
                平盘次数=0

        #金手指+cs<6600
        评估:总盈亏值=5530,交易次数=17  期望值=8333
                总盈亏率(1/1000)=5530,平均盈亏率(1/1000)=325,盈利交易率(1/1000)=705
                赢利次数=12,赢利总值=5727
                亏损次数=5,亏损总值=197
                平盘次数=0
        
        #银手指
        评估:总盈亏值=23766,交易次数=87 期望值=4706
                总盈亏率(1/1000)=23766,平均盈亏率(1/1000)=273,盈利交易率(1/1000)=574
                赢利次数=50,赢利总值=25929
                亏损次数=37,亏损总值=2163
                平盘次数=0

        sync,stock.above,stock.t120,s.g20 >= s.g60,s.g60 >= s.g120,s.g120 >= s.g250,s.g5>=3000,s.g5<=8000,stock.silver
        评估:总盈亏值=11019,交易次数=36 期望值=4781
                总盈亏率(1/1000)=11019,平均盈亏率(1/1000)=306,盈利交易率(1/1000)=777
                赢利次数=28,赢利总值=11535
                亏损次数=8,亏损总值=516
                平盘次数=0
                
    '''
    t = stock.transaction
    water_line = stock.ma60*115/100   #上方15处
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,7)
    linelog(stock.code)
    #return gand(sync,stock.above,stock.t120,stock.golden,cs)    
    return gand(sync,stock.above,stock.t120,stock.thumb,stock.silver)

def wvad(stock):
    t = stock.transaction
    vad = (t[CLOSE]-t[OPEN])*t[VOLUME]/(t[HIGH]-t[LOW]) / 10000
    svad = msum2(vad,24)
    ma_svad = ma(svad,6)
    #ecross = gand(stock.golden,cs,cross(ma_svad,vad)>0,strend(ma_svad)>0,stock.t120,stock.above)
    ecross = gand(stock.thumb,stock.silver,cross(ma_svad,vad)>0,strend(ma_svad)>0,stock.t120,stock.above)
    linelog(stock.code)
    return ecross

def temv(stock):
    '''
    name:Mediator:<temv:atr_seller:up_sector=2,trace_times=3000,stop_times=1200,covered=10:make_trade_signal_advanced:B1S1>
    pre_ev:	评估:总盈亏值=2244,交易次数=14	期望值=4210	
		总盈亏率(1/1000)=2244,平均盈亏率(1/1000)=160,盈利交易率(1/1000)=428
		赢利次数=6,赢利总值=2555
		亏损次数=8,亏损总值=311
		平盘次数=0
		闭合交易明细:
    
    '''
    t = stock.transaction
    ts = cached_zeros(len(t[CLOSE]))
    ekey = 'emv'
    em = emv(t[HIGH],t[LOW],t[VOLUME])
    mv = msum2(em,14)
    semv = ma(mv,9)
    ecross = gand(stock.thumb,stock.silver,cross(ts,mv)>0,strend(semv)>0,stock.t120,stock.above)
    linelog(stock.code)
    return ecross
    
def vmacd_ma4(stock):
    t = stock.transaction
    
    vdiff,vdea = cmacd(t[VOLUME])
    dcross = gand(cross(vdea,vdiff)>0,strend(vdiff)>0,strend(vdea)>0)

    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)

    c_ex = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=8500)
    cs = catalog_signal_cs(stock.c60,c_ex)    
    return gand(g,cs,dcross,stock.above,strend(stock.ma60)>0,vdea>=0,vdea<=12000)

def ma4(stock): #3X10
    t = stock.transaction
    fma = ma(t[CLOSE],3)
    dcross = gand(cross(stock.ma10,fma),strend(fma)>0,strend(stock.ma10)>0,strend(stock.ma20)>0,strend(stock.ma60)>0,stock.t120>0)
    linelog(stock.code)
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    #return gand(stock.golden,cs,dcross,stock.above,stock.t120)
    return gand(g,stock.silver,dcross,stock.above)    

def vmacd(stock):
    t = stock.transaction
    vdiff,vdea = cmacd(t[VOLUME])
    dcross = gand(cross(vdea,vdiff),strend(vdiff)>0,strend(vdea>0))
    linelog(stock.code)
    return gand(dcross,stock.golden,stock.t120,stock.silver,vdea>0,vdea<12000)

def gx60(stock,fast=5,slow=20):
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    g60 = stock.g60
    ma_fast = ma(g60,fast)
    ma_slow = ma(g60,slow)
    trend_ma_fast = strend(ma_fast) > 0
    trend_ma_slow = strend(ma_slow) > 0    
    cross_fast_slow = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast,trend_ma_slow)

    #c_ex = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)

    linelog(stock.code)

    ma_120 = ma(stock.g120,5)   #平滑一下
    ma_250 = ma(stock.g250,5)
    trend_ma_120 = strend(ma_120) > 0
    trend_ma_250 = strend(ma_250) > 0

    return gand(cross_fast_slow,g,stock.silver,stock.above,stock.t120,trend_ma_120,trend_ma_250)

def gx250(stock,fast=10,slow=67):
    t = stock.transaction
    g = gand(stock.g5 >= stock.g20,stock.g20 >= stock.g60,stock.g60 >= stock.g120,stock.g120 >= stock.g250)
    gx = stock.g250
    ma_fast = ma(gx,fast)
    ma_slow = ma(gx,slow)
    trend_ma_fast = strend(ma_fast) > 0
    trend_ma_slow = strend(ma_slow) > 0    
    cross_fast_slow = gand(cross(ma_slow,ma_fast)>0,trend_ma_fast,trend_ma_slow)

    #c_ex = lambda c,s:gand(c.g5 >= c.g20,c.g20>=c.g60,c.g60>=c.g120,c.g120>=c.g250,s<=6600)

    linelog(stock.code)

    ma_120 = ma(stock.g120,5)   #平滑一下
    ma_250 = ma(stock.g250,5)
    trend_ma_120 = strend(ma_120) > 0
    trend_ma_250 = strend(ma_250) > 0

    return gand(cross_fast_slow,stock.golden,stock.silver,stock.above,stock.t120,trend_ma_120,trend_ma_250)


def gcs(stock):
    '''
        20000101-20090101
        评估:总盈亏值=29163,交易次数=206        期望值=1880
                总盈亏率(1/1000)=29163,平均盈亏率(1/1000)=141,盈利交易率(1/1000)=422
                赢利次数=87,赢利总值=38080
                亏损次数=118,亏损总值=8917
                平盘次数=1
    '''
    t = stock.transaction
    ma5 = ma(t[CLOSE],5)
    linelog(stock.code)
    sbuy = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120)
    return sbuy

def xgcs(stock):
    t = stock.transaction
    ma5 = ma(t[CLOSE],5)
    linelog(stock.code)
    si = score2(t[CLOSE],t[VOLUME])
    mxi = gand(msum(si,5)>=-100,msum(si,5)<=0)
    sbuy = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120,mxi)
    return sbuy

def xgcs0(stock):
    ''' 下穿0线
        评估:总盈亏值=23464,交易次数=81 期望值=4013
                总盈亏率(1/1000)=23464,平均盈亏率(1/1000)=289,盈利交易率(1/1000)=617
                赢利次数=50,赢利总值=25703
                亏损次数=31,亏损总值=2239
                平盘次数=0
    '''
    t = stock.transaction
    ma5 = ma(t[CLOSE],5)
    linelog(stock.code)

    si = score2(t[CLOSE],t[VOLUME])
    zs = cached_zeros(len(t[CLOSE]))
    mxi = cross(zs,si)<0

    sbuy = gand(stock.golden,stock.silver,stock.above,ma5>stock.ma10,stock.ref.t120,mxi)
    return sbuy


def mgcs(stock):
    t = stock.transaction
    linelog(stock.code)
    s = stock
    g = gand(s.g20 >= s.g60,s.g60 >= s.g120,s.g20>=3000,s.g20<=8000,s.g20<=s.g120+1000)     ######
    pdiff,pdea = cmacd(t[CLOSE])
    sbuy = gand(g,pdiff>=225,pdiff<=350,stock.above,stock.ref.t120,strend(stock.ma20)>0,strend(stock.ma60)>0,stock.t120,stock.ref.above)
    return sbuy

def spring(stock,threshold=-30):
    ''' 对于结果
        下影越短越好，close-low/close 也是越短越好
    '''
    t = stock.transaction
    linelog('spring:%s' % stock.code)
    
    s11 = gand(stock.ks >=-5,stock.ks<0,stock.ref.ks<=threshold)
    s12 = gand(stock.ks >=5,stock.ks<20,stock.ref.ks<=threshold)
    s1 = bor(s11,s12)
    s_tt = gand(s1,stock.thumb,stock.t120)
    s21 = gand(stock.ks>=5,stock.ks<75,stock.ref.ks<=threshold)
    s_aa = gand(s21,stock.thumb,stock.above)

    signals = bor(s_aa,s_tt)

    ref = stock.ref
    sbuy = signals #gand(signals,greater(ref.ma10,ref.ma20),greater(ref.ma20,ref.ma60))

    svap,v2i = stock.svap_ma_67
    sdiff,sdea = cmacd(svap,19,39)
    ssignal = gand(strend(sdiff)>0,strend(sdiff-sdea)>0)

    msvap = transform(ssignal,v2i,len(t[VOLUME]))


    return gand(sbuy,msvap)


def cma2(stock,fast,slow,gfrom=0,gto=8500):  
    ''' 传统的ma2
        5 X 20
        评估:总盈亏值=11488,交易次数=54 期望值=3164
                总盈亏率(1/1000)=11488,平均盈亏率(1/1000)=212,盈利交易率(1/1000)=685
                赢利次数=37,赢利总值=12628
                亏损次数=17,亏损总值=1140
                平盘次数=0
            g5: 4000-8000
            评估:总盈亏值=10980,交易次数=38 期望值=4571
                总盈亏率(1/1000)=10980,平均盈亏率(1/1000)=288,盈利交易率(1/1000)=763
                赢利次数=29,赢利总值=11547
                亏损次数=9,亏损总值=567
                平盘次数=0
        5 X 13
        评估:总盈亏值=39727,交易次数=213        期望值=2952
                总盈亏率(1/1000)=39727,平均盈亏率(1/1000)=186,盈利交易率(1/1000)=553
                赢利次数=118,赢利总值=45746
                亏损次数=95,亏损总值=6019
                平盘次数=0
            #g5:7000-8500
            评估:总盈亏值=33922,交易次数=149        期望值=3603
                总盈亏率(1/1000)=33922,平均盈亏率(1/1000)=227,盈利交易率(1/1000)=617
                赢利次数=92,赢利总值=37550
                亏损次数=57,亏损总值=3628
                平盘次数=0
 
    '''
    t = stock.transaction
    water_line = ma(t[CLOSE],slow)
    dcross = cross(water_line,ma(t[CLOSE],fast))

    up_cross = dcross > 0

    linelog(stock.code)
    return gand(up_cross,stock.above,stock.t120,stock.g5>=stock.g20+500,stock.g20>=stock.g60+500,stock.g60>=stock.g120,stock.g5>=gfrom,stock.g5<=gto)


def cma1(stock,length=30,covered=7):  #
    t = stock.transaction
    
    water_line = ma(t[CLOSE],length)
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,covered=7)
    return gand(sync,stock.above,stock.t120,stock.thumb,stock.silver)


def x30(t):
    water_line = ma(t[CLOSE],30)
    dcross = cross(water_line,t[LOW])
    up_cross = dcross > 0
    down_cross = dcross < 0
    sync = sfollow(down_cross,up_cross,7)
    return sync

def tsvama2x(stock,fast=20,slow=100):
    ''' svama两线交叉
    '''
    t = stock.transaction
    g = stock.golden
    svap,v2i = stock.svap_ma_67
    ma_svapfast = ma(svap,fast)
    ma_svapslow = ma(svap,slow)
    trend_ma_svapfast = strend(ma_svapfast) > 0
    trend_ma_svapslow = strend(ma_svapslow) > 0
    cross_fast_slow = gand(cross(ma_svapslow,ma_svapfast)>0,trend_ma_svapfast,trend_ma_svapslow)
    msvap = transform(cross_fast_slow,v2i,len(t[VOLUME]))
    signal = msvap
    s2 = x30(t)
    sbuy = sfollow(signal,s2,10)
    linelog('%s:%s' % (tsvama2x.__name__,stock.code))
    return gand(sbuy,stock.above,stock.thumb,stock.silver)


def gmacd_old(stock): #
    ''' 
        20010701-20090101效果不好，但能持平
        20080701开始效果非常好
        ll5 = rollx(t[LOW],5),   hinc = t[HIGH] * 1000 / ll5
        ll10 = rollx(t[LOW],10),    hh10 = tmax(t[HIGH],10), rhl10 = hh10 * 1000/ll10
        lfilter = hinc<1200 and rhl10<1500
        ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30),t[LOW]),5),之后+lfilter,2115/704/846
        ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30)<0,t[LOW]),5),之后+lfilter,2213/759/595
            g60:4500-8500:  2946/821/286
        ss1=sfollow(cross(mdea,mdiff) > 0,vdiff<vdea), 然后再sfollow(ss1,cross(ma(t[CLOSE],30)<0,t[LOW]),10),之后+lfilter,2392/746/844    
            g60:0-3000:1457/670/273
            g60:3000-6000: 2709/788/402
            g60:6000-!: 2696/758/273
            g60:6000-8500: 2781/775/232
            g60:>8500:  2193/632/49
            g60:4500-8500:  3078/793/411
            g60:4500-7500:  2888/797/345
            g60:5000-8000:  2925/796/324
            数量太多,需要进一步筛选
        ss1=sfollow(cross(mdea,mdiff) > 0,gand(vdiff>vdea,pdiff>pdea)), 然后再sfollow(ss1,cross(ma(t[CLOSE],30)<0,t[LOW]),10),2392/746/844    
            mdiff>=mdea
            g60:4500-8500:3036/800/451
            g20:4500-8500:3886/817/465  #不需要hinc<1200，只需要rhl10<1500,而且效果也有限
            但这个滤掉了600121,600756,000961,600997等
            g20:5000-9000:3877/845/297   
            ####g20:5000-9500:3937/840/300    #去掉mdiff>=mdea,3571/841/416
                添加 strend(stock.ref.ma60)>0   4063/847/295
                above改为13>30>60>120
                above = gand(ma(c,13) > ma30,ma30>stock.ma60,stock.ma60>stock.ma120)
                signal = gand(ss,above,stock.t120,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma60)>0)
                4217/860/294
            g20:5000-10000:3425/833/306
            g20:6000-9500:3500/847/203
            g20:5000-6000:4097/840/113
            g20:4500-9500:3933/803/346
        仍然无法继续甄别超级强势股,如600756,000961的启动阶段,能够通过cmacd(mdea,mdiff)>0找到初始信号,但无法从噪声中甄别出来
        因为他们不触碰30线,需要进一步考虑
        ss1不变.
        x3 = gand(strend(ma(t[CLOSE],5))>0,strend(stock.ma10)>0,strend(stock.ma20)>0,strend(stock.ma60)>0)
        ss = sfollow(ss1,x3,10)
        
    '''
    t = stock.transaction
    
    mdiff,mdea = cmacd(stock.g60)
    ldiff,ldea = cmacd(stock.g120)
    lldiff,lldea = cmacd(stock.g250)

    vdiff,vdea = cmacd(t[VOLUME])
    pdiff,pdea = cmacd(t[CLOSE])


    #sfilter = vdiff<vdea
    #sfilter = vdiff<vdea
    sfilter = gand(vdiff>vdea,pdiff>pdea)

    xcross = cross(mdea,mdiff) > 0  
    #xcross = cross(mdiff,mdea) > 0  

    linelog(stock.code)


    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    ss1 = sfollow(xcross,sfilter,5)
    
    x2 = cross(ma(t[CLOSE],30),t[LOW]) < 0
    
    ss = sfollow(ss1,x2,10)

    gf1 = gand(stock.g20>5000,stock.g20<9500)

    c = t[CLOSE]
    ma30 = ma(c,30)
    above = gand(ma(c,13) > ma30,ma30>stock.ma60,stock.ma60>stock.ma120)

    #signal = gand(xcross,stock.above,stock.t120,t[VOLUME]>0,hinc<1200,rhl10<1500,gfilter)
    signal = gand(ss,above,stock.t120,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma60)>0)
    
    return signal

def gmacd(stock): #
    '''
        mxi: (-100,0], vfilter:>1.5
                2001.7-2008.12
                评估:总盈亏值=3070,交易次数=57  期望值=670
                总盈亏率(1/1000)=3070,平均盈亏率(1/1000)=53,盈利交易率(1/1000)=298
                赢利次数=17,赢利总值=6164
                亏损次数=39,亏损总值=3094
                平盘次数=1
                2008-2009.5
                评估:总盈亏值=1415,交易次数=8   期望值=1000
                总盈亏率(1/1000)=1415,平均盈亏率(1/1000)=176,盈利交易率(1/1000)=1000
                赢利次数=8,赢利总值=1415
                亏损次数=0,亏损总值=0

        mxi: (-100,0], vfilter:>1.33
                2001.7-2008.12
                评估:总盈亏值=6520,交易次数=26  期望值=41666
                总盈亏率(1/1000)=6520,平均盈亏率(1/1000)=250,盈利交易率(1/1000)=961
                赢利次数=25,赢利总值=6526
                亏损次数=1,亏损总值=6
                平盘次数=0
                2008-2009.5
                评估:总盈亏值=3926,交易次数=111 期望值=492
                总盈亏率(1/1000)=3926,平均盈亏率(1/1000)=35,盈利交易率(1/1000)=279
                赢利次数=31,赢利总值=9542
                亏损次数=79,亏损总值=5616
                平盘次数=1
            macd: 35,77
            评估:总盈亏值=5074,交易次数=91  期望值=763
                总盈亏率(1/1000)=5074,平均盈亏率(1/1000)=55,盈利交易率(1/1000)=296
                赢利次数=27,赢利总值=9624
                亏损次数=63,亏损总值=4550
                平盘次数=1
            36:78
            评估:总盈亏值=4841,交易次数=84  期望值=780
                总盈亏率(1/1000)=4841,平均盈亏率(1/1000)=57,盈利交易率(1/1000)=297
                赢利次数=25,赢利总值=9103
                亏损次数=58,亏损总值=4262
                平盘次数=1
        
        目前取1.33
        改成cmacd(svap,19,39)无改进
    '''
    t = stock.transaction
    
    mdiff,mdea = cmacd(stock.g60)

    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = gand(vma_s > vma_l * 4/3)
    
    xcross = cross(mdea,mdiff) > 0  

    linelog(stock.code)

    ll10 = rollx(t[LOW],10)
    hh10 = tmax(t[HIGH],10)
    rhl10 = hh10 * 1000/ll10

    c = t[CLOSE]
    ma30 = ma(c,30)
    above = gand(ma(c,13) > ma30,ma30>stock.ma60,stock.ma60>stock.ma120)


    svap,v2i = stock.svap_ma_67
    sdiff,sdea = cmacd(svap,36,78)
    ssignal = gand(sdiff < sdea,strend(sdiff)<0,strend(sdiff-sdea)>0)

    msvap = transform(ssignal,v2i,len(t[VOLUME]))

    x2 = cross(ma(t[CLOSE],30),t[LOW]) < 0

    ss = sfollow(xcross,x2,10)
    
    gf1 = gand(stock.g20>5000,stock.g20<9500)

    si = score2(t[CLOSE],t[VOLUME])
    msi = msum(si,5)
    mxi = gand(msi>=-100,msi<=0)
    
    signal = gand(ss,above,stock.t120,strend(stock.ma60)>0,t[VOLUME]>0,gf1,rhl10<1500,mdiff>=mdea,strend(stock.ref.ma60)>0,vfilter,msvap,mxi)
    
    return signal


def smacd(stock):
    '''
        36,78
        评估:总盈亏值=45847,交易次数=379        期望值=1643
                总盈亏率(1/1000)=45847,平均盈亏率(1/1000)=120,盈利交易率(1/1000)=448
                赢利次数=170,赢利总值=61166
                亏损次数=209,亏损总值=15319
                平盘次数=0
    
        36,78,     vfilter = vma_s < vma_l 
        评估:总盈亏值=22086,交易次数=126        期望值=2302
                总盈亏率(1/1000)=22086,平均盈亏率(1/1000)=175,盈利交易率(1/1000)=539
                赢利次数=68,赢利总值=26550
                亏损次数=58,亏损总值=4464
                平盘次数=0
            #20080701-20090531:
            评估:总盈亏值=811,交易次数=63   期望值=214
                总盈亏率(1/1000)=811,平均盈亏率(1/1000)=12,盈利交易率(1/1000)=396
                赢利次数=25,赢利总值=2976
                亏损次数=38,亏损总值=2165
                平盘次数=0
            
        ####36,78,     vfilter = vma_s < vma_l * 7/8
        评估:总盈亏值=8997,交易次数=45  期望值=2618
                总盈亏率(1/1000)=8997,平均盈亏率(1/1000)=199,盈利交易率(1/1000)=511
                赢利次数=23,赢利总值=10690
                亏损次数=22,亏损总值=1693
                平盘次数=0
                闭合交易明细:
            #20080701-20090531:
                评估:总盈亏值=1067,交易次数=20  期望值=1060
                总盈亏率(1/1000)=1067,平均盈亏率(1/1000)=53,盈利交易率(1/1000)=600
                赢利次数=12,赢利总值=1470
                亏损次数=8,亏损总值=403
                平盘次数=0
    '''
    t = stock.transaction
    #g = gand(stock.g20 >= stock.g60+1000,stock.g60 >= stock.g120+1000,stock.g20>=3000,stock.g20<=8000)
    #g = np.ones_like(stock.g5)
 
    svap,v2i = stock.svap_ma_67 

    diff,dea = cmacd(svap,36,78)
    dcross = gand(cross(dea,diff)>0,strend(diff)>0,strend(dea)>0)

    msvap = transform(dcross,v2i,len(t[VOLUME]))

    linelog(stock.code)
    vma_s = ma(t[VOLUME],13)
    vma_l = ma(t[VOLUME],30)

    vfilter = vma_s < vma_l * 7/8

    return gand(stock.golden,stock.above,msvap,vfilter)

