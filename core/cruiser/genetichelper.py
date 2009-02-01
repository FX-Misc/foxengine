# -*- coding: utf-8 -*-

"""
�Ŵ��㷨�ĸ�������
"""

import random
from math import log
from bisect import bisect_left as locate

MAX_POPULATION_SIZE = 4096  #�����Ⱥ��С
#��С��������16�����ܸ���
RANK_BASE = 10000   #��Ⱥ��Ӧ�ȵ��ܺ�(���൱��1),ÿ��1��ʾ���֮һ

def accumulate(source):
    sum = 0
    rev = [0] * len(source)
    for i in xrange(0,len(source)):
        sum += source[i]
        rev[i] = sum
    return rev

######crossover(����/����)�Ŀ��ƺ���,��Ӧ��λ����ʵֵ��gene
def random_crossover(parent_genes1,parent_genes2):  #�������,#������λ����ʵֵ
    assert len(parent_genes1) == len(parent_genes2)
    turning_points = random_crosspoints(len(parent_genes1))
    return weave(parent_genes1,parent_genes2,turning_points,exchange)

def uniform_crossover(parent_genes1,parent_genes2):#������λ����ʵֵ
    '''����(һ��)����,ÿһλ����Ҫѡ��. ѡ��ĸ�����0.5:0.5(����0�ĸ��ʶ���0.000...001)'''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = parent_genes1[:],parent_genes2[:]   #�Ӵ�����Ĭ�ϸ��Ƹ���
    for i in xrange(len(parent_genes1)):
        if(random.random() > 0.5):  #����
            genes1[i],genes2[i] = genes2[i],genes1[i]
    return genes1,genes2

def single_point_crossover(parent_genes1,parent_genes2):#������λ����ʵֵ
    ''' ���ν���(���㽻��,���淽ʽΪ����)
        ԭ���ϵ��㽻������ò���Ϊ1�Ķ�㽻�����滻
        ����������һ��len=2�����Σ���Ȼ���е㽻�棬������Ҫһ������Ĵ���
    '''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = parent_genes1[:],parent_genes2[:]   #�Ӵ�����Ĭ�ϸ��Ƹ���
    if(len(parent_genes1) == 2):#���ֻ������Ԫ�أ��򽻲�λ��ȻΪ1
        turning_points = [1]
    else:
        turning_points = [random.randint(1,len(parent_genes1))]    #cpoint��Ҳ����,��ѡ0�Ǳ���ȫ�����棬�൱��û�н���
    return weave(parent_genes1,parent_genes2,turning_points,exchange)

def single_point_crossover_g(parent_genes1,parent_genes2):#������λ����ʵֵ
    ''' ��׼���ν���(���㽻��,���淽ʽΪ����)
        û���������εĵ��㽻�棬������bitgroup��ʽ�Ļ�����(bitgroup��ʽÿһ����������������,������岻�������廥����������)
        �൱��multi_points_crossover_factory(1)
    '''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = parent_genes1[:],parent_genes2[:]   #�Ӵ�����Ĭ�ϸ��Ƹ���
    turning_points = [random.randint(0,len(parent_genes1))]    #cpoint��Ҳ����,��ѡ0�Ǳ���ȫ�����棬�൱��û�н���
    return weave(parent_genes1,parent_genes2,turning_points,exchange)

def multi_points_crossover_factory(number=2):  #��㽻�湤��
    def crossover(parent_genes1,parent_genes2):#������λ����ʵֵ
        '''��ν���(��㽻��,���淽ʽΪ����)'''
        #print 'number:',number
        assert len(parent_genes1) == len(parent_genes2)
        genes1,genes2 = parent_genes1[:],parent_genes2[:]   #�Ӵ�����Ĭ�ϸ��Ƹ���
        turning_points = [random.randint(0,len(parent_genes1)) for i in xrange(number)]  #�����
        turning_points.sort()
        return weave(genes1,genes2,turning_points,exchange)
    return crossover

