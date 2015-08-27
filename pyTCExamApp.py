#!/usr/bin/env python
# -*- coding: utf-8 -*-

# todo
#   gumbi se trebaju zvati sa IDom pitanja
#   ostale opcije testa (checkbox za MCMA, ...)
#   test report - bodovi
#   ako komentar nije enablean, ...


import wx
import pyTCExam
import pyTCExamConf
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

        # bez always on top
        # wx.Frame.__init__(self, parent=parent, id=wx.NewId(), title='pyTCExam', style=wx.DEFAULT_FRAME_STYLE, size=(1000, 800))

        # configuration
        conf = pyTCExamConf.pyTCExamConf()

        # database object
        self.db = pyTCExamMySQL.DbMySQL(conf.getDbHost(),
                                        conf.getDbPort(),
                                        conf.getDbUser(),
                                        conf.getDbPassword(),
                                        conf.getDbName())

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


    #----------------------------------------------------------------------
    def userLogin(self):
        self.panelLogin.Hide()
        self.panelTestList.Show()
        self.Layout()
        self.panelTestList.refreshTests()


    #----------------------------------------------------------------------
    def userLogoff(self):
        self.panelTestList.Hide()
        self.panelLogin.resetFields()
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
        self.appClose()


    #----------------------------------------------------------------------
    def appClose(self):
        # stop the timer
        self.panelTest.timerCountdown.Stop()
        # destroy the timer
        self.panelTest.timerCountdown.Destroy()
        self.Destroy()


#----------------------------------------------------------------------
class App(wx.App):
    def OnInit(self):
        self.frame = FrameMain(parent=None)
        # full screen
        self.frame.ShowFullScreen(show=True)

        # no full screen
        # self.frame.Center(direction=wx.BOTH)
        # self.frame.Show()

        self.SetTopWindow(frame=self.frame)
        return True
