#!/usr/bin/env python
# -*- coding: utf-8 -*-

# problemi:
# - ne vidi se ko je ulogiran, zbog sesije
# - ssl?
# - drugi načini ulogiravanja?
# - ip adresa?

# todo
#   gumbi se trebaju zvati sa IDom pitanja
#   ostale opcije testa (checkbox za MCMA, ...)
#   test report - bodovi
#   ako komentar nije enablean, ...

# reference:
# http://www.wxpython.org/docs/api/wx.Colour-class.html
# http://www.blog.pythonlibrary.org/2011/01/04/wxpython-wx-listctrl-tips-and-tricks/
# http://wxpython.org/Phoenix/docs/html/ListCtrl.html  <---- eventovi!!!
# http://wxpython-users.1045709.n5.nabble.com/wxPython-Listcontrol-GetItemData-td2276631.html <----- getdata
# http://www.blog.pythonlibrary.org/2010/06/16/wxpython-how-to-switch-between-panels/
# http://www.blog.pythonlibrary.org/2013/07/12/wxpython-making-your-frame-maximize-or-full-screen/
# ctrl+alt+del http://superuser.com/questions/740679/catching-ctrl-alt-delete
# ctrl+alt+del linux: http://unix.stackexchange.com/questions/153902/disabling-ctrl-alt-del-and-etc-init
# font: http://www.wxpython.org/docs/api/wx.Font-class.html
# font: http://www.blog.pythonlibrary.org/2011/04/28/wxpython-learning-to-use-fonts/
# http://stackoverflow.com/questions/6340362/redirecting-key-events-of-child-widgets-to-their-parent-frame-widget
# alttab http://markmail.org/message/b6t6ldf3f3gl66gg#query:+page:1+mid:on3tlpd553mkdi2i+state:results
# unicode: http://stackoverflow.com/questions/8365660/python-mysql-unicode-and-encoding
# add controls: http://www.blog.pythonlibrary.org/2012/05/05/wxpython-adding-and-removing-widgets-dynamically/
# scrolled window:
#   http://wxpython-users.1045709.n5.nabble.com/ScrolledWindow-sizing-issues-td2352337.html
# htmlwindow tagovi 2015-05-04
#   http://wxpython.org/Phoenix/docs/html/html_overview.html
# remove flickering (timer)2015-05-08
#   http://www.java2s.com/Tutorial/Python/0380__wxPython/Usetimer.htm
# hotkeys
#   http://wiki.wxpython.org/RegisterHotKey -> loše
#   http://jeffhoogland.blogspot.com/2014/10/pyhook-for-linux-with-pyxhook.html -> linux
#   http://sourceforge.net/p/pyhook/wiki/PyHook_Tutorial/ -> win
# self.Raise() 2015-05-10
#   https://groups.google.com/forum/#!topic/wxpython-users/zuz6pfQoxes
# AcceleratorTable 2015-05-10
#   http://www.wxpython.org/docs/api/wx.AcceleratorTable-class.html
#   http://markmail.org/message/kgdizhwtkajntpnu
# pyHook
#
# check if running on windows
#   http://stackoverflow.com/questions/1325581/how-do-i-check-if-im-running-on-windows-in-python

