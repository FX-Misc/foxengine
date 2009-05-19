# -*- coding: utf-8 -*-


"""
���catalog���������⣬�Լ�����װ��
"""

import numpy as np

from wolfox.fengine.core.d1 import *
from wolfox.fengine.core.d2 import *
from wolfox.fengine.core.source import *

RFACTOR = 1.0   #ʵ��ת������
INDEX_BASE = 1000

def calc_index_relative(stocks,sector=CLOSE,weight=AMOUNT,wave = 10):
    ''' ����catalogָ�������ظ�ָ������س�Ա������
        ����ÿ�յ��������㣬�Ա��ֳ�ʼ���ڵ�����ȶ���
        stocksΪ����Աstock��d2array����ļ���
        ����d1��ָ�����к�
        ��Ȩ�ؽ��б�׼��,�������Ϊ1-wave��wave����,ͣ�Ƹ��ɳɽ�Ȩ��Ϊnma(alen)
        ����㷨��Ϊ���������½�����(����Ȩ�ر仯)�������ڰ������ײ����ƹ����У�ָ�������ڸ���ƽ��
        Ҳ����˵������㷨���߱��۸��ȶ���
        ��һ��ָ����������Ʊ��ɣ���۸�
        A: 1000-->2000-->1000
        B: 1000-->1000-->1000
        ��������гɽ��������
        ���һ��ָ��Ϊ1000���������(ԭ����)���ڶ���ָ��Ϊ (2*0.5+1*0.5)*1000 = 1500
          ������ָ��Ϊ (0.5*0.5 + 1*0.5) * 1500 = 1125
          Ҳ����˵��ȥһ�ˣ�������ͬһλ��ʱָ��ȴ�仯�ˡ�
          ��Ȼ��һ������ɽ������أ�ָ���仯�Ǳ�Ȼ�ģ������ɽ�����ƽ��ʱ��ָ�������仯
          ����������Ǻ�������
        ͨ�����½��ν��м�Ȩ,�����˼۸񲨶��ȶ���. ����1.25�Ǿ�������
    '''
    csize = len(stocks)
    sectors = extract_collect(stocks,sector)
    weights = extract_collect(stocks,weight)
    #print weights
    scores = percent_sort(weights) / (PERCENT_BASE/wave) + 1 #0����Ϊ1��, ������ʱ������ʧ��
    #����ͣ�ƹɽ���ƽ������,��Ϊ�˼����ʼ��������, �����ʼ��ͣ�Ƶĸ��ɻᵼ��ָ������������ͬ
    waves = npercent(sectors) * RFACTOR / PERCENT_BASE
    scores = np.where(waves<1.0,scores * 1.25 ,scores)   #���½��ν��м�Ȩ
    s_weights = scores * RFACTOR / scores.sum(0)
    #print s_weights
    #waves = np.where(ori_waves<1.0,ori_waves*(csize-3)/(csize+3),ori_waves) #���µ���Ȩ
    rindex = (waves * s_weights).sum(0) #�����������������Ȩ������
    index = rindex.cumprod() * INDEX_BASE + 0.5
    return np.cast['int'](index)

calc_index = calc_index_relative    #ȡ����ȶ��ԣ���������һ���ԡ���Ϊcatalog_index���ô���Ҫ�ڴ�

def calc_index_old(stocks,sector=CLOSE,weight=AMOUNT,wave = 10,alen=10):
    ''' ����catalogָ�������ظ�ָ������س�Ա�����У��Ե�һ��Ϊ����
        ��Ϊ��ʼ���ڵĲ�ͬ��������ָ�����߱�����ȶ��ԣ���ͬ��ʼ�ռ��������ָ����������֮�����Ա������ȶ�
        stocksΪ����Աstock��d2array����ļ���
        ����d1��ָ������    #��d2array��ÿ�հٷ�����(array��ͬ�����stocks��)
        ��Ȩ�ؽ��б�׼��,�������Ϊ1-wave��wave����,ͣ�Ƹ��ɳɽ�Ȩ��Ϊnma(alen)
    '''
    sectors = extract_collect(stocks,sector)
    weights = extract_collect(stocks,weight)
    #print weights
    scores = percent_sort(weights) / (PERCENT_BASE/wave) + 1 #0����Ϊ1��
    sma = nma2(scores,alen)
    #print sma
    #print scores
    zero_pos = np.where(weights == 0)
    scores[zero_pos] = sma[zero_pos]    #ͣ�Ƹ���
    #print zero_pos
    #print scores
    s_weights = scores * RFACTOR / scores.sum(0)
    waves = cmp_percent(sectors) / 1.0 / PERCENT_BASE
    index = (waves * s_weights).sum(0)* INDEX_BASE + 0.5    #�Ա��²�ȡ��ʱ��������
    return np.cast['int'](index)