def discrete_crossover(parent_genes1,parent_genes2):#������λ����ʵֵ
    '''��ɢ���飬�����(һ��)�����������ÿ���Ӵ���������ѡ�񣬲����ǽ���(���������Ӵ���ĳ����λ��������ͬһ��parent)'''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = parent_genes1[:],parent_genes1[:]   #�Ӵ�����Ĭ�ϸ���parent1
    for i in xrange(len(parent_genes1)):
        if(random.random() > 0.5):  #�����Ӵ�1
            genes1[i] = parent_genes2[i]
        if(random.random() > 0.5):  #�����Ӵ�2
            genes2[i] = parent_genes2[i]
    return genes1,genes2

def middle_crossover(parent_genes1,parent_genes2,d=0.25):#ֻ����ʵֵ
    ''' �м����� �Ӹ��� = ������1 + a*(������2-������1)
        a�Ǵ���[-d,1+d]�ϵ��������ͨ��dȡ0.25
        ÿ���Ӵ���ÿ�������ж�����aֵ
    '''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = [],[]
    random2range = lambda rm,dd = d : -dd + rm * ( 1 + 2 * dd)  
    for i in xrange(len(parent_genes1)):
        a1 = random2range(random.random())
        a2 = random2range(random.random())
        genes1.append(parent_genes1[i] + a1 * (parent_genes2[i]-parent_genes1[i]))
        genes2.append(parent_genes1[i] + a2 * (parent_genes2[i]-parent_genes1[i]))
    #print genes1,genes2
    return genes1,genes2
        
def middle_sym_crossover(parent_genes1,parent_genes2,d=0.25):#ֻ����ʵֵ
    ''' �Գ��м����� 
        �Ӹ���1 = ������1 + a*(������2-������1)
        �Ӹ���2 = ������2 + a*(������1-������2)
        a�Ǵ���[-d,1+d]�ϵ��������ͨ��dȡ0.25
        �����Ӵ���ÿ�Ե�λ������һ��������aֵ
    '''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = [],[]
    random2range = lambda rm,dd = d : -dd + rm * ( 1 + 2 * dd)  
    for i in xrange(len(parent_genes1)):
        a = random2range(random.random())
        genes1.append(parent_genes1[i] + a * (parent_genes2[i]-parent_genes1[i]))
        genes2.append(parent_genes2[i] + a * (parent_genes1[i]-parent_genes2[i]))
    return genes1,genes2


def linear_crossover(parent_genes1,parent_genes2,d=0.25):#ֻ����ʵֵ
    ''' �������� �Ӹ��� = ������1 + a*(������2-������1)
        a�Ǵ���[-d,1+d]�ϵ��������ͨ��dȡ0.25
        ÿ���Ӵ�����һ��������aֵ
    '''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = [],[]
    random2range = lambda rm,dd = d : -dd + rm * ( 1 + 2 * dd)  
    a1 = random2range(random.random())
    a2 = random2range(random.random())
    for i in xrange(len(parent_genes1)):
        genes1.append(parent_genes1[i] + a1 * (parent_genes2[i]-parent_genes1[i]))
        genes2.append(parent_genes1[i] + a2 * (parent_genes2[i]-parent_genes1[i]))
    return genes1,genes2

def linear_sym_crossover(parent_genes1,parent_genes2,d=0.25):#ֻ����ʵֵ
    ''' �Գ��������� 
        �Ӹ���1 = ������1 + a*(������2-������1)
        �Ӹ���2 = ������2 + a*(������1-������2)
        a�Ǵ���[-d,1+d]�ϵ��������ͨ��dȡ0.25
        �����Ӵ�����aֵ
    '''
    assert len(parent_genes1) == len(parent_genes2)
    genes1,genes2 = [],[]
    random2range = lambda rm,dd = d : -dd + rm * ( 1 + 2 * dd)  
    a = random2range(random.random())
    for i in xrange(len(parent_genes1)):
        genes1.append(parent_genes1[i] + a * (parent_genes2[i]-parent_genes1[i]))
        genes2.append(parent_genes2[i] + a * (parent_genes1[i]-parent_genes2[i]))
    return genes1,genes2

