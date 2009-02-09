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
        �����Ƿ�����
    '''
    return swing2(shigh,slow,covered) > threshold
    

def swingin1(source,covered,threshold):
    ''' ����source���covered���ڵĲ�������С��threshold
        �����Ƿ�����
    '''
    return swing(source,covered) > threshold

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

def _limit_adjuster(css,cls,covered):#covered���ܴ���127��������, np.sign(bool array)���ص���int8����
    ''' css:ѹ�����source_signal,cls:ѹ�����limit_signal
        ����cls�ǿ��յ���Щcss�ź�,ʹ���Ӻ�covered֮�ڵķ�ͣ����,����ȡ��(�����covered�ն�ͣ��)
        ���ش�����css
        �����������źŵ����գ��������covered-1��2�������źţ���һ���źű���Ӧ������covered��λ��,�����ﱻ������. 
            ���������Ϊ����covered֮�ڵ����ź�,��covered��Сʱ,������ʵ��Ӱ��(��Ϊ������������û���������ź�,�ʴ�������Ϊ��Ч�ź�)
            �������cover�����repeat,ʹ�������ź�����,��ת�������Ϊͣ��Ĵ��ڵ����м�Ͽ��Ӷ�����źű��Ƴ�,��Ϊ����
    '''
    css_covered = repeat(css,covered)
    #print css,cls,css_covered,derepeat(band(css_covered>0,bnot(cls)))
    return derepeat(band(css_covered > 0,bnot(cls)),covered)    
    
def limit_adjust(source_signal,limit_signal,trans_signal,covered=3):#covered���ܴ���127��������, np.sign(bool array)���ص���int8����
    ''' ����ͣ���ź�limit_signal�ͽ������ź�trans_signal����ԭʼ�źţ�ʹԭʼ�źűܿ�ͣ�嵽������
        ������covered��ԭ����������ͣ�����м����ͣ���պ�,�źŶ෢. ���������makke_trade֮��ĺ��������
        ֻ��covered=2ʱ,�������������
    '''
    adjuster = fcustom(_limit_adjuster,covered=covered)
    return smooth(trans_signal,source_signal,limit_signal,sfunc=adjuster)

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
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
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
    #print 'begin adjust:',up_limit_line,down_limit_line
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
    sbuy = roll0(sbuy)
    #print 'input rolled:',sbuy,ssell
    up_limit_line = limitup2(trans[HIGH],trans[LOW])
    down_limit_line = limitdown1(trans[CLOSE])
    #print 'begin adjust:',up_limit_line,down_limit_line
    sbuy = limit_adjust(sbuy,up_limit_line,trans[VOLUME])
    ssell = limit_adjust(ssell,down_limit_line,trans[VOLUME])
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

def atr_seller(sbuy,trans,satr,times=1000,covered=20): 
    ''' kwargsĿ�����������ò���������cruiser
        timesΪ��0.001Ϊ��λ�ı���
    '''
    down_limit = tmax(trans[HIGH] - satr * times / 1000,covered)    #���n�첨�����޵����ֵ
    sdown = equals(cross(down_limit,trans[LOW]),-1)
    return band(sdown,sellconfirm(trans[OPEN],trans[CLOSE],trans[HIGH],trans[LOW]))
        
