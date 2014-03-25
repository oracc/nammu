'''
Created on 25 Mar 2014

@author: jamespjh
'''

from javax.swing import JButton, JFrame
from org.kohsuke.github import GitHub

gh=GitHub.connect()
me=gh.getMyself()


frame = JFrame('Hello, Jython!',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE,
            size = (300, 300)
        )

button = JButton('Click to get your name from GitHub!')

frame.add(button)

def change_text(event):
    button.setText(me.name)

button.actionPerformed=change_text

def main():
    print "Python called"
    frame.visible = True