def bitgroups_crossover_factory(bitgroups,icrossover=single_point_crossover,icrossover_rate=1.01):
    ''' λ�������齻�溯��
        bitgroupsΪλ�����size�б��ֱ��ʾ���ٸ�����λ���һ���Ա�ʾһ������
        icrossoverΪλ����Ľ��淽��
        icrossoverrateΪ�ⲿ����crossover֮���ڲ����������crossover����. 
            icrossover > 1��ʾֻҪ�������������ÿ����λ�����Ȼ��icrossover��ʽ����
        ���icrossover = uniform_crossover,��icrossover_rate>1.0�����൱��ֱ��ʹ��uniform_crossover
    '''
    def crossover(parent_genes1,parent_genes2):
        assert len(parent_genes1) == len(parent_genes2) == sum(bitgroups)
        cur = 0
        genes1,genes2 = [],[]
        for limit in bitgroups:
            if(random.random() < icrossover_rate):
                cgenes1,cgenes2 = icrossover(parent_genes1[cur:cur+limit],parent_genes2[cur:cur+limit])
                genes1.extend(cgenes1)
                genes2.extend(cgenes2)
            else:
                genes1.extend(parent_genes1[cur:cur+limit])
                genes2.extend(parent_genes2[cur:cur+limit])
            cur += limit
        #print 'parents:',parent_genes1,parent_genes2
        #print 'children:',genes1,genes2
        return genes1,genes2
    return crossover

###����/����ģ�庯��###
def weave(parent_genes1,parent_genes2,turning_points,weave_functor): 
    ''' ������,����������������ͽ���ת�۵�(turning_points������״̬�ķ�ת��)���Լ�����״̬�µĲ�������weave_functor
        �����Ӵ�����
    '''
    assert len(parent_genes1) == len(parent_genes2)
    if(len(turning_points) == 0):
        return parent_genes1,parent_genes2
    assert turning_points[-1] <= len(parent_genes2)
    genes1,genes2 = parent_genes1[:],parent_genes2[:]   #�Ӵ�����Ĭ�ϸ��Ƹ���
    ttps = turning_points + [len(parent_genes1)]    #�ڱ���,��Ҫʱ�������һ�εĽ���
    #print ttps
    pre = 0
    cross_flag = False
    for tp in ttps:
        if(cross_flag):
            weave_functor(genes1,genes2,pre,tp)
        cross_flag = not cross_flag
        pre = tp
    return genes1,genes2

#���������/���溯��
def exchange(genes1,genes2,begin,end): #��λ����������,�����[begin,end)�ĵ�λ����
    assert len(genes1) == len(genes2)
    assert 0 <= begin  <= end <= len(genes1)
    for index in xrange(begin,end):
        genes1[index],genes2[index] = genes2[index],genes1[index]
    return genes1,genes2

###����������/���渨������
def random_crosspoints(gene_length):
    ''' �����㽻��
        ����������ֵ�����ת�۵�
        ��0����һ��ת�۵�Ĳ���Ϊ��һ���֣�����Ϊ�ڶ���������....
        ÿ���������ֲ�����(0��ʾ)��ż�����ֽ���(1��ʾ)
    '''
    lastpart = random.randint(1,gene_length)    #lastpart����Ϊ0�����򽫲������ѭ��
    turning_points = []
    curpoint = 0
    while(curpoint < lastpart):
        part = random.randint(0,gene_length - curpoint)
        curpoint += part
        turning_points.append(curpoint)
    return turning_points

######��Ӧ��
###��Ӧ�ȼ���
def linear_rank(scores):
    return _simple_rank(scores,_calc_linear_rank)

