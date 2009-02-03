# -*- coding: gbk -*-
'''
    ����ָ��Ŀ¼�µ����в����ļ����������еĲ�������
'''
#This file is licensed under the Apache License Version 2.0
#author: wycharon@gmail.com

from django.core.management import setup_environ
#import wolfox.foxit.settings as settings
import wolfox.foxit.other_settings.settings_sqlite_test as settings
setup_environ(settings)

import sys, os, os.path, re, unittest

TEST_FILE_PATTERN = 'test\.py$' #Ĭ�ϵĲ����ļ���Ϊ��test.py��β���ļ�,��test��ͷ��.py�ļ���pattern��Ϊ��'\Atest\w*\.py$'
IGNORE_DIR_TYPE = ['.svn','CVS']

def find_tests_in_directory(root_path,sub_path): #root_path:��ʼĿ¼��sub_path:Ŀ��Ŀ¼���������ʼĿ¼��·��
    sub_package = sub_path.replace(os.path.sep,'.')
    filenames = [ os.path.splitext(name)[0] for name in os.listdir(sub_path) if find_tests_in_directory.pattern.search(name) ]
    module_names = [ sub_package and sub_package + '.' + name or name for name in filenames ]
    #print module_names
    gs,ls = globals(),locals()
    modules = [ __import__(module_name,gs,ls,[sub_package]) for module_name in module_names]    #ֻ�������ŷ��ص����module,������xxx.yyyʱ�����ص���xxx��������yyy.�μ�__import__���ĵ�
    #print root_path,sub_path,modules
    tests = [ unittest.defaultTestLoader.loadTestsFromModule(module) for module in modules ]
    #print sub_path,[ test.countTestCases() for test in tests]
    #return unittest.TestSuite()
    return unittest.TestSuite(tests)

def find_all_tests():
    all_tests = unittest.TestSuite()
    root_path = os.getcwd()
    sys.path.append(root_path)
    len_root_path = len(root_path)
    for root,dirs,files in os.walk(root_path):    
        #����Ŀ¼����ʱ�ڲ��޸ĵ�ǰ����Ŀ¼����Ա������̲���Ӱ��(���Ŀ¼����Ӱ��.walk�������Ŀ¼����ʱ�������ڲ��䶯Ŀ¼)
        #print root  #�鿴�ǲ��ǻ����������Ŀ¼�Լ�����Ŀ¼
        for entry in find_all_tests.ignore:
            if(entry in dirs):
                dirs.remove(entry)
        sub_path = root[len_root_path+1:]    #��������root_path��Ŀ¼
        #print sub_path
        all_tests.addTest(find_tests_in_directory(root_path,sub_path))
    return all_tests

#regression_test.pattern = re.compile(TEST_FILE_PATTERN, re.IGNORECASE)
find_tests_in_directory.pattern = re.compile(TEST_FILE_PATTERN, re.IGNORECASE)
find_all_tests.ignore = IGNORE_DIR_TYPE

import optparse
if __name__ == "__main__":                   
    import logging
    logging.basicConfig(filename="regression.log",level=logging.DEBUG,format='#%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    #unittest.main(defaultTest="regression_test")
    parser = optparse.OptionParser()
    #parser.add_option("-r","--recursion", action="store_true", dest="recursion",help="����������Ŀ¼�µĲ���")    #������Ŀ¼
    parser.add_option("-o","--only", action="store_true", dest="only",help="ִֻ��ָ��Ŀ¼�µĲ��ԣ���������Ŀ¼. δָ��ʱ����������Ŀ¼")    #ֻ��ǰĿ¼
    parser.add_option('-d',"--directory",default='.',dest='directory',help="������ʼĿ¼")
    parser.add_option('-f',"--force",action="store_true",dest='force',help="ǿ�Ʊ��ļ�����Ŀ¼Ϊ������ʼĿ¼��������-d")
    parser.add_option('-p',"--pattern",default='test\.py$',dest='pattern',help="�����ļ���ģʽ")
    parser.add_option('-i',"--ignore",default=IGNORE_DIR_TYPE,dest='ignore',help="���Ե�Ŀ¼������.svn/cvs")
    
    options,arguments = parser.parse_args()   
    find_all_tests.ignore = options.ignore.split(',')
    #regression_test.pattern = re.compile(options.pattern, re.IGNORECASE)
    find_tests_in_directory.pattern = re.compile(options.pattern, re.IGNORECASE)
    file_path = lambda filename : os.path.split(os.path.abspath(filename))[0]   #�������·���ļ�����þ���·��
    #print __file__,file_path(__file__)
    target_directory = options.force and file_path(__file__) or options.directory
    os.chdir(target_directory)
    test_runner = unittest.TextTestRunner()
    if(options.only):
        test_runner.run(find_tests_in_directory(target_directory,''))    #����ֱ��ʹ��unittest.main,�ᵼ�������в�����ͻ
    else:
        test_runner.run(find_all_tests())   #����ֱ��ʹ��unittest.main,�ᵼ�������в�����ͻ

