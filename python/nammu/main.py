'''
Created on 15 Apr 2015

Python entry point invoked from Java's entry point.

@author: raquel-ucl
'''

from controller.NammuController import NammuController
#from pyoracc.atf.atffile import AtfFile
#from pyoracc.test.fixtures import belsunu
#import codecs

#testATF = AtfFile(codecs.open("/Users/raquelalegre/workspace/ORACC/nammu/python/pyoracc/test/fixtures/tiny_corpus/belsunu.atf",
#                      encoding='utf-8').read())
#
#print testATF.serialize()

def main():
    NammuController()
    
if __name__ == '__main__':
    main()