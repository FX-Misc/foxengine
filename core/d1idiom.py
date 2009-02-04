# -*- coding: utf-8 -*-

"""
���õ��㷨�����
�����ֻ�����Ƿ��ܹ�ִ�У����������߼�
"""

import numpy as np

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
    return np.logical_and(sconfirm,np.logical_not(threeupextend))

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
    return np.logical_not(bm_and_pos)

def simplesell(sbuy,shigh,slow,threshold):
    downl = downlimit(shigh,sbuy,threshold)
    return slow - downl < 0

def tsimplesell(sbuy,shigh,slow,threshold):
    downl = tdownlimit(shigh,sbuy,threshold)
    return slow - downl < 0

def confirmedsell(sbuy,sopen,sclose,shigh,slow,ssignal,threshold):  #ssignalΪ�����������޵������ߣ�һ��Ϊsclose��slow
    downl = downlimit(shigh,sbuy,threshold)
    return np.sign(np.logical_and(ssignal-downl <0,sellconfirm(sopen,sclose,shigh,slow)))   #����intֵ���ڲμ������ת��

def confirmedselll(sbuy,sopen,sclose,shigh,slow,threshold): #��slowΪ��������
    downl = downlimit(shigh,sbuy,threshold)
    return np.sign(np.logical_and(slow-downl <0,sellconfirm(sopen,sclose,shigh,slow)))   #����intֵ���ڲμ������ת��

def confirmedsellc(sbuy,sopen,sclose,shigh,slow,threshold): #��scloseΪ��������
    downl = downlimit(shigh,sbuy,threshold)
    return np.sign(np.logical_and(sclose-downl <0,sellconfirm(sopen,sclose,shigh,slow))) #����intֵ���ڲμ������ת��

def downup(source1,source2,belowdays,crossdays=3):
    ''' �ж�source2����source1֮�ϣ�Ȼ��crossdays����(Ϊ�����غϣ�Ĭ��Ϊ3)���£�ͣ��n�����
    '''
    s2_1 = source2 - source1
    s2_lt_1 = s2_1 < 0 #tfilter_lt(s2_1)
    s2_gt_1 = s2_1 > 0 # tfilter_gt(s2_1)
    sdown = sfollow(s2_gt_1,s2_lt_1,crossdays)
    sdown_up = sfollow(sdown,s2_gt_1,belowdays)  #belowdays֮�ڻ�ȥ
    return sdown_up