def calc_index1(stocks,sector=CLOSE,weight=AMOUNT,wave = 10,alen=10):
    ''' ����catalogָ�������ظ�ָ������س�Ա�����У���һԪΪ��׼,�Դ�ʵ������ȶ���
        stocksΪ����Աstock��d2array����ļ���
        ����d1��ָ������    #��d2array��ÿ�հٷ�����(array��ͬ�����stocks��)
        ��Ȩ�ؽ��б�׼��,�������Ϊ1-wave��wave����,ͣ�Ƹ��ɳɽ�Ȩ��Ϊnma(alen)
        ������ܵ���Ȩ���ص�Ӱ��, ��Ϊ�޷��Ի�׼��Ȩ,���³�Ȩ�����̼ۼ���,�Ӷ����ڿ��ظ��ȶ����ϵ�ȱ��.
            ������֮�����¼���ʱ,���������ͬ
    '''
    sectors = extract_collect(stocks,sector)
    weights = extract_collect(stocks,weight)
    #print weights
    scores = percent_sort(weights) / (PERCENT_BASE/wave) + 1 #0����Ϊ1��
    sma = nma2(scores,alen)
    #print sma
    #print scores
    zero_pos = np.where(weights == 0)
    scores[zero_pos] = sma[zero_pos]    #ͣ�Ƹ���
    #print zero_pos
    #print scores
    s_weights = scores * RFACTOR / scores.sum(0)
    waves = sectors
    index = (waves * s_weights).sum(0) + 0.5    #�Ա��²�ȡ��ʱ��������
    return np.cast['int'](index)


#@wcache
def calc_drate(stocks,distance=1,sector=CLOSE,wave=100):
    ''' ����sector��distance��������˳λ
        �û���wave�ļ����ʾ
    '''
    sectors = extract_collect(stocks,sector)
    #print sectors
    scores = npercent(sectors,distance)
    #print percent_sort(scores)
    rate = percent_sort(scores) / (PERCENT_BASE/wave)   #0��
    return rate

#@wcache
def avg_price(stocks):
    ''' ����stocks��ƽ���۸񣬻�����ʱ�ɺ��Ը���������ͣ�����
    '''
    amount = extract_collect(stocks,AMOUNT) * 1.0   #�������
    volume = extract_collect(stocks,VOLUME)
    sa = amount.sum(0)  #��λΪ��Ԫ
    sv = volume.sum(0)  #��λΪ��
    return np.cast['int'](sa / sv *100) #��λΪ��

def catalog_signal(cata_info,cata_threshold=8000,stock_threshold=8000):
    ''' �鿴cata_info���Ƿ����catalog����>cata_threshold,stock�ڸ�catalog�е�����>stock_threshold���ź�
        cata_info:  {catalog ==> stock_order_in_catalog}
        cata_threshold: ��catalog��gorder��Ҫ����ֵ
        stock_threshold: ��stock�ڸ�catalog�е������Ҫ����ֵ����stock_order_in_catalog
        ��catalog_signal_together������汾
    '''
    return gor(*[band(k.gorder >= cata_threshold,v >= stock_threshold) for k,v in cata_info.items()])

def catalog_signal_cs(cata_info,extractor):
    ''' �鿴cata_info���Ƿ����catalog����extractor���ź�
        cata_info:  {catalog ==> stock_order_in_catalog}
        extractor: catalog,stock ==> signal���еĺ������� lambda c,s:band(c.g60 > 5000,s.g60>5000)
    '''
    return gor(*[extractor(c,s) for c,s in cata_info.items()])

def catalog_signal_c(cata_info,extractor):
    ''' �鿴cata_info���Ƿ����catalog����extractor���ź�
        cata_info:  {catalog ==> stock_order_in_catalog}
        extractor: catalog ==> signal���еĺ������� lambda c:c.g60 > 5000
    '''
    return gor(*[extractor(c) for c in cata_info.keys()])

def catalog_signal_m(func,*catalogs):
    ''' ��catalogs�еĸ���catalog������˳�����n��valueȡ��������Ϊfunc�Ĳ������㣬���or��Щ���
        ��gor(func(catalog1.values()[0],catalog2.values()[0],...),...,func(catalog1.values()[-1],catalog2.values()[-1]...))
        ��Ҫ���ڲ�ͬ���ڵ�catalog֮��ıȽ�,��c20,c60,c120�ĵ�һ�����ıȽ�
        ���������ڲ�ͬdict֮��ͬ����keys(������һ��)��������һ����. 
            �����ֹ����ԣ����ò������ȷ�ġ�����������Ҳ����ˣ�key��˳��Ӧ�����ȶ���(�����ڲ���˳��һ��ʱ)
    '''
    vvs = [ c.values() for c in catalogs ]
    pairs = zip(*vvs)
    return gor(*[func(*pair) for pair in pairs])

