# -*- coding: utf-8 -*-

#�뽻����صĺ���

import numpy as np
from wolfox.fengine.base.common import Trade,Evaluation
from wolfox.fengine.core.base import BaseObject
from wolfox.fengine.core.utils import fcustom

import logging
logger = logging.getLogger('wolfox.fengine.core.trade')

VOLUME_BASE = 1000

def buy_first(signal):  #ȷ���Ƿ�ǰ��һ���Էϳ���һ�������ź�
    return 1 if signal < 0 else 0

def sell_first(signal):  #ȷ���Ƿ�ǰ��һ���Էϳ���һ�������ź�
    return 1 if signal > 0 else 0

def double_first(signal):  #˫��
    return 0

def default_extra(trade,stock,index):   #�����κ�����
    return trade

def atr_extra_custom(trade,stock,index):   #��atrֵ����trade��ר�Ŷ��ƣ��Ѿ��ں��汻һ�㷽������
    trade.atr = int(stock.atr[index])   #��atrת��Ϊƽ����int���ͣ�����numpy.int32���Ա��������
    return trade

def append_attribute_extra(trade,stock,index,attr_name_from,attr_name_to=None):
    if attr_name_from in stock.__dict__:
        if not attr_name_to:
            attr_name_to = attr_name_from
        trade.__dict__[attr_name_to] = int(stock.__dict__[attr_name_from][index]) #��atrת��Ϊƽ����int���ͣ�����numpy.int32���Ա��������
    else:
        logger.warn('append attribute error:%s do not have attribute %s',stock.code,attr_name_from)
    return trade

atr_extra = fcustom(append_attribute_extra,attr_name_from='atr')    #atr_extra��һ�㶨�巽��

def make_trades(stock,signal,tdate,tpositive,tnegative
        ,begin=0,taxrate=125,trade_strategy=buy_first,extra_func=default_extra):
    ''' stockΪstock
        ssingalΪ�����ź�,���ڴ����������źţ�����ǰ��Ҫ��signal roll(1)
        tpositive,tnegativeΪ�ź�ֵΪ���͸�ʱ��ѡ��۸�
        taxrateΪ˰�ʣ�Ĭ��Ϊǧ��֮��
        beginΪ��ʼ������
        trade_strategyΪ���׷�ʽ������������������򣬻��Ǿ���
        �����뿪ʼ����
    '''
    assert len(tpositive) == len(tnegative) == len(signal)
    sis = signal.nonzero()[0]  #��0�źŵ�index    
    slen = len(sis)    
    if slen == 0:
        return []
    tbegin = tdate.searchsorted(begin)
    ibegin = sis.searchsorted(tbegin)   #tbegin�ڷ�0�����еĲ���λ��
    #print tbegin,ibegin
    if ibegin >= slen: #���ź�
        return []
    should_skip = trade_strategy(signal[sis[ibegin]])
    ibegin += should_skip
    if ibegin >= slen: #��Ȼ�ǿ��ź�
        return []
    #print signal[tbegin:].tolist(),sis,ibegin,tbegin
    tbegin = sis[ibegin]
    trades = []
    for i in xrange(ibegin,slen):
        ci = sis[i]
        cs = signal[ci]     #ͨ����1/-1,ֻ����/�������壬��ֵ����������
        price = tpositive[ci] if cs>0 else tnegative[ci]
        ctrade = Trade(stock.code,int(tdate[ci]),int(price),int(cs)*VOLUME_BASE,taxrate) #intǿ��ת���������numpy.int32����trade.��Ϊndarray�����õ���ֵ��numpy.intxx�ģ�������ͨint
        trades.append(extra_func(ctrade,stock,ci))
    if sum(signal[tbegin:]) != 0: #���һ��δƽ��,������
        #print sum(signal[tbegin:]),signal[tbegin:].tolist()
        trades.pop()
    return trades

def last_trade(stock,signal,tdate,tpositive,tnegative
        ,begin=0,taxrate=125,trade_strategy=buy_first,extra_func=default_extra): #trade_strategy��Ȼû�ã�Ҳ��д��
    ''' ����ֵΪ[x]��ʽ(��ʱΪ[])
    '''
    assert len(tpositive) == len(tnegative) == len(signal)
    #for t,s in zip(tdate,signal):print t,s
    sis = signal.nonzero()[0]  #��0�źŵ�index
    tbegin = tdate.searchsorted(begin)
    ibegin = sis.searchsorted(tbegin)   #tbegin�ڷ�0�����еĲ���λ��
    slen = len(sis)
    #print tbegin,ibegin,slen
    #if slen == 0 or sum(signal[tbegin:]) == 0 or tdate[sis[-1]] < begin: #���ź�����(ʵ����Ҳ��sum(signal)==0)���Ѿ�ƥ�䣬������֮����/����
    #    return []
    if slen == 0 or tdate[sis[-1]] < begin: #���ź�����,ƥ�������ҲҪ��ʾ    
        return []
    #print signal
    last_index = sis[-1]
    cs = signal[last_index]
    price = tpositive[last_index] if cs > 0 else tnegative[last_index]
    ltrade = Trade(stock.code,int(tdate[last_index]),int(price),int(cs)*VOLUME_BASE,taxrate)
    trades= [extra_func(ltrade,stock,last_index)]
    return trades

def match_trades(trades):
    ''' �Խ��׽���ƥ��
        һ�ν��׿���������������(�����)����ֲ����֣�������һ��ƽ��
        ����ֵmatched_trades�б��е�Ԫ����ʽΪ��
            [trade1,trade2,....,traden]
            ����    ����trade��volume֮��Ϊ0�������κ�ǰm��trade��volume֮�Ͳ�Ϊ0(�������Ȳ���Ϊ����0)
        ���ﲻ�����ս������ƣ��������պ��������յĶ���������d1match.make_trade_signal.xxxx
        ���������������ֿ����ж�Σ�ƽ�ֶ�ֻ��һ��
    '''
    matched_trades = []
    contexts = {}
    #state: 1�ֶ�֣�0�ղ֣�-1������
    for trade in trades:
        if(trade.tstock in contexts):
            tsum,items = contexts[trade.tstock]
            #print trade,tsum
            items.append(trade)
            if (tsum > 0 and trade.tvolume < 0) or (tsum < 0 and trade.tvolume > 0):   #�����λ����ƽ��
                #print 'trade finish,date=%s' % trade.tdate,'items:',items[0]
                del contexts[trade.tstock] #�Դ�����һ�ε�else (�������ΪNone���һ�κ�ÿ���½��׵��жϲ�ͬ)
                trade.tvolume = -tsum   #ƽ��ֻ��һ��
                matched_trades.append(items) 
            else:   #ͬ��
                tsum += trade.tvolume
                contexts[trade.tstock] = (tsum,items)
        else:
            contexts[trade.tstock] = (trade.tvolume,[trade])
    #print matched_trades
    #for matched_trade in matched_trades:logger.debug('matched trade:%s,%s',matched_trade[0],matched_trade[1])
    return matched_trades


