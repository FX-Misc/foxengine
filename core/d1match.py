# -*- coding: utf-8 -*-

import numpy as np

def tmatch(signal,length=5,interval=1):
    ''' ��ȷ���ó�ʱƽ�ֵ�    
        ƽ�ֲ������źţ��ֹ�ʱ�������. signal>0Ϊ���ź�
        ���У���ʱ��֮�����µ����룬��ʱ����0����
        ���Ϊ�źź���峡�������Ϊ�����źŵڶ���(�����źŵ�������)��������������һ��Ϊ1
        length=5Ϊһ�������
    '''
    
    rev = np.zeros_like(signal)
    total = length > interval and length or interval  #����ֹ�һ��,interval=1,���ǵ���������(2,1,0)
    cur = -1
    for i in xrange(len(signal)):
        cur = total if signal[i] > 0 else cur-1
        rev[i] = 1 if cur == 0 else 0
    return rev

def make_trade_signal(target,follow):  
    ''' ����target��follow�źţ����ɽ����źţ���ȥ��ƥ����������������
        ͬʱ���������ȼ��������룬������������t+1���⡣
        �źŴ�����Ч��ƫ����Ҫ�ⲿ����
        ������follow�ź�����(tsum<=-1), ���ڴ�������ղ���,ֻ��Ҫ�������ź���Ϊtarget
        ���ؽ��ȷ���κ����������ź������Ϊ0
    '''
    len_t,len_f = len(target),len(follow)
    assert len_t == len_f
    if(len_f == 0):
        return  np.array([])
    s = np.sign(target - follow * 2) #�������������룬��������ͬʱ�����Ļ�����ȻΪ�����ź�
    tsum = 0
    for i in xrange(len_t):
        cv = s[i]
        tsum += cv
        if tsum > 1 or tsum <= -1: #��������ƥ����������е�����
            tsum -= cv
            s[i] = 0
    return s

def make_trade_signal_double_direct(target_b,target_s):
    ''' ����target��follow�źţ����ɽ����źţ���ȥ��ƥ����������������
        ͬʱ���������ȼ��������룬������������t+1���⡣
        �źŴ�����Ч��ƫ����Ҫ�ⲿ����
        ����target_b/target_s��������, ����������
        ���ؽ��ȷ���κ����������ź�����Ӳ�����2��С��-2, �����������2������, ��һ�������Ƕ�֮ǰ������ƽ��,�ڶ����ǿ�������
    '''
    len_b,len_s = len(target_b),len(target_s)
    assert len_b == len_s
    if(len_s == 0):
        return  np.array([])
    s = np.sign(target_b - target_s) #�����ź�ͬ�ȴ���,ͬʱ���������
    tsum = 0
    for i in xrange(len_b):
        cv = s[i]
        tsum += cv
        if tsum > 1 or tsum < -1: #��������ƥ������/����
            tsum -= cv
            s[i] = 0
    return s

def make_trade_signal_advanced(target,follow):  
    ''' ����target��follow�źţ����ɽ����ź�
        ͬʱ���������ȼ��������룬������������t+1���⡣
        �źŴ�����Ч��ƫ����Ҫ�ⲿ����
        ������follow�ź�����(tsum<=-1), ���ڴ�������ղ���,ֻ��Ҫ�������ź���Ϊtarget
        ���������룬��ֻ����һ������,�������������������ź�
    '''
    len_t,len_f = len(target),len(follow)
    assert len_t == len_f
    if(len_f == 0):
        return  np.array([])
    s = np.sign(target - follow * 2) #�������������룬��������ͬʱ�����Ļ�����ȻΪ�����ź�
    state = 0   #0�ղ�״̬,1�ֲ�״̬
    for i in xrange(len_t):
        cv = s[i]
        if state == 0:   #�ղ�
            if cv < 0:   #�ղֺ��������ź�
                s[i] = 0
            elif cv > 0:
                state = 1
        elif cv < 0:    #�ֲ������,��Ϊ�ղ�
            state = 0
    return s

def make_trade_signal_double_direct_free(target_b,target_s):
    ''' ����target��follow�źţ����ɽ����źţ���ȥ��ƥ����������������
        ͬʱ���������ȼ��������룬������������t+1���⡣
        �źŴ�����Ч��ƫ����Ҫ�ⲿ����
        ����target_b/target_s��������, ����������
        �����������źŲ������ơ�
    '''
    len_b,len_s = len(target_b),len(target_s)
    assert len_b == len_s
    if(len_s == 0):
        return  np.array([])
    s = np.sign(target_b - target_s) #�����ź�ͬ�ȴ���,ͬʱ���������
    return s


###################��ǰ��ʵ��,������deprecated####################
def matchshift(target,follow):  
    ''' follow���ź�ֻ����target����δƥ���ź�ʱ�ź���1λ����������
        �����������źŶ������źŵ�ƥ������ϣ����⵱������������
    '''
    assert len(target) == len(follow)
    if(len(follow) == 0):
        return  np.array([])
    rev = np.zeros_like(target)
    sstate = 0 #�ź�״̬
    for i in xrange(len(target)-1):
        ct,cf = target[i],follow[i]
        if(ct != 0 and cf == 0):
            sstate = 1
        elif(cf != 0 and (ct != 0 or sstate == 1)):
            sstate = 0
            rev[i+1] = cf
    return rev

def makematch(target,follow):
    ''' ����target�е��źţ���target���źŷ����պ�ĵ�һ��follow�źŴ�����λ�������Ķ���0. �����Ͳ���Ҫroll(1)��
        ������������target�źŵ�����follow�źţ���follow�����ź���Ȼ���ڣ�����Ӵ����ź�
        ��0Ϊ���ź�
        Note:���������ź�ǰһ�շ����������ź�(���������������),����������Ҳ����ӣ�ֻ�ǵ������֡���tradeȥ�㶨
        ���һ��follow�źŵĴ���:
            ��Ϊѭ��ֻ��length-1,�������һ��follow�ź�û�б�����
            �����������һ�֣�������һ��target���źţ������һ��follow�źŲ�����ô��������Ӱ��trade(����Ҫ��Ч��ҲҪ���ղ���ִ��trade)
                ��һ�֣����������target�źţ������follow�źŲ���λ�����Ӱ��target�ź��Ƿ�ʵʩ
            ͳһ��������м���������һ��
            ���һ�������target�źţ���follow��λ�����򲻹�
    '''
    assert len(target) == len(follow)
    if(len(follow) == 0):
        return  np.array([])
    if(len(follow) == 1):
        return np.array([0])  #��Ȼ��0����ʹfollow[0]=1����Ϊֻ�ܴ��շ���������ҲΪ[0]
    rev = np.zeros_like(target)
    sstate = 1  #�ź�״̬. ��һ������������Ҳ�������źš�����������������������
    for i in xrange(len(target)-1):
        ct,cf = target[i],follow[i]
        if(ct != 0 and cf != 0): #�����źű���������Ӵ����ź�
            rev[i+1] = rev[i] = cf
            sstate = 0
        elif(ct != 0):   #follow[i] == 0
            sstate = 1
            #rev[i] = 0  #ȡ����Ϊ����֮�����źŶ��������ź�
        elif(cf != 0 and sstate == 1):    #target[i] == 0
            #print i,sstate
            rev[i+1] = cf
            sstate = 0
    #�����ã�����Ȼ��ȷ��ʾ���һ�������ź����Ƴ����е�����
    rev[-1] = 1 if target[-1] and follow[-1] else rev[-1]  #������һ��target��follow�����źţ�������follow����������������֮ǰ���õ�(���һ��ѭ������)����Ԥ�õ�0
    return rev