def nonlinear_rank(scores):
    return _simple_rank(scores,_calc_nonlinear_rank)

def intround(fv):
    return int(fv + 0.5)

_indices = xrange(MAX_POPULATION_SIZE)
def _simple_rank(scores,rank_functor,*args):
    pairs = zip(scores,_indices)
    pairs.sort()    #����
    pairs.reverse() #���򣬷�ֵ��ߵ�����ǰ��
    ranks = rank_functor(len(scores),*args)
    orders = zip([second for first,second in pairs],ranks)
    orders.sort()
    return [second for first,second in orders]

###��Ӧ����ֵ����
cached_linear_ranks = {}
cached_nonlinear_ranks = {}
#������Ӧ�ȼ���
def _calc_linear_rank(length,first_times = 1.8): 
    ''' ����<�Ŵ��㷨--���ۡ�Ӧ�������ʵ��p29,��ʽ2.50
        ���ص��б���ÿ��Ԫ�ض�����0.0001Ϊ��λ����������ʾ����
        ����㷨��lengthû��Ҫ��
        ���� 1 < first_times < 2 (<1��Ϊ����>2������󲿷ֳ��ָ���)
    '''
    ranks_key = '%s_%s' % (length,first_times)
    if(ranks_key in cached_linear_ranks):
        return cached_linear_ranks[ranks_key]
    ns = 2 * first_times - 2.0
    d1 = 1.0/length
    d2 = 1.0/(length-1)
    #print ns,d1,d2
    ranks = []
    for i in xrange(0,length):
        #print RANK_BASE * d1 * (first_times - ns*i*d2)
        ranks.append(intround(RANK_BASE * d1 * (first_times - ns*i*d2)))
    #print ranks,sum(ranks)
    epsl = RANK_BASE - sum(ranks)
    ranks[0] += epsl    #���ӵ���һ��
    cached_linear_ranks[ranks_key] = ranks
    return ranks

#��������Ӧ�ȼ���
def _calc_nonlinear_rank(length,first=0.2):
    ''' ����<�Ŵ��㷨--���ۡ�Ӧ�������ʵ��p30,��ʽ2.51
        ���ص��б���ÿ��Ԫ�ض�����0.0001Ϊ��λ����������ʾ����
        Ҫ��length>=16. (������������Ѻ���)
        firstΪ�����һ��Ԫ�صĸ��ʣ�Ĭ��Ϊ0.2������ 0 < first < 1 (��Ϊ��epsl�ĵ���������firstֻҪ>0�Ϳ���.Ϊ0���һԪ��Ϊ10000�����Ϸ�)
    '''
    assert length >= 16 #���length̫С������㷨���������
    ranks_key = '%s_%s' % (length,first)
    if(ranks_key in cached_nonlinear_ranks):
        return cached_nonlinear_ranks[ranks_key]
    factor = 1-first
    ranks = [intround(first * RANK_BASE)]
    cur = first
    for i in xrange(1,length):
        cur = cur * factor
        ranks.append(intround(cur * RANK_BASE))
    epsl = RANK_BASE - sum(ranks)
    ranks[0] += epsl    #���ӵ���һ��
    cached_nonlinear_ranks[ranks_key] = ranks
    return ranks

######ѡ���㷨,���е�ѡ���㷨������2������Ϊ��Ⱥ����*2������,��һ������Ϊ������У��ڶ�������Ϊǰ�ߵ��������(����һ����Ԫ����Ҫ��Ե�ʱ��)
###���������ܴ���ֲ�ѡ��
#����ѡ��
def roulette(sums):
    v = random.randint(0,sums[-1])
    return locate(sums,v)

#���о���
bits = [0,1]
dcache = {}

def cached_distance2(seq1,seq2):
    skey = repr(seq1) + repr(seq2)
    if(skey not in dcache):
        #print 'new distance'
        dcache[skey] = distance2(seq1,seq2)
    else:
        #print 'cached distance'
        pass
    return dcache[skey]