#deprecated
def calc_index_adjacent(stocks,sector=CLOSE):
    ''' �ڽӷ�����catalogָ�������ظ�ָ������س�Ա������
        stocksΪ����Աstock��d2array����ļ���
        ����d1��ָ�����к�d2array��ÿ�հٷ�����(array��ͬ�����stocks��)
        ���ּ��㲻�߱��ȶ��ԣ�ͬ���ļ۸�/�ɽ����ڲ�ͬ�����ӵ��µ�ָ���ǲ�ͬ��
        ��
            a = np.array([(0,0,0,0),(500,400,800,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,1000,1000,1000)])
            b = np.array([(0,0,0,0),(200,200,200,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,2000,1000)])
            c = np.array([(0,0,0,0),(700,700,300,400),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(1000,0,1000,1000)])
            qa = CommonObject(id=3,transaction=np.array([a,b,c]))
            ��qa[:,2]�����qa[:,1]��λ�ã����ߵ�ָ���ǲ�һ���ģ��ֱ���885��1007
    '''
    sectors = extract_collect(stocks,sector)
    volumes = extract_collect(stocks,VOLUME)
    weights = volumes * RFACTOR / volumes.sum(0)
    #ָ���ļ�����ʹ���ڽ��������⴦���¹ɺ�ͣ�Ƶ������⡣
    #�����¹ɣ���һ����Ϊ�۸񲻱����Ϊ�ȶ����أ��ɽ����ϴ󣩡���ͣ����������Ϊ�ɽ�Ϊ0Ȩ��Ϊ0������һ������������ȷ�����˼۸��
    #��Ϊ�¹�֮ǰ�ļ۸��ǵ�һ��۸񣬵��ɽ�Ϊ0����ͣ���յļ۸�Ϊǰһ�����ռ۸񣬳ɽ�ҲΪ0
    #�Գɽ���ΪȨ���ܹ���Ϊ���Ľ���������
    diffs = (increase(sectors) * (RFACTOR / PERCENT_BASE))
    diffs += 1  #ÿ�춼��ǰ�յ�������
    #index = (diffs.cumprod(1) * weights).sum(0)* INDEX_BASE    #��ͬ��calc_index_base_0 
    #print diffs * weights
    index = (diffs * weights).sum(0).cumprod() * INDEX_BASE + 0.5   #�Ա��²�ȡ��ʱ��������
    return np.cast['int'](index)

#deprecated
def calc_index_base0_old(stocks,sector=CLOSE):
    ''' ����catalogָ�������ظ�ָ������س�Ա�����У��Ե�һ��Ϊ����
        stocksΪ����Աstock��d2array����ļ���
        ����d1��ָ�����к�d2array��ÿ�հٷ�����(array��ͬ�����stocks��)
        �������ȶ��ģ������ĳ���ۼƾ޷��ǵ����ҳɽ���������Ĺ�Ʊĳ��ͣ�ƣ���ᵼ��ָ���ڸ���ǰ������쳣����
    '''
    sectors = extract_collect(stocks,sector)
    volumes = extract_collect(stocks,VOLUME)
    weights = volumes * RFACTOR / volumes.sum(0)
    #ָ���ļ�����ʹ���ڽ��������⴦���¹ɺ�ͣ�Ƶ������⡣
    #�����¹ɣ���һ����Ϊ�۸񲻱����Ϊ�ȶ����أ��ɽ����ϴ󣩡���ͣ����������Ϊ�ɽ�Ϊ0Ȩ��Ϊ0������һ������������ȷ�����˼۸��
    #��Ϊ�¹�֮ǰ�ļ۸��ǵ�һ��۸񣬵��ɽ�Ϊ0����ͣ���յļ۸�Ϊǰһ�����ռ۸񣬳ɽ�ҲΪ0
    #�Գɽ���ΪȨ���ܹ���Ϊ���Ľ���������
    diffs = (increase(sectors) * (RFACTOR / PERCENT_BASE))
    diffs += 1  #ÿ�춼��ǰ�յ�������
    index = (diffs.cumprod(1) * weights).sum(0)* INDEX_BASE + 0.5    #��ͬ��calc_index_base_0 
    return np.cast['int'](index)

#deprecated
def calc_index_base0(stocks,sector=CLOSE):
    ''' ����catalogָ�������ظ�ָ������س�Ա�����У����Ե�һ��Ϊ����
        stocksΪ����Աstock��d2array����ļ���
        ����d1��ָ�����к�d2array��ÿ�հٷ�����(array��ͬ�����stocks��)
        �������ȶ��ģ������ĳ���ۼƾ޷��ǵ����ҳɽ���������Ĺ�Ʊĳ��ͣ�ƣ���ᵼ��ָ���ڸ���ǰ������쳣����        
    '''
    sectors = extract_collect(stocks,sector)
    volumes = extract_collect(stocks,VOLUME)
    weights = volumes * RFACTOR / volumes.sum(0)
    #ָ���ļ�����ʹ���ۼƷ���Ҳ�ܱ��⴦���¹ɺ�ͣ�Ƶ������⡣
    #ÿ��ָ������ͬ�ڵ��ս��׵ĸ����Խ�����ΪȨ�ļ۸��������ʼ�۸�ı���
    waves = cmp_percent(sectors) / 1.0 / PERCENT_BASE
    index = (waves * weights).sum(0)* INDEX_BASE + 0.5  #�Ա��²�ȡ��ʱ��������
    return np.cast['int'](index)


