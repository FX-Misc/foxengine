# -*- coding: utf-8 -*-

"""
���õ��㷨�����
�����ֻ�����Ƿ��ܹ�ִ�У����������߼�
"""

import numpy as np

from wolfox.fengine.core.utils import fcustom
from wolfox.fengine.core.base import *
from wolfox.fengine.core.d1 import *
from wolfox.fengine.core.d1ex import *
from wolfox.fengine.core.d1indicator import *
from wolfox.fengine.core.d1kline import *


def swingin(shigh,slow,covered,threshold):
    ''' ����shigh,slow���covered���ڵĲ�������С��threshold
        ������i����[0:len(shigh)),��shigh[i] >= slow[i]
        ����������ԣ�����ȷ�����������Ļ��ǵ���ȥ
    '''
    #print swing2(shigh,slow,covered)
    return lesser_equals(swing2(shigh,slow,covered),threshold)
    
def swingin1(source,covered,threshold):
    ''' ����source���covered���ڵĲ�������С��threshold
        ����������ԣ�����ȷ�����������Ļ��ǵ���ȥ
    '''
    return lesser_equals(swing(source,covered),threshold)

def up_under(shigh,slow,covered,threshold):
    ''' ����shigh,slow���covered������������С��threshold
        ������i����[0:len(shigh)),��shigh[i] >= slow[i]
        �����Ƿ�����
    '''
    srange,sdiff = iswing2(shigh,slow,covered)
    #print srange,sdiff
    up2threshold = band(srange >= threshold,sdiff >= 0)
    #print up2threshold
    return bnot(up2threshold)

def upconfirm(sopen,sclose,shigh):#����ͻ��ȷ��
    sksize = ksize(sopen,sclose)
    sksign = ksign(sopen,sclose)
    
    posconsecutive = consecutive(sksign,'a')  #����������Ŀ
    middleconsecutive = consecutive(sksize,'b')  #�����е�ʵ����Ŀ

    #����������
    onebigpos = np.logical_and(sksign == 'a',sksize == 'a')
    #����2���е�����
    twomiddlepos = np.logical_and( posconsecutive > 1, middleconsecutive > 1)
    #����3������
    threepos = posconsecutive > 2
    ###�����
    #����Ӱ����
    threeupextend = kscmp(sopen,sclose,shigh,sclose,tbig=3000) == 'a'  #��Ӱ/ʵ�� > 3Ϊ��

    #print kscmp(sopen,sclose,shigh,tmax(sopen,sclose),tbig=3000)
    sconfirm = gor(onebigpos,twomiddlepos,threepos)
    #return sconfirm
    return band(sconfirm,np.logical_not(threeupextend))

def upveto(sopen,sclose,shigh,slow):   #����������
    sksize = ksize(sopen,sclose)
    sksign = ksign(sopen,sclose)

    negconsecutive = consecutive(sksign,'b')  #����������Ŀ
    middleconsecutive = consecutive(sksize,'b')  #�����е�ʵ����Ŀ
    smallconsecutive = consecutive(sksize,'c')  #����Сʵ����Ŀ
    
    #������
    onebig = np.logical_and(sksign == 'b',sksize == 'a')
    #��������������
    twomiddle = np.logical_and(negconsecutive > 1,middleconsecutive > 1)
    #��������С����
    threesmall = np.logical_and(negconsecutive > 2,smallconsecutive > 2)

    return gor(onebig,twomiddle,threesmall)

def sellconfirm(sopen,sclose,shigh,slow):   #����ȷ��������Ǵ�����������
    sksize = ksize(sopen,sclose)
    sksign = ksign(sopen,sclose)
    #���������
    big_or_middle = np.logical_or(sksize == 'a',sksize =='b')
    bm_and_pos = np.logical_and(sksign == 'a',big_or_middle)
    return bnot(bm_and_pos)

####sell_func�����stock.downlimit���и�ֵ
def simplesell(sbuy,shigh,slow,threshold):
    downl = downlimit(shigh,sbuy,threshold)
    return slow - downl < 0

def tsimplesell(sbuy,shigh,slow,threshold):
    downl = tdownlimit(shigh,sbuy,threshold)
    return slow - downl < 0

def confirmedsell(sbuy,sopen,sclose,shigh,slow,ssignal,threshold):  #ssignalΪ�����������޵������ߣ�һ��Ϊsclose��slow
    downl = downlimit(shigh,sbuy,threshold)
    return band(ssignal-downl <0,sellconfirm(sopen,sclose,shigh,slow))   #����intֵ���ڲμ������ת��

def confirmedselll(sbuy,sopen,sclose,shigh,slow,threshold): #��slowΪ��������
    downl = downlimit(shigh,sbuy,threshold)
    return band(slow-downl <0,sellconfirm(sopen,sclose,shigh,slow))   #����intֵ���ڲμ������ת��

