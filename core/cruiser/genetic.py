# -*- coding: utf-8 -*-

"""
�����Ŵ��㷨:
"""

import random
from math import log
import logging
from wolfox.common.tutils import linelog
import wolfox.core.cruiser.genetichelper as helper

logger = logging.getLogger('wolfox.fengine.core.cruiser.genetic')

class Nature(object):
    __slots__ = 'judge','fitness_ranker','selector','reproducer','crossover_rate','mutation_rate','goal','generation','judgecache'
    #Ŀ��ֵ���(����Ѱ��Ŀ��ֵ����Ը��壬Ҫ��Ϊ�Ǹ���)����Ӧ������(������,���Ⱥ�壬������)
    #ѡ����(���ո��ʷֲ�,�����̶ĵ�)�����ݸ��������Ӵ�(�����������)
    #��ֹĿ�ꡢ��ǰ����

    def __init__(self,judge,fitness_ranker,selector,reproducer,goal = 99.0):
        self.judge = judge
        self.fitness_ranker = fitness_ranker
        self.selector = selector
        self.reproducer = reproducer
        self.generation = 0
        self.judge = judge
        self.judgecache = {}
        self.goal = goal * 1.0  #ת��Ϊ������
        
    def run(self,population, n):
        ''' ��populationΪ��ʼ��Ⱥ������n�����ߴﵽgoal
            �������յ�population�͵�������
        '''
        assert n > 0
        for i in range(n):
            #print 'begin loop %s' % i
            logger.debug('begin loop %s' % i)
            self.generation = i
            scores = [ self.cached_judge(cell) for cell in population]  #ÿ����Ŀ��ֵ���
            if(max(scores) >= self.goal):
                #linelog('��������Ҫ��Ľⷨ��������ֹ�ڵ�%s��' % i)
                logger.debug('��������Ҫ��Ľⷨ��������ֹ�ڵ�%s��' % i)
                break
            fitness = self.fitness_ranker(scores)   #ȷ����Ӧ��(��0.0001Ϊ��λ),�ܺ�Ϊ10000
            #print scores,fitness
            seeds,gametes = self.selector(population,fitness)    #ѡ��������Ŀ�ĺ�ѡ����
            population = self.reproducer(seeds,gametes)  #����
        return population,i 
 
    def cached_judge(self,cell): #judge����
        skey = repr(cell)
        if(skey not in self.judgecache):
            #print 'can not find:',skey
            self.judgecache[skey] = self.judge(cell)
        return self.judgecache[skey]
        
 
class Cell(object):   #�����������
    __slots__ = 'length','crossoverer','genes'
    #length:���򴮳���,crossoverer:����㺯��,genes:����
    
    def __init__(self,length,crossoverer,genes=None):
        assert not genes or length == len(genes)
        self.length = length
        self.crossoverer = crossoverer
        self.genes = genes
        if(not self.genes): #����_generate_geneǰself.genes�������и�ֵ(����������������ֵΪNone)
            self.genes = [self._generate_gene(i) for i in xrange(length)]

    def __repr__(self):
        return "<genes:%s>" % (repr(self.genes))
        
    def mate(self,other,mutation_rate = 0):  #�������α�ȻҪ����
        genes1,genes2 = self.crossoverer(self.genes,other.genes)
        self._intround(genes1)
        self._intround(genes2)
        child1,child2 = self.create_by_genes(genes1),self.create_by_genes(genes2)
        if(random.random() < mutation_rate):
            child1.mutation()
        if(random.random() < mutation_rate):
            child2.mutation()
        return child1,child2

    def mutation(self): #ͻ��
        i = random.randint(0,self.length-1)
        #print 'before mutation,genes[%s]:%s' %(i,self.genes[i])
        self.genes[i] = self.gene_mutation(i)
        #print 'after mutation,genes[%s]:%s' %(i,self.genes[i])

    def _generate_gene(self,index): 
        '''������������ڹ��������е��ã���Ϊ�õ���self.genes�����Ե��÷���ǰself.genes�����Ѿ���ֵ(��ֵNoneҲ��)'''
        assert index < self.length
        gene = self.random_gene(index)
        while(self.genes and gene == self.genes[index]):
            gene = self.random_gene(index)
        return gene
    
    @staticmethod
    def _intround(genes):
        for i in xrange(len(genes)):
            genes[i] = int(genes[i] + 0.5)
        return genes


