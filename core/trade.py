# -*- coding: utf-8 -*-

#�뽻�׺�������صĺ���

import numpy as np
from wolfox.common.tcommon import Trade,Evaluation

VOLUMEBASE = 1000

def make_trades(tstock,signal,tdate,tpositive,tnegative,begin=0,taxrate=125):
    ''' tstockΪstock_id
        ssingalΪ�����ź�,���ڴ����������źţ�����ǰ��Ҫ��signal roll(1)
        tpositive,tnegativeΪ�ź�ֵΪ���͸�ʱ��ѡ��۸�
        taxrateΪ˰�ʣ�Ĭ��Ϊǧ��֮��
        beginΪ��ʼ������
    '''
    assert len(tpositive) == len(tnegative) == len(signal)
    sis = signal.nonzero()[0]  #��0�źŵ�index    
    tbegin = tdate.searchsorted(begin)
    ibegin = sis.searchsorted(tbegin)   #tbegin�ڷ�0�����еĲ���λ��
    #print tbegin,ibegin
    slen = len(sis)
    if slen == 0 or ibegin == slen: #���ź�
        return []
    trades = []
    for i in xrange(ibegin,slen):
        ci = sis[i]
        cs = signal[ci]
        price = tpositive[ci] if cs>0 else tnegative[ci]
        trades.append(Trade(tstock,tdate[ci],price,cs*VOLUMEBASE,taxrate))        
    if sum(signal[tbegin:]) != 0: #���һ��δƽ��,������
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
    trades= [Trade(tstock,tdate[last_index],price,cs*VOLUMEBASE,taxrate)]
    return trades

def evaluate(trades):#һ�ν��׿����������������Ե�����Ʊ����Ϊ0Ϊ������ɱ�־
    matchedtrades = []
    contexts = {}
    for trade in trades:
        if(trade.tstock in contexts):
            sum,items = contexts[trade.tstock]
            items.append(trade)
            sum += trade.tvolume
            if(sum == 0):#�������
                del contexts[trade.tstock] #�Դ�����һ�ε�else (�������ΪNone���һ�κ�ÿ���½��׵��жϲ�ͬ)
                matchedtrades.append(items) 
            else:
                contexts[trade.tstock] = (sum,items)
        else:
            contexts[trade.tstock] = (trade.tvolume,[trade])
    #print '�������',matchedtrades,wincount,winamount,lostcount,lostamount
    return Evaluation(matchedtrades)