def confirmedsellc(sbuy,sopen,sclose,shigh,slow,threshold): #��scloseΪ��������
    downl = downlimit(shigh,sbuy,threshold)
    return band(sclose-downl <0,sellconfirm(sopen,sclose,shigh,slow)) #����intֵ���ڲμ������ת��

def downup(source1,source2,belowdays,crossdays=3):
    ''' �ж�source2����source1֮�ϣ�Ȼ��crossdays����(Ϊ�����غϣ�Ĭ��Ϊ3)���£�ͣ��n�����
    '''
    s2_1 = source2 - source1
    s2_lt_1 = s2_1 < 0 #tfilter_lt(s2_1)
    s2_gt_1 = s2_1 > 0 # tfilter_gt(s2_1)
    sdown = sfollow(s2_gt_1,s2_lt_1,crossdays)
    sdown_up = sfollow(sdown,s2_gt_1,belowdays)  #belowdays֮�ڻ�ȥ
    return sdown_up

def _limit_adjuster_deprecated(css,cls,covered):#covered���ܴ���127��������, np.sign(bool array)���ص���int8����
    ''' css:ѹ�����source_signal,cls:ѹ�����limit_signal
        ����cls�ǿ��յ���Щcss�ź�,ʹ���Ӻ�covered֮�ڵķ�ͣ����,����ȡ��(�����covered�ն�ͣ��)
        ���ش�����css
        ������������Ȱ�covered��չ���źţ��ڿ���ͣ���գ�Ȼ���ٽ���derepeat���������̫�����ˣ�����
        �����������źŵ����գ��������covered-1��2�������źţ���һ���źű���Ӧ������covered��λ��,�����ﱻ������. 
            ���������Ϊ����covered֮�ڵ����ź�,��covered��Сʱ,������ʵ��Ӱ��(��Ϊ������������û���������ź�,�ʴ�������Ϊ��Ч�ź�)
            �������cover�����repeat,ʹ�������ź�����,��ת�������Ϊͣ��Ĵ��ڵ����м�Ͽ��Ӷ�����źű��Ƴ�,��Ϊ����
    '''
    css_covered = repeat(css,covered)
    #print css,cls,css_covered,derepeat(band(css_covered>0,bnot(cls)))
    #print '_ad',band(css_covered > 0,bnot(cls))[-20:-5].tolist(),derepeat(band(css_covered > 0,bnot(cls)),covered)[-20:-5].tolist()
    return derepeat(band(css_covered > 0,bnot(cls)),covered)    
    
def limit_adjust_deprecated(source_signal,limit_signal,trans_signal,covered=10):#covered���ܴ���127��������, np.sign(bool array)���ص���int8����
    ''' ����ͣ���ź�limit_signal�ͽ������ź�trans_signal����ԭʼ�źţ�ʹԭʼ�źűܿ�ͣ�嵽������
        ������covered��ԭ����������ͣ�����м����ͣ���պ�,�źŶ෢. ���������makke_trade֮��ĺ��������
        ֻ��covered=2ʱ,�������������
        covered=10�����10��ͣ�壬��������ܵ��µ�ͣ����������źű�����
    '''
    adjuster = fcustom(_limit_adjuster_deprecated,covered=covered)
    return smooth(trans_signal,source_signal,limit_signal,sfunc=adjuster)

def limit_adjust(source_signal,limit_signal,trans_signal):
    ''' ����ͣ���ź�limit_signal�ͽ������ź�trans_signal����ԭʼ�źţ�ʹԭʼ�źűܿ�ͣ�嵽������
        ��ͣ����Ҳ��ͬͣ����
    '''
    signal2 = band(trans_signal,limit_signal==0) #�����ձ������㲻��ͬ��ͣ����
    return smooth_simple(signal2,source_signal)

def BS_DUMMY(trans,sbuy,ssell):
    return sbuy,ssell

def B0S0(trans,sbuy,ssell):
    ''' �����źŶ��ڵ���ʵ��
        tΪstock.transaction
        ���ؾ����ź�������ͣ���ͣ�ƴ����sbuy,ssell
    '''
    #print 'input rolled:',sbuy,ssell
    up_limit_line = limitup1(trans[CLOSE])
    down_limit_line = limitdown1(trans[CLOSE])
    #print 'begin adjust:',up_limit_line,down_limit_line
    sbuy = limit_adjust(sbuy,up_limit_line,trans[VOLUME])
    #print ssell[-20:-5].tolist(),down_limit_line[-20:-5]
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
    #print ssell[-20:-5].tolist()
    #print 'end adjust:',ssell
    return sbuy,ssell

def B0S1(trans,sbuy,ssell):
    ''' �����źŵ���,�����źŴ���
        tΪstock.transaction
        ���ؾ����ź�������ͣ���ͣ�ƴ����sbuy,ssell
    '''
    ssell = roll0(ssell)
    #print 'input rolled:',sbuy,ssell
    up_limit_line = limitup1(trans[CLOSE])
    down_limit_line = limitdown2(trans[HIGH],trans[LOW])
    #print 'begin adjust:',up_limit_line,down_limit_line,trans[VOLUME]
    sbuy = limit_adjust(sbuy,up_limit_line,trans[VOLUME])
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
    #print 'end adjust:',ssell
    return sbuy,ssell