class BCell(Cell):#����Ϊ�����ƴ�
    def __init__(self,length,crossoverer,genes=None):
        super(BCell,self).__init__(length,crossoverer,genes)

    def random_gene(self,index):
        return  random.randint(0,1)

    def gene_mutation(self,index):
        return [1,0][self.genes[index]]

    def create_by_genes(self,genes):
        cell = BCell(self.length,self.crossoverer,genes)
        return cell


class CCell(Cell):#����Ϊ�ַ���
    pool = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def __init__(self,length,crossoverer,genes=None):
        super(CCell,self).__init__(length,crossoverer,genes)

    def random_gene(self,index):
        return  random.choice(self.pool)

    def gene_mutation(self,index):
        return self._generate_gene(index)

    def create_by_genes(self,genes):
        cell = CCell(self.length,self.crossoverer,genes)
        return cell


def rangeround(genes,genes_max):
    assert len(genes) == len(genes_max)
    for i in xrange(len(genes)):
        genes[i] = genes[i] % genes_max[i]
    return genes

class NCell(Cell):#��������
    __slots__ = 'genes_max'  #genes_max:������������ֵ

    def __init__(self,genes_max,crossoverer,genes=None):
        self.genes_max = genes_max    #���������ã���Ϊ����Ҫ�õ�
        super(NCell,self).__init__(len(genes_max),crossoverer,genes)

    def random_gene(self,index):
        return  random.randint(0,self.genes_max[index])

    def gene_mutation(self,index):   #���Բ�ȡһЩ�Ƚϸ��ӵ��㷨���繫ʽ2.61,����򵥴���
        return self._generate_gene(index)

    def create_by_genes(self,genes):
        rangeround(genes,self.genes_max)
        cell = NCell(self.genes_max,self.crossoverer,genes)
        return cell


class NCell2(Cell): #NCell�ı仯�汾������ʱֻ�仯һλ
    __slots__ = 'genes_max','genes_bits'  #genes_max:������������ֵ,genes_bits:������������λ��
    ''' ����ֵ����ʵ����ֵ�ı任����Ϊ����������ԭ����Ҫ���ⲿʹ����ȷ����ͨ������ ����ֵ/genes_max��������� % genes_max
        ���ﲻ����ÿ��gene��maxֵ
    '''

    def __init__(self,genes_max,crossoverer,genes=None):
        self.genes_max = genes_max
        self.genes_bits = self.calc_bits(genes_max)    #���������ã���Ϊ����Ҫ�õ�
        super(NCell2,self).__init__(len(genes_max),crossoverer,genes)

    def random_gene(self,index):
        return  random.randint(0,self.genes_max[index])

    def gene_mutation(self,index):   #1λ�����㷨,���ܳ�����ǰ���ֵ(������ڸ�������??����uplimit��1<<bitnumber-1֮�������?�ֺ���û��??)
        uplimit = self.genes_max[index]
        curv = self.genes[index]
        nextv = curv
        while(nextv > uplimit or nextv == curv): 
            nextv = helper.integer_mutation1(self.genes[index],self.genes_bits[index])
            #print curv,self.genes_bits[index],uplimit,nextv
        return nextv
               
    def create_by_genes(self,genes):
        rangeround(genes,self.genes_max)
        cell = NCell2(self.genes_max,self.crossoverer,genes)
        return cell

    @staticmethod
    def calc_bits(genes_max):
        bits = []
        for uplimit in genes_max:
            bits.append(helper.calc_bitnumber(uplimit))
        return bits


def init_population_bc(initializer,size,length,crossover):
    population = []
    for i in xrange(size):
        population.append(initializer(length,crossover))
    return population

def init_population_bc_with_geness(initializer,geness,crossover):
    assert len(geness) > 0
    length = len(geness[0])
    population = []
    for genes in geness:
        population.append(initializer(length,crossover,genes))
    return population

def init_population_n(initializer,size,genes_max,crossover):
    population = []
    for i in xrange(size):
        population.append(initializer(genes_max,crossover))
    return population

def init_population_n_with_geness(initializer,geness,genes_max,crossover):
    assert len(geness) > 0
    population = []
    for genes in geness:
        population.append(initializer(genes_max,crossover,genes))
    return population

