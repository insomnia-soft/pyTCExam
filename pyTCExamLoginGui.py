#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import pyTCExamConf
import pyTCExamTestList

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
class PanelLogin(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent, db, user):
        wx.Panel.__init__(self, parent=parent, id=wx.NewId())

        conf = pyTCExamConf.pyTCExamConf()

        self.__parent = parent
        self.__db = db
        self.__user = user
        self.__userLevelForExit = conf.getUserLevelForExit()

        loginUsernameLabel = wx.StaticText(parent=self, id=wx.NewId(), size=(100, -1), label=u"Korisničko ime:", style=wx.ALIGN_RIGHT)
        self.textCtrlUsername = wx.TextCtrl(parent=self, id=wx.NewId(), size=(150, -1))
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add(loginUsernameLabel, 0, wx.TOP, 3)
        hsizer1.Add(self.textCtrlUsername, 0, wx.LEFT, 5)

        loginPasswordLabel = wx.StaticText(parent=self, id=-1, size=(100, -1), label="Lozinka:", style=wx.ALIGN_RIGHT)
        self.textCtrlPassword = wx.TextCtrl(parent=self, id=-1, size=(150, -1), style=wx.TE_PASSWORD)
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2.Add(loginPasswordLabel, 0, wx.TOP, 3)
        hsizer2.Add(self.textCtrlPassword, 0, wx.LEFT, 5)

        buttonLogin = wx.Button(parent=self, id=wx.NewId(), size=(120, 28), label="&Prijava")
        buttonExit = wx.Button(parent=self, id=wx.NewId(), size=(120, 28), label="&Izlaz")
        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer3.Add(buttonLogin, 0, wx.EXPAND | wx.ALL, 3)
        hsizer3.Add((-1, -1), 1, wx.EXPAND)
        hsizer3.Add(buttonExit, 0, wx.EXPAND | wx.ALL, 3)

        sbvsizer1 = wx.StaticBoxSizer(wx.StaticBox(self, -1, label="Prijava korisnika"), wx.VERTICAL)
        sbvsizer1.Add(hsizer1, 0, wx.ALL, 4)
        sbvsizer1.Add(hsizer2, 0, wx.ALL, 4)
        sbvsizer1.Add(hsizer3, 0, wx.ALL | wx.EXPAND, 4)

        gsizer1 = wx.GridSizer(1, 1, 0, 0)
        gsizer1.Add(sbvsizer1, 1, wx.ALIGN_CENTER)
        self.SetSizer(gsizer1)

        self.Bind(wx.EVT_BUTTON, self.__onClickLogin, buttonLogin)
        self.Bind(wx.EVT_BUTTON, self.__onClickExit, buttonExit)


    #----------------------------------------------------------------------
    def __userLogin(self, reportError=True):
        msg = ""
        username = self.textCtrlUsername.GetValue()
        password = self.textCtrlPassword.GetValue()

        if len(username) == 0 or len(password) == 0:
            msg = u"Potrebno je upisati korisničko ime i lozinku za prijavu!"
        elif self.__user.userLogin(username, password) == False:
            msg = u"Prijava neuspješna!"

        if len(msg):
            if reportError == True:
                wx.MessageBox(message=msg, caption=u"Prijava korisnika", style=wx.OK | wx.ICON_ERROR)
            return False
        else:
            return True


    #----------------------------------------------------------------------
    def __onClickLogin(self, event):
        if self.__userLogin() == True:
            self.GetParent().userLogin()


    #----------------------------------------------------------------------
    def __isAdmin(self):
        if self.__userLogin(False) == True and self.__userLevelForExit >= self.__user.getUserLevel():
            return True
        else:
            wx.MessageBox(message=u"Nemate privilegiju ugasiti aplikaciju!", caption=u"Izlaz", style=wx.OK | wx.ICON_ERROR)
            return False


    #----------------------------------------------------------------------
    def __onClickExit(self, event):
        if self.__isAdmin() == True:
            self.GetParent().appClose()
