#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.lib.buttons as buttons
import datetime
import pyTCExam
import pyTCExamApp
import pyTCExamTest
import pyTCExamCommon
import pyTCExamHtmlWindowQuestionGui as question_gui

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
class WindowTimer(wx.Window):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Window.__init__(self, parent=parent, id=wx.NewId(), size=(400, -1))
        self.Bind(event=wx.EVT_PAINT, handler=self.__onPaint)
        self.__text = ""


    #----------------------------------------------------------------------
    def __onPaint(self, event):
        dc = wx.BufferedPaintDC(window=self)
        self.__drawTime(dc)


    #----------------------------------------------------------------------
    def __drawTime(self, dc):
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))
        dc.SetTextForeground("#FF0000")
        w, h = dc.GetSize()
        tw, th = dc.GetTextExtent(self.__text)
        dc.DrawText(self.__text, w-tw, 0)


    #----------------------------------------------------------------------
    def drawTime(self, text):
        dc = wx.BufferedDC(wx.ClientDC(win=self))
        self.__text = text
        self.__drawTime(dc)


    #----------------------------------------------------------------------
    def getText(self):
        return self.__text


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
class PanelTest(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent, testObject):
        wx.Panel.__init__(self, parent=parent, id=wx.NewId())
        self.__parent = parent
        self.__test = testObject
        self.__lastButtonClick = 0
        self.__questionButton = {}
        self.__questionButtonCount = 0

        # not displayed, displayed, with answer
        self.__colorArray = ["#FFA0A0", "#FFFFA0", "#A0FFA0"]
        fontBlue = wx.Font(pointSize=16, family=wx.SWISS, style=wx.NORMAL, weight=wx.BOLD)

        vsizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        sbsizer5 = wx.StaticBoxSizer(box=wx.StaticBox(parent=self, id=wx.NewId(), label=u"Ispit" ), orient=wx.HORIZONTAL)
        self.staticTextTestTitle = wx.StaticText(parent=self, id=wx.NewId())
        self.staticTextTestTitle.SetForegroundColour("#003399")
        self.staticTextTestTitle.SetFont(fontBlue)
        self.windowTimerCountdown = WindowTimer(self)
        sbsizer5.Add(item=self.staticTextTestTitle, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        sbsizer5.Add(item=self.windowTimerCountdown, proportion=0, flag=wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, border=5)
        vsizer1.Add(item=sbsizer5, proportion=0, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        hsizer1 = wx.BoxSizer(orient=wx.HORIZONTAL)

        sbsizer1 = wx.StaticBoxSizer(box=wx.StaticBox(parent=self, id=wx.NewId(), label=u"Pitanja" ), orient=wx.HORIZONTAL)

        self.scrolledWindow = wx.ScrolledWindow(parent=self, id=wx.NewId(), size=(280, -1), style=wx.VSCROLL)
        self.scrolledWindow.SetScrollRate(xstep=5, ystep=5)

        self.fgsizer1 = wx.FlexGridSizer(rows=0, cols=5, vgap=5, hgap=5)

        hsizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)
        hsizer2.Add(item=(-1, -1), proportion=1)
        hsizer2.Add(item=self.fgsizer1)
        hsizer2.Add(item=(-1, -1), proportion=1)

        self.scrolledWindow.SetSizer(sizer=hsizer2)
        sbsizer1.Add(item=self.scrolledWindow, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        self.htmlWindow = question_gui.HtmlWindowQuestion(parent=self)

        sbsizer2 = wx.StaticBoxSizer(box=wx.StaticBox(parent=self, id=wx.NewId(), label=u"Odabrano pitanje"), orient=wx.VERTICAL)
        sbsizer2.Add(item=self.htmlWindow, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.buttonPrevQuestion = wx.Button(parent=self, id=wx.NewId(), label=u"<< Prethodno pitanje", size=(160, 25))
        self.buttonConfirmAnswer = wx.Button(parent=self, id=wx.NewId(), label=u"Potvrdi odgovor", size=(160, 25))
        self.buttonNextQuestion = wx.Button(parent=self, id=wx.NewId(), label=u"Slijedeće pitanje >>", size=(160, 25))
        buttonTerminateExam = wx.Button(parent=self, id=wx.NewId(), label=u"Završi ispit", size=(160, 25))
        buttonBackToTestList = wx.Button(parent=self, id=wx.NewId(), label=u"Povratak na popis ispita", size=(160, 25))

        sbsizer3 = wx.StaticBoxSizer(box=wx.StaticBox(parent=self, id=wx.NewId(), label=u"Navigacija"), orient=wx.HORIZONTAL)
        sbsizer3.Add(item=self.buttonPrevQuestion, flag=wx.ALL, border=5)
        sbsizer3.Add(item=(20, -1))
        sbsizer3.Add(item=self.buttonConfirmAnswer, flag=wx.ALL, border=5)
        sbsizer3.Add(item=(20, -1))
        sbsizer3.Add(item=self.buttonNextQuestion, flag=wx.ALL, border=5)
        sbsizer3.Add(item=(-1, -1), proportion=1, flag=wx.EXPAND)
        sbsizer3.Add(item=buttonTerminateExam, flag=wx.ALL, border=5)
        sbsizer3.Add(item=(20, -1))
        sbsizer3.Add(item=buttonBackToTestList, flag=wx.ALL, border=5)

        self.textCtrlComment = wx.TextCtrl(parent=self, id=wx.NewId(), size=(-1, 150), style=wx.TE_MULTILINE)
        self.sbsizer4 = wx.StaticBoxSizer(box=wx.StaticBox(parent=self, id=wx.NewId(), label=u"Komentar"), orient=wx.VERTICAL)
        self.sbsizer4.Add(self.textCtrlComment, 1, wx.EXPAND)

        self.vsizer2 = wx.BoxSizer(orient=wx.VERTICAL)
        self.vsizer2.Add(item=sbsizer2, proportion=1, flag=wx.EXPAND)
        self.vsizer2.Add(item=sbsizer3, proportion=0, flag=wx.EXPAND)
        self.vsizer2.Add(item=self.sbsizer4, proportion=0, flag=wx.EXPAND)

        hsizer1.Add(item=sbsizer1, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        hsizer1.Add(item=self.vsizer2, proportion=1, flag=wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, border=10)

        vsizer1.Add(item=hsizer1, proportion=1, flag=wx.EXPAND)

        self.SetSizer(sizer=vsizer1)

        self.timerCountdown = wx.Timer(owner=self, id=wx.NewId())

        self.Bind(event=wx.EVT_BUTTON, handler=self.__onPrevQuestion, source=self.buttonPrevQuestion)
        self.Bind(event=wx.EVT_BUTTON, handler=self.__onConfirmAnswer, source=self.buttonConfirmAnswer)
        self.Bind(event=wx.EVT_BUTTON, handler=self.__onNextQuestion, source=self.buttonNextQuestion)
        self.Bind(event=wx.EVT_BUTTON, handler=self.__onTerminateExam, source=buttonTerminateExam)
        self.Bind(event=wx.EVT_BUTTON, handler=self.__onBackToTestList, source=buttonBackToTestList)
        self.Bind(event=wx.EVT_TIMER, handler=self.__onTimer, source=self.timerCountdown)

        self.Hide()


    #----------------------------------------------------------------------
    def onToggleButton(self, event):
        self.htmlWindow.toggleHandleEvent(False)
        name = event.GetEventObject().GetName()
        if name[:9] == "question_":
            buttonId = int(name[9:])
            self.__selectQuestion(buttonId)
        event.Skip()


    #----------------------------------------------------------------------
    def __enableButtons(self):
        question_id = self.__test._selectedQuestionId
        question_order = self.__test._testData[question_id]["testlog_order"]
        question_count = self.__test.getQuestionsCount()
        if question_order == 1:
            self.buttonPrevQuestion.Disable()
            self.buttonNextQuestion.Enable()
        elif question_order == question_count:
            self.buttonPrevQuestion.Enable()
            self.buttonNextQuestion.Disable()
        else:
            self.buttonPrevQuestion.Enable()
            self.buttonNextQuestion.Enable()

        self.buttonNextQuestion.SetFocus()


    #----------------------------------------------------------------------
    def initUi(self):
        # set test name
        self.staticTextTestTitle.SetLabel(self.__test._testInfo["test_name"])
        # comment
        if self.__test._testInfo["test_comment_enabled"]:
            self.vsizer2.Show(item=self.sbsizer4)
            comment = self.__test._testInfo["testuser_comment"]
            if comment:
                self.textCtrlComment.SetValue(comment)
        else:
            self.vsizer2.Hide(item=self.sbsizer4)
        # set remaining time
        self.__setRemainingTime()
        # start timer
        self.timerCountdown.Start(100)
        # add buttons
        self.__addQuestionsButtons()
        # if there are questions
        if self.__test.getQuestionsCount() > 0:
            # select first question
            self.__selectQuestion(1)

        self.Layout()


    #----------------------------------------------------------------------
    def __addQuestionsButtons(self):
        self.__resetQuestionsButtons()
        # for each question
        for t in self.__test._testData:
            # increase toggle button counter
            self.__questionButtonCount += 1
            # make toggle button data
            label = "%s" %  self.__questionButtonCount
            name = "question_%s" % self.__questionButtonCount
            # add toggle button
            self.__questionButton[self.__questionButtonCount] = buttons.GenToggleButton(self.scrolledWindow, id=wx.NewId(), label=label, name=name, size=(45, 30))
            # add toggle button to flex grid sizer
            self.fgsizer1.Add(item=self.__questionButton[self.__questionButtonCount])
            # toggle button background color
            self.__paintButton(self.__questionButtonCount - 1)
            # add event handler
            self.Bind(wx.EVT_BUTTON, self.onToggleButton, self.__questionButton[self.__questionButtonCount])


    #----------------------------------------------------------------------
    def __resetQuestionsButtons(self):
        for i in range(self.__questionButtonCount, 0, -1):
            self.fgsizer1.Hide(self.__questionButtonCount - 1)
            self.fgsizer1.Remove(self.__questionButtonCount - 1)
            self.__questionButtonCount -= 1
        # reset buttons dictionary
        self.__questionButton = {}
        # reset toggle button counter
        self.__questionButtonCount = 0
        self.__lastButtonClick = 0


    #----------------------------------------------------------------------
    def __selectQuestion(self, question_number):
        question_id = question_number - 1
        if question_number != self.__lastButtonClick:
            self.__confirmAnswer()

            if self.__lastButtonClick > 0:
                self.__questionButton[self.__lastButtonClick].SetValue(False)
                self.__questionButton[self.__lastButtonClick].Enabled = True

            self.__lastButtonClick = question_number
            self.__questionButton[question_number].Enabled = False
            self.__questionButton[question_number].SetValue(True)

            self.__test.setSelectedQuestion(question_id)
            self.htmlWindow.unbind()
            self.htmlWindow.setQuestion(self.__test)
            self.__paintButton()
            self.__enableButtons()


    #----------------------------------------------------------------------
    def __confirmAnswer(self):
        self.__test.setComment(self.textCtrlComment.GetValue())
        self.__test.executeUpdateQuery()
        self.__paintButton()


    #----------------------------------------------------------------------
    def __terminateExam(self):
        dlg = wx.MessageDialog(parent=self, message=u"Potvrdite kraj ispita.", caption=u"Ispit", style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = dlg.ShowModal()
        if ret == wx.ID_YES:
            self.__confirmAnswer()
            self.timerCountdown.Stop()
            self.__test.terminateTest()
            self.__parent.terminateTest()


    #----------------------------------------------------------------------
    def __paintButton(self, unselected_id = -1):
        if unselected_id == -1:
            button_id = self.__test._selectedQuestionId
        else:
            button_id = unselected_id
        color_id = 0
        if self.__test._testData[button_id]["testlog_display_time"] == None:
            color_id = 0
        else:
            if self.__test._testData[button_id]["testlog_change_time"] == None:
                color_id = 1
            else:
                color_id = 2

        if self.__questionButton[button_id + 1].Enabled == False:
            self.__questionButton[button_id + 1].Enabled = True
            self.__questionButton[button_id + 1].SetBackgroundColour(self.__colorArray[color_id])
            self.__questionButton[button_id + 1].Enabled = False
        else:
            self.__questionButton[button_id + 1].SetBackgroundColour(self.__colorArray[color_id])


    #----------------------------------------------------------------------
    def __onConfirmAnswer(self, event):
        self.__confirmAnswer()
        event.Skip()


    #----------------------------------------------------------------------
    def __onPrevQuestion(self, event):
        question_id = self.__test._selectedQuestionId
        self.__selectQuestion(question_id)
        event.Skip()


    #----------------------------------------------------------------------
    def __onNextQuestion(self, event):
        question_id = self.__test._selectedQuestionId
        self.__selectQuestion(question_id + 2)
        event.Skip()


    #----------------------------------------------------------------------
    def __onTerminateExam(self, event):
        self.__terminateExam()
        event.Skip()


    #----------------------------------------------------------------------
    def __onBackToTestList(self, event):
        self.__confirmAnswer()
        self.timerCountdown.Stop()
        self.__parent.terminateTest()
        event.Skip()


    #----------------------------------------------------------------------
    def __onTimer(self, event):
        self.__setRemainingTime()


    #----------------------------------------------------------------------
    def __setRemainingTime(self):
        end = self.__test._testInfo["test_end_time"]
        current = pyTCExamCommon.getCurrentTime()
        diff = end - current
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time = "%02d:%02d:%02d" % (hours, minutes, seconds)
        if diff.days > 0:
            time = str(diff.days) + "d " + time

        if current > end:
            self.timerCountdown.Stop()
            wx.MessageBox(message="Vrijeme je isteklo!", caption=u"Ispit", style=wx.ICON_EXCLAMATION)
            self.__terminateExam()
        else:
            old = self.windowTimerCountdown.getText()
            if time != old:
                self.windowTimerCountdown.drawTime(time)