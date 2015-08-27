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
        self.__parent = parent

        # definiranje stilova teksta
        fontNormal = wx.Font(pointSize=11, family=wx.SWISS, style=wx.NORMAL, weight=wx.NORMAL)
        fontBold = wx.Font(pointSize=11, family=wx.SWISS, style=wx.NORMAL, weight=wx.BOLD)

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
            tmp = wx.StaticText(parent=self, id=-1, size=(150, -1), style=wx.ALIGN_RIGHT, label=name[1])
            tmp.SetFont(fontNormal)
            self.infoStaticText[name[0]] = wx.StaticText(parent=self, id=-1)
            self.infoStaticText[name[0]].SetFont(fontBold)
            fgsizer1.Add(tmp)
            fgsizer1.Add(self.infoStaticText[name[0]])

        buttonContinue = wx.Button(parent=self, id=wx.NewId(), label="&Kreni")
        buttonCancel = wx.Button(parent=self, id=wx.NewId(), label="&Odustani")

        hsizer1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        hsizer1.Add(item=(-1, -1), proportion=1)
        hsizer1.Add(item=buttonContinue)
        hsizer1.Add(item=(-1, -1), proportion=1)
        hsizer1.Add(item=buttonCancel)
        hsizer1.Add(item=(-1, -1), proportion=1)

        # info o ispitu
        sbvsizer1 = wx.StaticBoxSizer(box=wx.StaticBox(parent=self, id=wx.NewId(), label=u"Informacije o odabranom ispitu"), orient=wx.VERTICAL)
        sbvsizer1.SetMinSize(size=(350, -1))

        sbvsizer1.Add(self.staticTextTestName, 0, wx.EXPAND | wx.ALL, 5)
        sbvsizer1.Add(self.staticTextTestDescription, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        sbvsizer1.Add(fgsizer1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        sbvsizer1.Add(hsizer1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)

        gsizer1 = wx.GridSizer(1, 1, 0, 0)
        gsizer1.Add(sbvsizer1, 1, wx.ALIGN_CENTER)
        self.SetSizer(gsizer1)

        self.Hide()

        self.Bind(wx.EVT_BUTTON, self.__onButtonContinue, buttonContinue)
        self.Bind(wx.EVT_BUTTON, self.__onButtonCancel, buttonCancel)

    #----------------------------------------------------------------------
    def loadTestData(self):
        self.__testInfo = self.__testObject.getTestInfo()

        self.staticTextTestName.SetLabel(str(self.__testInfo['test_name']))
        self.staticTextTestDescription.SetLabel(str(self.__testInfo['test_description']))
        for name in pyTCExamCommon.getInfoNames():
            self.infoStaticText[name[0]].SetLabel(str(self.__testInfo[name[0]]))

    #----------------------------------------------------------------------
    def __onButtonContinue(self, event):
        if self.__testInfo['test_password'] != None:
            dlgGetPw = wx.PasswordEntryDialog(self, u'Upiši lozinku za pristup ispitu:', u'Ispit', "")
            ret = dlgGetPw.ShowModal()
            dlgGetPw.Destroy()

            if ret == wx.ID_OK:
                if pyTCExamCommon.getPasswordHash(dlgGetPw.GetValue()) == self.__testInfo['test_password']:
                    self.__startTest()
                else:
                    wx.MessageBox(message=u"Pristup ispitu nije dozvoljen!", caption=u"Ispit", style=wx.OK | wx.ICON_ERROR)
        else:
            self.__startTest()

    #----------------------------------------------------------------------
    def __onButtonCancel(self, event):
        self.__parent.endTest()

    #----------------------------------------------------------------------
    def __startTest(self):
        self.__testObject.executeTest()