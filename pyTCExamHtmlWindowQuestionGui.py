#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.html as html
import wx.lib.wxpTag
import pyTCExam
import pyTCExamCommon

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
class HtmlWindowQuestion(html.HtmlWindow):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        html.HtmlWindow.__init__(self, parent=parent, id=wx.NewId(), style=html.HW_NO_SELECTION)
        self.__test = None
        self.__handleEvent = False
        self.answers = {}
        self.__widgetMcsaName = "mcsa_answer_"
        self.__widgetMcmaName = "mcma_answer_"
        self.__widgetTextName = "text_answer"
        self.__widgetOrderName = "order_answer_"

    #----------------------------------------------------------------------
    def setQuestion(self, test):
        self.answers = {}
        self.__test = test
        code = self.__getUi()
        self.SetPage(source=code)
        self.__setAnswersToWidgets()
        self.toggleHandleEvent(True)

    #----------------------------------------------------------------------
    def toggleHandleEvent(self, toggle):
        self.__handleEvent = toggle

    #----------------------------------------------------------------------
    def __getUi(self):
        question_id = self.__test._selectedQuestionId
        test_noanswer_enabled = self.__test._testInfo["test_noanswer_enabled"]
        question_type = self.__test._testData[question_id]["question_type"]
        counter = 1

        code = ''
        code += '<div>' + pyTCExamCommon.decodeBBCode(self.__test._testData[question_id]["question_description"]) + '</div>'
        code += '<hr>'
        if question_type == 1:
            # MCSA - single-answer question
            code += '<table>'
            for a in self.__test._testData[question_id]["answers"]:
                code += '<tr>'
                code += '<td>' + str(counter) + '.</td>'
                code += '<td>'
                code += '<wxp module="wx" class="RadioButton">'
                code += '<param name="name" value="' + self.__widgetMcsaName + str(a["logansw_answer_id"]) + '">'
                code += '</wxp>'
                code += '</td>'
                code += '<td>' + pyTCExamCommon.decodeBBCode(a["answer_description"]) + '</td>'
                code += '</tr>'
                counter += 1

            if test_noanswer_enabled:
                code += '<tr>'
                code += '<td>' + str(counter) + '.</td>'
                code += '<td>'
                code += '<wxp module="wx" class="RadioButton">'
                code += '<param name="name" value="' + self.__widgetMcsaName + '0">'
                code += '</wxp>'
                code += '<td>Bez odgovora</td>'
                code += '</td>'
                code += '</tr>'
            code += '<table>'

            self.Bind(wx.EVT_RADIOBUTTON, self.onRadioBox)

        elif question_type == 2:
            # MCMA - multiple-answer question
            if self.__test._testInfo["test_mcma_radio"]:
                # radio button
                code += '<table>'
                code += '<tr>'
                if test_noanswer_enabled:
                    code += u'<td width="80" align="center"><font color="#A0A0A0"><b>Bez odgovora</b></font></td>'
                code += u'<td width="80" align="center"><font color="#FF0000"><b>Netočno</b></font></td>'
                code += u'<td width="80" align="center"><font color="#008000"><b>Točno</b></font></td>'
                code += '</tr>'

                for a in self.__test._testData[question_id]["answers"]:
                    code += '<tr>'
                    code += '<td>' + str(counter) + '.</td>'
                    if test_noanswer_enabled:
                        code += '<td align="center">'
                        code += '<wxp module="wx" class="RadioButton">'
                        code += '<param name="name" value="' + self.__widgetMcmaName + str(a["logansw_answer_id"]) + '_0">'
                        code += '<param name="style" value="wx.RB_GROUP">'
                        code += '</wxp>'
                        code += '</td>'

                    code += '<td align="center">'
                    code += '<wxp module="wx" class="RadioButton">'
                    code += '<param name="name" value="' + self.__widgetMcmaName + str(a["logansw_answer_id"]) + '_1">'
                    if not test_noanswer_enabled:
                        code += '<param name="style" value="wx.RB_GROUP">'
                    code += '</wxp>'
                    code += '</td>'

                    code += '<td align="center">'
                    code += '<wxp module="wx" class="RadioButton">'
                    code += '<param name="name" value="' + self.__widgetMcmaName + str(a["logansw_answer_id"]) + '_2">'
                    code += '</wxp>'
                    code += '</td>'

                    code += '<td>' + pyTCExamCommon.decodeBBCode(a["answer_description"]) + '</td>'
                    code += '</tr>'
                    counter += 1
                code += '</table>'

                self.Bind(wx.EVT_RADIOBUTTON, self.onRadioBox)
            else:
                # checkbox
                code += '<table>'

                for a in self.__test._testData[question_id]["answers"]:
                    code += '<tr>'
                    code += '<td>' + str(counter) + '.</td>'
                    code += '<td>'
                    code += '<wxp module="wx" class="CheckBox">'
                    code += '<param name="name" value="' + self.__widgetMcmaName + str(a["logansw_answer_id"]) + '">'
                    code += '</wxp>'
                    code += '</td>'
                    code += '<td>' + pyTCExamCommon.decodeBBCode(a["answer_description"]) + '</td>'
                    code += '</tr>'
                    counter += 1

                code += '</table>'
                self.Bind(wx.EVT_CHECKBOX, self.onCheckBox)

        elif question_type == 3:
            # TEXT - free text question
            code += '<wxp module="wx" class="TextCtrl" height=200 width=100%>'
            code += '<param name="style" value="wx.TE_MULTILINE">'
            code += '<param name="name" value="' + self.__widgetTextName + '">'
            code += '</wxp><br /><br />'

            self.Bind(wx.EVT_TEXT, self.onTextInput)

        elif question_type == 4:
            # ORDER - ordering questions
            choices = []
            if test_noanswer_enabled:
                choices.append(' ')
            choices.extend(["{0}".format(x) for x in range(1, len(self.__test._testData[question_id]["answers"]) + 1)])

            if len(self.__test._testData[question_id]["answers"]):
                code += '<table>'
                for a in self.__test._testData[question_id]["answers"]:
                    code += '<tr>'
                    code += '<td>' + str(counter) + '.</td>'
                    code += '<td>'
                    code += '<wxp module="wx" class="StaticText">'
                    code += "<param name='label' value='" + a["answer_description"] + "'>"
                    code += '</wxp>'
                    code += '</td><td>'
                    code += '<wxp module="wx" class="ComboBox">'
                    code += '<param name="style" value="wx.CB_READONLY">'
                    code += '<param name="choices" value="' + str(choices) + '">'
                    code += '<param name="name" value="' + self.__widgetOrderName + str(a["logansw_answer_id"]) + '">'
                    code += '</wxp>'
                    code += '</td></tr>'
                    counter += 1
                code += '<table>'

            self.Bind(wx.EVT_COMBOBOX, self.onComboBox)

        return code

    #----------------------------------------------------------------------
    def __setAnswersToWidgets(self):
        question_id = self.__test._selectedQuestionId
        question_type = self.__test._testData[question_id]["question_type"]
        test_noanswer_enabled = self.__test._testInfo["test_noanswer_enabled"]

        answered = False
        if self.__test._testData[question_id]["testlog_change_time"] != None:
            answered = True

        if question_type == 1:
            # MCSA - single-answer question
            for a in self.__test._testData[question_id]["answers"]:
                # odabran odgovor
                if a["logansw_selected"] == 1:
                    name = self.__widgetMcsaName + str(a["logansw_answer_id"])
                    self.__setWidgetValue(name, True)

            if test_noanswer_enabled and answered == False:
                self.__setWidgetValue(self.__widgetMcsaName + "0", True)

        elif question_type == 2:
			# MCMA - multiple-answer question
            for a in self.__test._testData[question_id]["answers"]:
                status = a["logansw_selected"]
                if self.__test._testInfo["test_mcma_radio"]:
                    name = self.__widgetMcmaName + str(a["logansw_answer_id"]) + "_" + str(status + 1)
                    self.__setWidgetValue(name, True)
                else:
                    name = self.__widgetMcmaName + str(a["logansw_answer_id"])
                    if status == 1:
                        self.__setWidgetValue(name, True)

        elif question_type == 3:
            # TEXT - free text question
            a = self.__test._testData[question_id]
            if a["testlog_answer_text"] != None:
                self.__setWidgetValue(self.__widgetTextName, a["testlog_answer_text"])

        elif question_type == 4:
            # ORDER - ordering questions
            #if self.__test._testData[question_id]["testlog_change_time"] != None:
            for a in self.__test._testData[question_id]["answers"]:
                name = self.__widgetOrderName + str(a["logansw_answer_id"])
                self.__setWidgetValue(name, str(a["logansw_position"]))

    #----------------------------------------------------------------------
    def __setWidgetValue(self, name, value):
        widget = wx.FindWindowByName(name)
        if widget != None:
            widget.SetValue(value)

    #----------------------------------------------------------------------
    def __getWidgetValue(self, name):
        widget = wx.FindWindowByName(name)
        if widget != None:
            return widget.GetValue()
        return None

    #----------------------------------------------------------------------
    def onCheckBox(self, event):
        if self.__handleEvent == True:
            question_id = self.__test._selectedQuestionId
            question_type = self.__test._testData[question_id]["question_type"]
            answers = {}
            time = pyTCExamCommon.getCurrentTime()

            tmp = event.GetEventObject().GetName().split("_")
            selectedAnswerIndex = int(tmp[2])

            for a in self.__test._testData[question_id]["answers"]:
                name = self.__widgetMcmaName + str(a["logansw_answer_id"])
                value = self.__getWidgetValue(name)
                answers[a["logansw_answer_id"]] = 1 if value == True else 0

            self.__test.setAnswerData(field="logansw_selected", answer_dict=answers)
            self.__test.setQuestionData(field="testlog_change_time", value=time)

    #----------------------------------------------------------------------
    def onRadioBox(self, event):
        if self.__handleEvent == True:
            question_id = self.__test._selectedQuestionId
            question_type = self.__test._testData[question_id]["question_type"]
            test_noanswer_enabled = self.__test._testInfo["test_noanswer_enabled"]
            answers = {}

            if question_type == 1:
                # MCSA
                tmp = event.GetEventObject().GetName().split("_")
                selectedAnswerIndex = int(tmp[2])
                time = None
                if selectedAnswerIndex > 0:
                    time = pyTCExamCommon.getCurrentTime()
                    for a in self.__test._testData[question_id]["answers"]:
                        answers[a["logansw_answer_id"]] = 0
                    answers[selectedAnswerIndex] = 1
                else:
                    for a in self.__test._testData[question_id]["answers"]:
                        answers[a["logansw_answer_id"]] = -1

                self.__test.resetUpdateQuery()
                self.__test.setAnswerData(field="logansw_selected", answer_dict=answers)
                self.__test.setQuestionData(field="testlog_change_time", value=time)

            elif question_type == 2:
                # MCMA
                tmp = event.GetEventObject().GetName().split("_")
                value = int(tmp[3]) - 1
                selectedAnswerIndex = int(tmp[2])
                time = None
                #time = pyTCExamCommon.getCurrentTime()
                for a in self.__test._testData[question_id]["answers"]:
                    for i in range(3):
                        name = self.__widgetMcmaName + str(a["logansw_answer_id"]) + "_" + str(i)
                        if self.__getWidgetValue(name) == True:
                            value = i - 1
                            break
                    answers[a["logansw_answer_id"]] = value
                    if value > -1:
                        time = pyTCExamCommon.getCurrentTime()

                self.__test.resetUpdateQuery()
                self.__test.setAnswerData(field="logansw_selected", answer_dict=answers)
                self.__test.setQuestionData(field="testlog_change_time", value=time)

    #----------------------------------------------------------------------
    def onTextInput(self, event):
        if self.__handleEvent == True:
            if event.GetEventObject().GetName() == self.__widgetTextName:
                time = None
                text = self.__getWidgetValue(self.__widgetTextName)
                if len(text):
                    time = pyTCExamCommon.getCurrentTime()

                self.__test.resetUpdateQuery()
                self.__test.setQuestionData(field="testlog_answer_text", value=text)
                self.__test.setQuestionData(field="testlog_change_time", value=time)

    #----------------------------------------------------------------------
    def onComboBox(self, event):
        if self.__handleEvent == True:
            question_id = self.__test._selectedQuestionId
            question_type = self.__test._testData[question_id]["question_type"]
            answers = {}
            if question_type == 4:
                time = None
                for a in self.__test._testData[question_id]["answers"]:
                    field = []
                    name = self.__widgetOrderName + str(a["logansw_answer_id"])
                    value = self.__getWidgetValue(name)
                    if value == "" or value == " ":
                        value = -1
                    else:
                        value = int(value)
                    field = ("logansw_selected", "logansw_position")
                    if value == -1:
                        answers[a["logansw_answer_id"]] = (-1, 0)
                    else:
                        answers[a["logansw_answer_id"]] = (1, value)

                    if value > -1:
                        time = pyTCExamCommon.getCurrentTime()

                self.__test.resetUpdateQuery()
                self.__test.setAnswerData(field=field, answer_dict=answers)
                self.__test.setQuestionData(field="testlog_change_time", value=time)

    #----------------------------------------------------------------------
    def unbind(self):
        self.Unbind(wx.EVT_RADIOBUTTON)
        self.Unbind(wx.EVT_TEXT)
