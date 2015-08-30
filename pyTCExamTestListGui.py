#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import pyTCExamTestList
import pyTCExamTest
import pyTCExamCommon
import pyTCExam

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
class PanelTestList(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent, db, user):
        wx.Panel.__init__(self, parent=parent, id=wx.NewId())
        self.__parent = parent
        self.__db = db
        self.__user = user
        self.__testsObject = pyTCExamTestList.TestList(self.__db)
        self.selectedTestId = 0

        # dictionary sa testovima i osnovnim informacijama o testovima
        self.__tests = {}

        # definiranje stilova teksta
        fontNormal = wx.Font(pointSize=10, family=wx.SWISS, style=wx.NORMAL, weight=wx.NORMAL)
        fontBold = wx.Font(pointSize=10, family=wx.SWISS, style=wx.NORMAL, weight=wx.BOLD)

        # ListCtrl sa popisom ispita
        self.listCtrlTests = wx.ListCtrl(parent=self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES)
        self.listCtrlTests.InsertColumn(col=0, heading="Ispit", width=300)
        self.listCtrlTests.InsertColumn(col=1, heading="Od")
        self.listCtrlTests.InsertColumn(col=2, heading="Do")
        self.listCtrlTests.InsertColumn(col=3, heading="Status")

        # gumb refresh tests
        buttonRefreshTests = wx.Button(parent=self, id=wx.NewId(), label="Dohvati ispite", size=(200, 25))

        sbvsizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.NewId(), label="Popis ispita"), wx.VERTICAL)
        sbvsizer1.Add(self.listCtrlTests, 1, wx.EXPAND | wx.ALL, 5)
        sbvsizer1.Add(buttonRefreshTests, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)

        # naziv ispita
        self.staticTextTestName = wx.StaticText(parent=self, id=-1)
        self.staticTextTestName.SetFont(wx.Font(pointSize=16, family=wx.SWISS, style=wx.NORMAL, weight=wx.BOLD))
        self.staticTextTestName.SetForegroundColour("#003399")

        # opis ispita
        self.staticTextTestDescription = wx.StaticText(parent=self)
        self.staticTextTestDescription.SetFont(fontNormal)
        self.staticTextTestDescription.SetForegroundColour("#003399")

        fgsizer1 = wx.FlexGridSizer(rows=11, cols=2, vgap=2, hgap=5)

        self.infoTextNames = pyTCExamCommon.getInfoNames()

        self.infoStaticText = {}

        for name in self.infoTextNames:
            tmp = wx.StaticText(parent=self, id=-1, size=(300, -1), style=wx.ALIGN_RIGHT, label=name[1])
            tmp.SetFont(fontNormal)
            self.infoStaticText[name[0]] = wx.StaticText(parent=self, id=-1)
            self.infoStaticText[name[0]].SetFont(fontBold)
            fgsizer1.Add(tmp)
            fgsizer1.Add(self.infoStaticText[name[0]])

        fgsizer1.AddGrowableCol(1, 1)

        # info o ispitu
        sbvsizer2 = wx.StaticBoxSizer(wx.StaticBox(self, -1, u"Informacije o odabranom ispitu"), wx.VERTICAL)
        sbvsizer2.Add(self.staticTextTestName, 0, wx.EXPAND | wx.ALL, 5)
        sbvsizer2.Add(self.staticTextTestDescription, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        sbvsizer2.Add(fgsizer1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)

        # opcije korisnika
        sbvsizer3 = wx.StaticBoxSizer(wx.StaticBox(parent=self, id=wx.NewId(), label="Opcije"), wx.VERTICAL)

        self.buttonExecuteTest = wx.Button(parent=self, id=wx.NewId(), label=u"Započni s rješavanjem", size=(200, 25))
        self.buttonContinueTest = wx.Button(parent=self, id=wx.NewId(), label=u"Nastavi s rješavanjem ispita", size=(200, 25))
        self.buttonRepeatTest = wx.Button(parent=self, id=wx.NewId(), label=u"Ponovi ispit", size=(200, 25))
        self.buttonTestReport = wx.Button(parent=self, id=wx.NewId(), label=u"Prikaži rezultat", size=(200, 25))
        self.buttonLogoff = wx.Button(parent=self, id=wx.NewId(), label=u"Odjava", size=(200, 25))

        sbvsizer3.Add(item=self.buttonExecuteTest, proportion=0, flag=wx.ALL, border=5)
        sbvsizer3.Add(item=self.buttonContinueTest, proportion=0, flag=wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        sbvsizer3.Add(item=self.buttonRepeatTest, proportion=0, flag=wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        sbvsizer3.Add(item=self.buttonTestReport, proportion=0, flag=wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
        sbvsizer3.Add(item=self.buttonLogoff, proportion=0, flag=wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)

        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add(sbvsizer2, 1, wx.EXPAND | wx.ALL, 10)
        hsizer1.Add(sbvsizer3, 0, wx.EXPAND | wx.ALL, 10)

        vsizerMain = wx.BoxSizer(wx.VERTICAL)
        vsizerMain.Add(sbvsizer1, 1, wx.EXPAND | wx.ALL, 10)
        vsizerMain.Add(hsizer1, 0, wx.EXPAND)
        self.SetSizer(vsizerMain)
        self.Hide()

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.__onSelectTest, self.listCtrlTests)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.__onDeselectTest, self.listCtrlTests)
        self.Bind(wx.EVT_LIST_DELETE_ALL_ITEMS, self.__onClearTestList)
        self.Bind(wx.EVT_BUTTON, self.__onButtonRefreshTests, buttonRefreshTests)
        self.Bind(wx.EVT_BUTTON, self.__onButtonExecuteTest, self.buttonExecuteTest)
        self.Bind(wx.EVT_BUTTON, self.__onButtonContinueTest, self.buttonContinueTest)
        self.Bind(wx.EVT_BUTTON, self.__onButtonRepeatTest, self.buttonRepeatTest)
        self.Bind(wx.EVT_BUTTON, self.__onButtonTestReport, self.buttonTestReport)
        self.Bind(wx.EVT_BUTTON, self.__onButtonLogoff, self.buttonLogoff)


    #----------------------------------------------------------------------
    def __onButtonRefreshTests(self, event):
        self.refreshTests()


    #----------------------------------------------------------------------
    def refreshTests(self):
        self.listCtrlTests.DeleteAllItems()
        self.__resetInfoWidgets()
        self.__tests = self.__testsObject.getTestList(self.__user.id)
        colors = ["#FFFFA0", "#A0FFA0", "#FFA0A0", "#A0FFA0", "#E0E0E0"]

        index = 0
        for testId in self.__tests:
            self.listCtrlTests.InsertStringItem(index, self.__tests[testId]['test_name'])
            self.listCtrlTests.SetStringItem(index, 1, self.__tests[testId]['test_begin_time'].strftime("%d.%m.%Y. %H:%M:%S"))
            self.listCtrlTests.SetStringItem(index, 2, self.__tests[testId]['test_end_time'].strftime("%d.%m.%Y. %H:%M:%S"))
            self.listCtrlTests.SetStringItem(index, 3, self.__tests[testId]['status_msg'])
            self.listCtrlTests.SetItemBackgroundColour(index, colors[self.__tests[testId]['status_color']])
            self.listCtrlTests.SetItemData(item=index, data=testId)
            index += 1
        self.listCtrlTests.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.listCtrlTests.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.listCtrlTests.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER) # zadnja kolona popunjava sav slobodan prostor


    #----------------------------------------------------------------------
    def __resetInfoWidgets(self):
        self.staticTextTestName.SetLabel("")
        self.staticTextTestDescription.SetLabel("")
        for name in self.infoTextNames:
            self.infoStaticText[name[0]].SetLabel("")
        self.buttonExecuteTest.Disable()
        self.buttonContinueTest.Disable()
        self.buttonRepeatTest.Disable()
        self.buttonTestReport.Disable()


    #----------------------------------------------------------------------
    def __onSelectTest(self, event):
        self.selectedTestId = event.GetItem().GetData()
        self.staticTextTestName.SetLabel(self.__tests[self.selectedTestId]['test_name'])
        self.staticTextTestDescription.SetLabel(self.__tests[self.selectedTestId]['test_description'])
        self.buttonExecuteTest.Disable()
        self.buttonContinueTest.Disable()
        self.buttonRepeatTest.Disable()
        if self.__tests[self.selectedTestId]['expired'] == False:
            if self.__tests[self.selectedTestId]['status'] == 0:
                self.buttonExecuteTest.Enable()
            elif self.__tests[self.selectedTestId]['status'] == 1 or self.__tests[self.selectedTestId]['status'] == 2 or self.__tests[self.selectedTestId]['status'] == 3:
                self.buttonContinueTest.Enable()
            elif self.__tests[self.selectedTestId]['status'] >= 4 and self.__tests[self.selectedTestId]['test_repeatable'] == 1:
                self.buttonRepeatTest.Enable()

        # if
        if self.__tests[self.selectedTestId]["status"] >= 4 and self.__tests[self.selectedTestId]['test_results_to_users']:
            self.buttonTestReport.Enable()

        for name in self.infoTextNames:
            if (name[0] == "test_results_to_users" or
                name[0] == "test_report_to_users" or
                name[0] == "test_repeatable"):
                if self.__tests[self.selectedTestId][name[0]] == 1:
                    self.infoStaticText[name[0]].SetLabel("da")
                else:
                    self.infoStaticText[name[0]].SetLabel("ne")
            elif name[0] == "test_begin_time" or name[0] == "test_end_time":
                self.infoStaticText[name[0]].SetLabel(self.__tests[self.selectedTestId][name[0]].strftime("%d.%m.%Y. %H:%M:%S"))
            else:
                self.infoStaticText[name[0]].SetLabel(str(self.__tests[self.selectedTestId][name[0]]))


    #----------------------------------------------------------------------
    def __onDeselectTest(self, event):
        self.__resetInfoWidgets()
        self.selectedTestId = 0
        event.Skip()


    #----------------------------------------------------------------------
    def __onClearTestList(self, event):
        self.__resetInfoWidgets()
        self.selectedTestId = 0
        event.Skip()


    #----------------------------------------------------------------------
    def __onButtonLogoff(self, event):
        self.__parent.userLogoff()
        event.Skip()


    #----------------------------------------------------------------------
    def __onButtonExecuteTest(self, event):
        self.__parent.initTest()
        event.Skip()


    #----------------------------------------------------------------------
    def __onButtonContinueTest(self, event):
        self.__parent.continueTest()
        event.Skip()


    #----------------------------------------------------------------------
    def __onButtonRepeatTest(self, event):
        self.__parent.repeatTest()
        event.Skip()


    #----------------------------------------------------------------------
    def __onButtonTestReport(self, event):
        self.__parent.showReport()
        event.Skip()