def B1S0(trans,sbuy,ssell):
    ''' �������,��������
        tΪstock.transaction
        ���ؾ����ź�������ͣ���ͣ�ƴ����sbuy,ssell
        ��������ֻ�ܵ�һ����Ӱ�죬�����������ܵ����̵�ͣӰ��
    '''
    #print 'input:%s',sbuy.tolist()
    sbuy = roll0(sbuy)
    #print 'input,after roll:%s',sbuy.tolist()
    #print 'input rolled:',sbuy,ssell
    up_limit_line = limitup2(trans[HIGH],trans[LOW])
    down_limit_line = limitdown1(trans[CLOSE])
    #print 'begin adjust:',up_limit_line,down_limit_line,trans[VOLUME],sbuy
    sbuy = limit_adjust(sbuy,up_limit_line,trans[VOLUME])
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
    #print 'after limit adjust:%s',sbuy.tolist()    
    #print 'end adjust:',ssell
    return sbuy,ssell

def B1S1(trans,sbuy,ssell):
    ''' �����źŶ��Ǵ���ʵ��
        transΪstock.transaction
        ���ؾ����ź�������ͣ���ͣ�ƴ����sbuy,ssell
        ����������ֻ�ܵ�һ���ߵ�Ӱ��
    '''
    #print sbuy,np.sum(sbuy)
    sbuy,ssell = roll0(sbuy),roll0(ssell)
    #print 'input rolled:',sbuy,ssell
    up_limit_line = limitup2(trans[HIGH],trans[LOW])
    down_limit_line = limitdown2(trans[HIGH],trans[LOW])
    #print 'begin adjust:',up_limit_line,down_limit_line
    sbuy = limit_adjust(sbuy,up_limit_line,trans[VOLUME])
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
    #print 'end adjust:',ssell
    #print sbuy,np.sum(sbuy)
    return sbuy,ssell

B0S0.bshift = B0S1.bshift = lambda s : s   #bshift�Ƕ�buy�źŵĴ���,���������ź���. B0ϵ�в���ƫ�ơ�
B1S0.bshift = B1S1.bshift = lambda s : rollx(s)   #bshift�Ƕ�buy�źŵĴ���,���������ź���. B1ϵ������һλ

def atr_sell_func(sbuy,trans,satr,stop_times=3*BASE/2,trace_times=2*BASE,covered=10,up_sector=HIGH): 
    ''' 
        timesΪ��0.001Ϊ��λ�ı���
    '''
    #down_limit = tmax(trans[HIGH] - satr * times / BASE,covered)    #���covered�첨�����޵����ֵ
    down_limit = tracelimit((trans[OPEN]+trans[LOW])/2,trans[up_sector],sbuy,satr,stop_times,trace_times) #���źŵ��ն��ǽ�����(B1����»����һ��)�ļ۸�Ϊ�߼��㡣��Ϊ�����޷�֪�����ײ��ԡ�����ֹ�����ʱҲ������˼���
    #sdown = equals(cross(down_limit,trans[LOW]),-1)     #����
    sdown = under_cross(sbuy,down_limit,trans[LOW])
    #return band(sdown,sellconfirm(trans[OPEN],trans[CLOSE],trans[HIGH],trans[LOW])),down_limit
    return sdown,down_limit

def atr_sell_func_old(sbuy,trans,satr,times=BASE,covered=10,sector=LOW): 
    ''' 
        timesΪ��0.001Ϊ��λ�ı���
    '''
    down_limit = tmax(trans[HIGH] - satr * times / BASE,covered)    #���covered�첨�����޵����ֵ
    #sdown = equals(cross(down_limit,trans[sector]),-1)     #��ͼ۴���
    sdown = under_cross(sbuy,down_limit,trans[sector])
    return band(sdown,sellconfirm(trans[OPEN],trans[CLOSE],trans[HIGH],trans[LOW])),down_limit

def atr_seller(stock,buy_signal,stop_times=3*BASE/2,trace_times=2*BASE,covered=10,up_sector=HIGH,**kwargs): 
    ''' kwargsĿ�����������ò���������cruiser
        timesΪ0.001Ϊ��λ�ı���
        covered���������ߵ�ķ�Χ��
        ��d1idiom.atr_seller�ļ򵥰�װ
    '''
    trans = stock.transaction
    ssignal,down_limit = atr_sell_func(buy_signal,trans,stock.atr,stop_times,trace_times,covered,up_sector)
    stock.down_limit = down_limit
    #print buy_signal - ssignal
    return ssignal

def atr_seller_factory(stop_times=3*BASE/2,trace_times=2*BASE,covered=10,up_sector=HIGH):
    return fcustom(atr_seller,stop_times=stop_times,trace_times=trace_times,covered=covered,up_sector=up_sector)