import pyHook
import wx
import pyTCExam
import pyTCExamMySQL
import pyTCExamUser
import pyTCExamTest
from pyTCExamLoginGui import PanelLogin
from pyTCExamTestListGui import PanelTestList
from pyTCExamTestStartGui import PanelTestStart
from pyTCExamTestGui import PanelTest
from pyTCExamTestReportGui import PanelTestReport


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
class FrameMain(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        # always on top
        wx.Frame.__init__(self, parent=parent, id=wx.NewId(), title='pyTCExam', style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)
        # normalno
        #wx.Frame.__init__(self, parent=parent, id=wx.NewId(), title='pyTCExam', style=wx.DEFAULT_FRAME_STYLE, size=(1000, 800))

        # database object
        self.db = pyTCExamMySQL.DbMySQL("localhost", "root", "passww", "tcexam")
        # user object
        self.user = pyTCExamUser.User(self.db)
        # test object
        self.test = pyTCExamTest.Test(self.db)

        self.panelLogin = PanelLogin(self, self.db, self.user)
        self.panelTestList = PanelTestList(self, self.db, self.user)
        self.panelTestStart = PanelTestStart(self, self.test)
        self.panelTest = PanelTest(self, self.test)
        self.panelTestReport = PanelTestReport(self)

        # box sizer for panels -> all panels are in same frame
        mainVSizer = wx.BoxSizer(wx.VERTICAL)
        mainVSizer.Add(self.panelLogin, 1, wx.EXPAND)
        mainVSizer.Add(self.panelTestList, 1, wx.EXPAND)
        mainVSizer.Add(self.panelTestStart, 1, wx.EXPAND)
        mainVSizer.Add(self.panelTest, 1, wx.EXPAND)
        mainVSizer.Add(self.panelTestReport, 1, wx.EXPAND)
        self.SetSizer(mainVSizer)

        # bind close event
        self.Bind(wx.EVT_CLOSE, self.__onCloseWindow)

        # keyboard hook, left+right win key, left+right control, left+right alt, tab, f4
        self.hook = pyHook.HookManager()
        self.hook.KeyDown = self.onKeyboardEvent
        self.hook.HookKeyboard()

    #----------------------------------------------------------------------
    def onKeyboardEvent(self, event):
        if event.Key.lower() in ['lwin', 'rwin', 'lcontrol', 'rcontrol', 'lalt', 'ralt', 'tab', 'f4']:
            return False
        else:
            return True


    #----------------------------------------------------------------------
    def userLogin(self):
        self.panelLogin.Hide()
        self.panelTestList.refreshTests()
        self.panelTestList.Show()
        self.Layout()


    #----------------------------------------------------------------------
    def userLogoff(self):
        self.panelTestList.Hide()
        self.panelLogin.Show()
        self.Layout()


    #----------------------------------------------------------------------
    def initTest(self):
        """ u listi odabran ispit -> klik na "započni s rješavanjem" """
        self.test.initTest(userId=self.user.id, testId=self.panelTestList.selectedTestId)
        self.panelTestStart.loadTestData()
        self.panelTestList.Hide()
        self.panelTestStart.Show()
        self.Layout()


    #----------------------------------------------------------------------
    def startTest(self):
        """ klik na pokretanje testa u prozoru sa detaljima ispita """
        self.test.initTest(userId=self.user.id, testId=self.panelTestList.selectedTestId)
        self.panelTestStart.Hide()
        self.panelTest.initUi()
        self.panelTest.Show()
        self.Layout()


    #----------------------------------------------------------------------
    def initTestCancel(self):
        """ vraćanje na popis ispita """
        self.panelTestStart.Hide()
        self.panelTestList.refreshTests()
        self.panelTestList.Show()
        self.Layout()


    #----------------------------------------------------------------------
    def continueTest(self):
        self.test.initTest(userId=self.user.id, testId=self.panelTestList.selectedTestId)
        self.panelTestList.Hide()
        self.panelTest.initUi()
        self.panelTest.Show()
        self.Layout()


    #----------------------------------------------------------------------
    def repeatTest(self):
        self.test.initTest(userId=self.user.id, testId=self.panelTestList.selectedTestId)
        self.test.repeatTest()
        self.test.executeTest()
        self.test.initTest(userId=self.user.id, testId=self.panelTestList.selectedTestId)
        self.panelTestList.Hide()
        self.panelTest.initUi()
        self.panelTest.Show()
        self.Layout()


    #----------------------------------------------------------------------
    def terminateTest(self):
        self.panelTest.Hide()
        self.panelTestList.refreshTests()
        self.panelTestList.Show()
        self.Layout()


    #----------------------------------------------------------------------
    def showReport(self):
        self.test.initTest(userId=self.user.id, testId=self.panelTestList.selectedTestId)
        self.panelTestReport.initUi(self.user, self.test)
        self.panelTestList.Hide()
        self.panelTestReport.Show()
        self.Layout()


    #----------------------------------------------------------------------
    def closeReport(self):
        self.panelTestReport.Hide()
        self.panelTestList.refreshTests()
        self.panelTestList.Show()
        self.Layout()


    #----------------------------------------------------------------------
    def __onCloseWindow(self, event):
        """
        Method called by EVT_CLOSE event.

        Args:
            event
        """
        self.appClose()


    #----------------------------------------------------------------------
    def appClose(self):
        # stop the timer
        self.panelTest.timerCountdown.Stop()
        # destroy the timer
        self.panelTest.timerCountdown.Destroy()
        # remove keyboard hook
        self.hook.UnhookKeyboard()
        # destroy frame
        self.Destroy()


#----------------------------------------------------------------------
class App(wx.App):
    def OnInit(self):
        self.frame = FrameMain(parent=None)
        # produkcija - odkomentirati
        self.frame.ShowFullScreen(show=True)

        # develop - zakomentirati
        #self.frame.Center(direction=wx.BOTH)
        #self.frame.Show()

        self.SetTopWindow(frame=self.frame)
        return True


#----------------------------------------------------------------------
if __name__ == '__main__':
    pyTCExam.main()