def distance2(seq1,seq2):   #���������еľ���
    assert len(seq1) > 0
    if(isinstance(seq1[0],int)):
        if(seq1[0] not in bits or seq1[-1] not in bits or seq2[0] not in bits or seq2[1] not in bits):
            #�������жϣ���������һ���жϵĺ�ʱ����
            return distance2i(seq1,seq2)
        elif(set(seq1).issubset([0,1])):#��ȥ��set(seq2)���ж�
            return distance2b(seq1,seq2)
        else:#��Ȼ����������
            return distance2i(seq1,seq2)
    elif(isinstance(seq1[0],str)):
        return distance2c(seq1,seq2)
    else:
        assert False

def distance2c(seq1,seq2):#�������ַ����еľ���
    assert len(seq1) == len(seq2)
    sum = 0
    for i in xrange(len(seq1)):
        sd = ord(seq1[i]) - ord(seq2[i])
        sum += sd * sd
    return sum

def distance2i(seq1,seq2):   #������ʵ�����еľ���
    assert len(seq1) == len(seq2)
    sum = 0
    for i in xrange(len(seq1)):
        sum += (seq1[i] - seq2[i]) * (seq1[i] - seq2[i])
    return sum

def distance2b(seq1,seq2):   #������λ���е����λ��
    assert len(seq1) == len(seq2)
    sum = 0
    for i in xrange(len(seq1)):
        sum += seq1[i] - seq2[i] > 0 and seq1[i] - seq2[i] or seq2[i] - seq1[i]
    return sum

##�����ڼ�
#�����ڼ�
def find_adjacents(population,seed,adj_number,distancer = cached_distance2):
    ''' populationΪ��Ⱥ����,seedΪѡ�еĸ���,adj_numberΪ����������Ҫѡ�������������ھ���
        �����ҵ����ڼ�������
    '''
    assert adj_number < len(population)
    distance2s = [distancer(seed.genes,unit.genes) for unit in population]
    pairs = zip(distance2s,_indices)
    pairs.sort()
    return [index for distance,index in pairs[1:adj_number+1]]

#���̶�ѡ���㷨
def roulette_wheel_selection_factory(times=1):
    assert isinstance(times,int)
    def roulette_wheel_selection(population,fitness):
        assert len(fitness) > 0
        length = times * len(fitness)
        sums = accumulate(fitness)    #��Ȼ����
        seeds = []
        gametes = []    #��ż��
        for i in xrange(0,length):
            seed = population[roulette(sums)]
            gamete = population[roulette(sums)]
            while(gamete == seed):
                gamete = population[roulette(sums)]
            seeds.append(seed)            
            gametes.append(gamete)
        return seeds,gametes
    return roulette_wheel_selection

#�ض�ѡ��
def truncate_selection_factory(times=1,truncate_rate=0.5):
    assert isinstance(times,int)
    def truncate_selection(population,fitness):
        assert len(fitness) > 0
        length = times * len(fitness)
        pairs = zip(fitness,population)
        pairs.sort()
        pairs.reverse()
        snumber = int(len(pairs) * truncate_rate + 0.5)
        pool = [ cell for fit,cell in pairs][:snumber]
        seeds = []
        gametes = []    #��ż��
        for i in xrange(length):
            seed = random.choice(pool)
            gamete = random.choice(pool)
            while(gamete == seed):
                gamete = random.choice(pool)
            seeds.append(seed)
            gametes.append(gamete)
        return seeds,gametes
    return truncate_selection

