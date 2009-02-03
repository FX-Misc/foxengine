# -*- coding: utf-8 -*-
#���н���ƥ���㷨�Ĳ���

import unittest
from wolfox.fengine.core.d1match import *

class ModuleTest(unittest.TestCase):
    def test_tmatch(self):
        signal = np.array([0,0,5,0,0,0,0,0,0,0,1,0,0,3,0,0,-1,0,0,0,0,3,0,0,0])
        self.assertEquals([0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 0,0,1,0,0,0,0,0,0],tmatch(signal,5).tolist())
        self.assertEquals([0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0, 0,1,0,0,0,0,0,0,0],tmatch(signal,4).tolist())
        self.assertEquals([0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0, 0,0,0,0,0,0,1,0,0],tmatch(signal,0).tolist())
        self.assertEquals([0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0, 0,0,1,0,0,0,0,0,0],tmatch(signal,5,3).tolist())

    def test_make_trade_signal(self):
        self.assertEquals([],make_trade_signal(np.array([]),np.array([])).tolist())
        self.assertEquals([0,0,0,1,-1,0],make_trade_signal(np.array([0,1,0,1,0,0]),np.array([0,1,0,0,1,0])).tolist())
        self.assertEquals([0,1,-1,0,0],make_trade_signal(np.array([0,1,0,1,0]),np.array([1,0,1,1,0])).tolist())

    def test_make_trade_signal_double_direct(self):
        self.assertEquals([],make_trade_signal_double_direct(np.array([]),np.array([])).tolist())
        self.assertEquals([0,0,0,1,-1,0],make_trade_signal_double_direct(np.array([0,1,0,1,0,0]),np.array([0,1,0,0,1,0])).tolist())
        self.assertEquals([-1,1,-1,0,0],make_trade_signal_double_direct(np.array([0,1,0,1,0]),np.array([1,0,1,1,0])).tolist())

    def test_matchshift(self):
        self.assertEquals([],matchshift(np.array([]),np.array([])).tolist())
        self.assertEquals([0,0,1,0,0,1],matchshift(np.array([0,1,0,1,0,0]),np.array([0,1,0,0,1,0])).tolist())
        self.assertEquals([0,0,0,1,1],matchshift(np.array([0,1,0,1,0]),np.array([1,0,1,1,0])).tolist())

    def test_makematch(self):
        #����С��1�����
        self.assertEquals([],makematch(np.array([]),np.array([])).tolist())
        #����=1�����
        self.assertEquals([0],makematch(np.array([1]),np.array([1])).tolist())
        self.assertEquals([0],makematch(np.array([1]),np.array([0])).tolist())
        self.assertEquals([0],makematch(np.array([0]),np.array([1])).tolist())
        self.assertEquals([0],makematch(np.array([0]),np.array([0])).tolist())
        target = np.array([1,0,0,1,0,1,-1,1,0,0])
        target2 = np.array([-1,0,0,1,0,1,0,0,0,1])
        self.assertEquals([1,1,0,0,0,1,1,1,0,1],makematch(target,np.array([1,0,0,0,1,0,1,0,1,1])).tolist())
        self.assertEquals([1,1,0,0,0,1,0,1,0,1],makematch(target2,np.array([1,1,0,0,1,0,1,0,1,1])).tolist())
        #����ʵ������г��ֵ�����, �������е������������ڽ�����ȶ�����
        target_r1 = np.array([0,1,1,1,1,1,1])
        target_r2 = np.array([0,1,1,1,1,1,1,1,0])
        self.assertEquals([0,1,1,1,1,1,1],makematch(target_r1,np.array([1,1,0,1,1,0,1])).tolist()) #�޸�
        self.assertEquals([0,1,1,1,1,1,1,1,1],makematch(target_r2,np.array([1,1,0,1,1,0,1,1,1])).tolist())
        #�������֮��
        self.assertEquals([0,1,1,1,1,1,1,1,1],makematch(target_r2,np.array([1,1,0,1,1,0,1,1,0])).tolist())
        #???
        self.assertEquals([0,0,1,0,0,1],makematch([1,0,0,1,0,0],np.array([0,1,1,0,1,0])).tolist())
        self.assertEquals([0,0,0,0,1,0],makematch([0,1,0,0,1,0],np.array([0,0,0,1,0,0])).tolist())

if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    unittest.main()
