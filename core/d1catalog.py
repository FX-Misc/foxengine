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

#@wcache
def calc_index(stocks,sector=CLOSE,weight=AMOUNT,wave = 10,alen=10):
    ''' ����catalogָ�������ظ�ָ������س�Ա�����У��Ե�һ��Ϊ����
        stocksΪ����Աstock��d2array����ļ���
        ����d1��ָ�����к�d2array��ÿ�հٷ�����(array��ͬ�����stocks��)
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
    scores[zero_pos] = sma[zero_pos]
    #print zero_pos
    #print scores
    s_weights = scores * RFACTOR / scores.sum(0)
    waves = cmp_percent(sectors) / 1.0 / PERCENT_BASE
    index = (waves * s_weights).sum(0)* INDEX_BASE + 0.5    #�Ա��²�ȡ��ʱ��������
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


