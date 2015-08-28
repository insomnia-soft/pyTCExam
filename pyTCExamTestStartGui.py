#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import pyTCExamCommon

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
class PanelTestStart(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent, testObject):
        wx.Panel.__init__(self, parent=parent, id=wx.NewId())
        self.__testObject = testObject
        self.__testInfo = {}

        # definiranje stilova teksta
        fontNormal = wx.Font(pointSize=10, family=wx.SWISS, style=wx.NORMAL, weight=wx.NORMAL)
        fontBold = wx.Font(pointSize=10, family=wx.SWISS, style=wx.NORMAL, weight=wx.BOLD)

        self.infoTextNames = pyTCExamCommon.getInfoNames()

        fgsizer1 = wx.FlexGridSizer(rows=11, cols=2, vgap=2, hgap=5)

        # naziv ispita
        self.staticTextTestName = wx.StaticText(parent=self, id=-1)
        self.staticTextTestName.SetFont(wx.Font(pointSize=16, family=wx.SWISS, style=wx.NORMAL, weight=wx.BOLD))
        self.staticTextTestName.SetForegroundColour("#003399")

        # opis ispita
        self.staticTextTestDescription = wx.StaticText(parent=self)
        self.staticTextTestDescription.SetFont(fontNormal)
        self.staticTextTestDescription.SetBackgroundColour("#E0E0E0")

        self.infoStaticText = {}

        for name in self.infoTextNames:
            tmp = wx.StaticText(parent=self, id=-1, size=(300, -1), style=wx.ALIGN_RIGHT, label=name[1])
            tmp.SetFont(fontNormal)
            self.infoStaticText[name[0]] = wx.StaticText(parent=self, id=-1)
            self.infoStaticText[name[0]].SetFont(fontBold)
            fgsizer1.Add(tmp)
            fgsizer1.Add(self.infoStaticText[name[0]])

        buttonContinue = wx.Button(parent=self, id=wx.NewId(), label="&Kreni")
        buttonCancel = wx.Button(parent=self, id=wx.NewId(), label="&Odustani")

        # password + message
        self.staticTextPassword = wx.StaticText(parent=self, id=wx.NewId(), label="Lozinka:")
        self.textCtrlPassword = wx.TextCtrl(parent=self, id=wx.NewId(), style=wx.TE_PASSWORD)
        self.staticTextMessage = wx.StaticText(parent=self, id=wx.NewId(), style=wx.ALIGN_CENTER)
        self.staticTextMessage.SetForegroundColour("#FF0000")

        # sizer for password & message
        hsizer1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        hsizer1.Add(item=self.staticTextPassword, proportion=0, flag=wx.TOP | wx.RIGHT, border=3)
        hsizer1.Add(item=self.textCtrlPassword, proportion=1, flag=wx.EXPAND)

        # sizer for buttons
        hsizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)
        hsizer2.Add(item=(-1, -1), proportion=1)
        hsizer2.Add(item=buttonContinue)
        hsizer2.Add(item=(-1, -1), proportion=1)
        hsizer2.Add(item=buttonCancel)
        hsizer2.Add(item=(-1, -1), proportion=1)

        # info o ispitu
        sbvsizer1 = wx.StaticBoxSizer(box=wx.StaticBox(parent=self, id=wx.NewId(), label=u"Informacije o odabranom ispitu"), orient=wx.VERTICAL)
        sbvsizer1.SetMinSize(size=(350, -1))

        sbvsizer1.Add(self.staticTextTestName, 0, wx.EXPAND | wx.ALL, 5)
        sbvsizer1.Add(self.staticTextTestDescription, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        sbvsizer1.Add(fgsizer1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        sbvsizer1.Add(hsizer1, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=5)
        sbvsizer1.Add(self.staticTextMessage, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=5)
        sbvsizer1.Add(hsizer2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)

        gsizer1 = wx.GridSizer(1, 1, 0, 0)
        gsizer1.Add(sbvsizer1, 1, wx.ALIGN_CENTER)
        self.SetSizer(gsizer1)

        self.Hide()

        self.Bind(wx.EVT_BUTTON, self.__onButtonContinue, buttonContinue)
        self.Bind(wx.EVT_BUTTON, self.__onButtonCancel, buttonCancel)


    #----------------------------------------------------------------------
    def loadTestData(self):
        self.staticTextTestName.SetLabel(self.__testObject._testInfo['test_name'])
        self.staticTextTestDescription.SetLabel(self.__testObject._testInfo['test_description'])
        for name in pyTCExamCommon.getInfoNames():
            txt = ""
            if (name[0] == "test_results_to_users" or
                name[0] == "test_report_to_users" or
                name[0] == "test_repeatable"):
                if self.__testObject._testInfo[name[0]] == 1:
                    txt = "da"
                else:
                    txt = "ne"
            elif name[0] == "test_begin_time" or name[0] == "test_end_time":
                txt = self.__testObject._testInfo[name[0]].strftime("%d.%m.%Y. %H:%M:%S")
            else:
                txt = str(self.__testObject._testInfo[name[0]])
            self.infoStaticText[name[0]].SetLabel(txt)

        if self.__testObject._testInfo['test_password'] is None:
            self.staticTextPassword.Hide()
            self.textCtrlPassword.Hide()
        else:
            self.staticTextPassword.Show()
            self.textCtrlPassword.Show()
        self.staticTextMessage.Hide() # show only when user enters wrong password
        self.Layout()


    #----------------------------------------------------------------------
    def __onButtonContinue(self, event):
        if self.__testObject._testInfo['test_password'] is None: # user does not need to type password to start test
            self.__startTest()
        else: # user needs to type password to start test
            password = self.textCtrlPassword.GetValue()
            if pyTCExamCommon.getPasswordHash(password) == self.__testObject._testInfo['test_password']:
                self.__startTest()
            else:
                msg = u"Lozinka je pogrešna!"
                self.staticTextMessage.SetLabel(label=msg)
                self.staticTextMessage.Show()
                self.Layout()


    #----------------------------------------------------------------------
    def __onButtonCancel(self, event):
        self.GetParent().initTestCancel()


    #----------------------------------------------------------------------
    def __startTest(self):
        if self.__testObject.executeTest():
            self.GetParent().startTest()