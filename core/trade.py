# -*- coding: utf-8 -*-

#�뽻�׺�������صĺ���

import numpy as np
from wolfox.fengine.base.common import Trade,Evaluation
from wolfox.fengine.core.base import BaseObject

import logging
logger = logging.getLogger('wolfox.fengine.core.trade')

VOLUME_BASE = 1000

def buy_first(signal):  #ȷ���Ƿ�ǰ��һ���Էϳ���һ�������ź�
    return 1 if signal < 0 else 0

def sell_first(signal):  #ȷ���Ƿ�ǰ��һ���Էϳ���һ�������ź�
    return 1 if signal > 0 else 0

def double_first(signal):  #˫��
    return 0

def make_trades(tstock,signal,tdate,tpositive,tnegative,begin=0,taxrate=125,trade_strategy=buy_first):
    ''' tstockΪstock_code
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
        cs = signal[ci]
        price = tpositive[ci] if cs>0 else tnegative[ci]
        trades.append(Trade(tstock,tdate[ci],price,cs*VOLUME_BASE,taxrate))        
    if sum(signal[tbegin:]) != 0: #���һ��δƽ��,������
        #print sum(signal[tbegin:]),signal[tbegin:].tolist()
        trades.pop()
    return trades

def last_trade(tstock,signal,tdate,tpositive,tnegative,begin=0,taxrate=125):
    ''' ����ֵΪ[x]��ʽ(��ʱΪ[])
    '''
    assert len(tpositive) == len(tnegative) == len(signal)
    sis = signal.nonzero()[0]  #��0�źŵ�index
    tbegin = tdate.searchsorted(begin)
    ibegin = sis.searchsorted(tbegin)   #tbegin�ڷ�0�����еĲ���λ��
    slen = len(sis)
    if slen == 0 or sum(signal[tbegin:]) == 0 or tdate[sis[-1]] < begin: #���ź�����(ʵ����Ҳ��sum(signal)==0)���Ѿ�ƥ�䣬������֮����/����
        return []
    last_index = sis[-1]
    cs = signal[last_index]
    price = tpositive[last_index] if cs > 0 else tnegative[last_index]
    trades= [Trade(tstock,tdate[last_index],price,cs*VOLUME_BASE,taxrate)]
    return trades

def match_trades(trades):
    ''' �Խ��׽���ƥ��
        һ�ν��׿����������������Ե�����Ʊ��������Ϊ0Ϊ������ɱ�־
        ����ֵmatched_trades�б��е�Ԫ����ʽΪ��
            trade1,trade2,....,traden
            ����    ����trade��volume֮��Ϊ0�������κ�ǰm��trade��volume֮�Ͳ�Ϊ0(�������Ȳ���Ϊ����0)
            ���matcher����ֻ��trade1,trade2�����ɷ֣����Ҫһ�������������ģ���Ҫ��һ��matcher
            ����Ҫ����Ӧ���µ�make_trades��������Ӧ
    '''
    matched_trades = []
    contexts = {}
    for trade in trades:
        if(trade.tstock in contexts):
            sum,items = contexts[trade.tstock]
            items.append(trade)
            sum += trade.tvolume
            if(sum == 0):#�������
                del contexts[trade.tstock] #�Դ�����һ�ε�else (�������ΪNone���һ�κ�ÿ���½��׵��жϲ�ͬ)
                matched_trades.append(items) 
            else:
                contexts[trade.tstock] = (sum,items)
        else:
            contexts[trade.tstock] = (trade.tvolume,[trade])
    #print matched_trades
    #for matched_trade in matched_trades:logger.debug('matched trade:%s,%s',matched_trade[0],matched_trade[1])
    return matched_trades

def evaluate(trades,matcher=match_trades):
    ''' �Խ��׽���ƥ�������
    '''
    return Evaluation(matcher(trades))

import operator
def DEFAULT_EVALUATE_FILTER(matched_named_trades):
    ''' ������Ԫ�����µ��б�
            parent: BaseObject
            trades:[[trade1,trade2,...],[trade3,trade4,...],....] �պϽ����б�
        ���ز��ɵıպϽ��׵ĺϲ��б�
            [[trade1,trade2,...],[trade3,trade4,...],....]
    '''
    tradess = [ mnt.trades for mnt in matched_named_trades if mnt.trades]   #����[[trades,trades...],[trades,trades,...]...]
    return reduce(operator.add,tradess)

def gevaluate(named_trades,filter=DEFAULT_EVALUATE_FILTER,matcher=match_trades):
    ''' �Զ����Դ��Ľ��׽���ƥ�䡢ͷ������������һ�ν��׿����������������Ե�����Ʊ��������Ϊ0Ϊ������ɱ�־
        named_tradesΪBaseObject�б�ÿ��BaseObject����name,evaluation,trades��������
            evalutaion���ڶ�trades�еĽ��׽��з��պ���������
        filterΪ���Ѿ�ƥ��ɹ��Ľ��׽���ͷ�����
        matched_named_trades�б��е�Ԫ��ΪBaseObject�������԰�����
            parent:ָ��������named_trade(Ҳ��BaseObject)
            trades:[[trade1,trade2,...],[trade3,trade4,...],....]
            ����    ����trade��volume֮��Ϊ0�������κ�ǰm��trade��volume֮�Ͳ�Ϊ0(�������Ȳ���Ϊ����0)
            ���evaluate����ֻ��trade1,trade2�����ɷ֣����Ҫһ�������������ģ���Ҫ��һ��evaluate
            ����Ҫ����Ӧ���µ�make_trades����
    '''
    matched_named_trades = []
    for nt in named_trades:
        matched_named_trades.append(BaseObject(parent=nt,trades=matcher(nt.trades)))
    matched_trades = filter(matched_named_trades)   #ת����[trades,trades,...]��ʽ
    for matched_trade in matched_trades:
        #print 'matched trade:%s,%s',matched_trade[0],matched_trade[1]
        logger.debug('matched trade:%s,%s',matched_trade[0],matched_trade[1])
    return Evaluation(matched_trades)
