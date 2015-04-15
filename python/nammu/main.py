'''
Created on 25 Mar 2014

@author: raquel-ucl
'''
from javax.swing import JFrame, JTabbedPane, JPanel, BoxLayout, JEditorPane, BorderFactory, JLabel, JTextField, JScrollPane
from javax.swing.event import DocumentListener
from java.awt import BorderLayout, GridLayout, Color, Dimension
from javax.swing.border import BevelBorder
from java.lang import Short
from org.kohsuke.github import GitHub
from nammu import Nammu
from pyoracc.atf.atffile import AtfFile
from pyoracc.test.fixtures import belsunu
import codecs

testATF = AtfFile(codecs.open("/Users/raquelalegre/workspace/ORACC/nammu/python/pyoracc/test/fixtures/tiny_corpus/belsunu.atf",
                       encoding='utf-8').read())

print testATF.serialize()

def main():
    Nammu()
    
if __name__ == '__main__':
    main()