#����ڼ�ѡ�񷨹��� ������p31�е������ڼ�������ɢЧ�ʺ㶨
#����������㿪���ܴ�ÿһ����������Ⱥ��С������distance sort.
def adjacent_selection_factory(times=1,adj_factor = 0.2,adj_finder = find_adjacents):
    def adjacent_selection(population,fitness):    #adjnumber�ڽ�����,Ϊ��Ⱥ����һ���ٷֱ�
        ''' ���ڴ�fitness���ҵ���ÿ������㣬��gemete�Ӿ��������len(fitness) * adj_factor��Ԫ�������ѡ��'''
        length = times * len(fitness)
        adj_number = intround(len(fitness) * adj_factor)
        #print adj_number,len(population),len(fitness),len(fitness) * adj_factor
        sums = accumulate(fitness)    #��Ȼ����
        seeds = []
        gametes = []    #��ż��
        for i in xrange(0,length):
            seed = population[roulette(sums)]
            seeds.append(seed)
            candidates = find_adjacents(population,seed,adj_number)
            gametes.append(population[candidates[random.randint(0,adj_number-1)]])
        return seeds,gametes
    return adjacent_selection

######�����㷨
#�����Ķ����Ʊ�ʾλ������
def calc_bitnumber(uplimit):
    return int(log(uplimit,2)+0.99999)

#������һλ����
def integer_mutation1(value,bitnumber):
    ''' bitnumberΪ��������������ռ�Ķ�����λ��'''
    bit = random.randint(0,bitnumber-1)
    xorv = 1 << bit
    return value ^ xorv
    
######��ֳ�����㷨
#�򵥷�ֳ�㷨����. crossover_rate�����Ƿ񽻲棬����������ֱ�Ӹ���
def simple_reproducer_factory(crossover_rate,mutation_rate): 
    def reproducer(seeds,gametes):
        #print seeds
        assert len(seeds) == len(gametes)
        children = []
        cur = 0
        while(len(children) < len(seeds)):
            if(random.random() < crossover_rate):
                children.extend(list(seeds[cur].mate(gametes[cur],mutation_rate)))
                cur += 1
            else:
                children.extend([seeds[cur],gametes[cur]])
        assert len(children) == len(seeds)
        #print 'children size: %s' % len(children)
        return children
    reproducer.times_of_length = 1
    return reproducer

#2��1. crossover_rate�����Ƿ񽻲棬����������ֱ�Ӹ���
def simple21_reproducer_factory(crossover_rate,mutation_rate): 
    def reproducer(seeds,gametes):
        #print seeds
        assert len(seeds) == len(gametes)
        children = []
        cur = 0
        while(len(children) < len(seeds)):
            if(random.random() < crossover_rate):
                child1,child2 = seeds[cur].mate(gametes[cur],mutation_rate)
                children.append(child1) #ȡ��һ���Ӵ�
                cur += 1
            else:
                children.append(seeds[cur])
        assert len(children) == len(seeds)
        #print 'children size: %s' % len(children)
        return children
    reproducer.times_of_length = 1
    return reproducer

######������������
def bits2int(bits): #��bits�б�ת��Ϊ��Ӧ��intֵ,���и�λ��ǰ����[1,0,0,1,1] ==> 19
    value = 0
    length = len(bits)
    for i in xrange(length):
        value += pow(2,length - i - 1) * bits[i]
    return value

#��bitsת��Ϊints,isizesΪÿ������ռ��λ��,��[4,6,4,2]��,bitsΪλ��
def bits2ints(isizes,bits):
    assert sum(isizes) == len(bits)
    cur = 0
    ints = []
    for s in isizes:
        ints.append(bits2int(bits[cur:cur+s]))
        cur += s
    return ints

def int2bits(iv,bitnumber):
    bs = []
    while(iv > 0):
        bs.insert(0,iv & 1)
        iv >>= 1
    assert len(bs) <= bitnumber
    bs[0:0] = [0] * (bitnumber - len(bs))
    return bs
        
def ints2bits(isizes,ints):
    assert len(ints) == len(isizes)
    bs = []
    for i in xrange(len(ints)):
        bs.extend(int2bits(ints[i],isizes[i]))
    return bs

