#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.html as html
import pyTCExam
import pyTCExamCommon
import pyTCExamTest

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
class PanelTestReport(wx.Panel):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.NewId())
        self.__parent = parent

        self.htmlWindowTestReport = html.HtmlWindow(parent=self, id=wx.NewId(), style=html.HW_NO_SELECTION)
        buttonClose = wx.Button(parent=self, id=wx.NewId(), label=u"Zatvori", size=(200, 25))

        vsizer1 = wx.BoxSizer(orient=wx.VERTICAL)
        vsizer1.Add(item=self.htmlWindowTestReport, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        vsizer1.Add(item=buttonClose, proportion=0, flag=wx.LEFT | wx.BOTTOM | wx.RIGHT | wx.ALIGN_CENTER, border=10)

        self.Bind(event=wx.EVT_BUTTON, handler=self.onButtonClose, source=buttonClose)

        self.SetSizer(vsizer1)
        self.Hide()


    #----------------------------------------------------------------------
    def initUi(self, __user, __test):
        created = None
        edited = None
        scoreMsg = ""
        scoreTotal = 0
        scoreMax = __test._testInfo["test_max_score"]
        scoreThreshold = __test._testInfo["test_score_threshold"]
        correctMsg = ""
        correctTotal = 0
        correctMax = len(__test._testData)
        questionOpen = "" # vrijeme kad je pitanje prikazano
        questionEdit = "" # vrijeme kad je pitanje odgovoreno
        questionTimeElapsed = "" # vrijeme proteklo za rješavanje pitanja
        i = 0 # brojač za pitanja
        j = 0 # brojač za odgovore

        if len(__test._testData):
            created = __test._testData[0]["testlog_creation_time"]

        for q in __test._testData:
            if edited == None:
                if q["testlog_change_time"] != None:
                    edited = q["testlog_change_time"]
            else:
                if q["testlog_change_time"] != None and q["testlog_change_time"] > edited:
                    edited = q["testlog_change_time"]
            scoreTotal += q["testlog_score"]
            if q["testlog_score"] == __test._testInfo["test_score_right"]:
                correctTotal += 1

        scoreMsg += str(scoreTotal) + " / " + str(scoreMax) + " (" + str(int((scoreTotal / scoreMax) * 100)) + "%)"

        if scoreTotal > 0:
            if scoreTotal >= scoreThreshold:
                scoreMsg += " - prolaz"
            else:
                scoreMsg += " - pad"

        correctMsg += str(correctTotal) + " / " + str(correctMax) + " (" + str(int((float(correctTotal) / correctMax) * 100)) + "%)"

        if __test._testInfo.has_key("testuser_comment"):
            comment = __test._testInfo["testuser_comment"]
        else:
            comment = ""

        if edited:
            time = edited - created
            h = int(time.seconds / 60**2)
            m = int(time.seconds % 60**2 / 60)
            s = time.seconds % 60
            edited_time = ("%02d:%02d:%02d" % (h, m, s))
        else:
            edited = ""
            edited_time = ""

        out = ''
        out += '<div><font size="+4" color="#003399"><b>Rezultati ispita:</b></font></div>'
        out += '<hr>'
        out += '<div>'

        out += '<table>'

        out += '<tr>'
        out += '<td width=200 align=right>Korisnik:</td>'
        out += '<td>' + __user.getName() + '</td>'
        out += '</tr>'

        out += '<tr>'
        out += '<td align=right>Ispit:</td>'
        out += '<td>' + __test._testInfo["test_name"] + '</td>'
        out += '</tr>'

        out += '<tr>'
        out += '<td align=right></td>'
        out += '<td>' + __test._testInfo["test_description"] + '</td>'
        out += '</tr>'

        out += '<tr>'
        out += u'<td align=right>Početak:</td>'
        out += '<td>' + str(created) + '</td>'
        out += '</tr>'

        out += '<tr>'
        out += '<td align=right>Kraj:</td>'
        out += '<td>' + str(edited) + '</td>'
        out += '</tr>'

        out += '<tr>'
        out += '<td align=right>Trajanje:</td>'
        out += '<td>' + edited_time + '</td>'
        out += '</tr>'

        out += '<tr>'
        out += '<td align=right>Bodovi:</td>'
        out += '<td>' + scoreMsg + '</td>'
        out += '</tr>'

        out += '<tr>'
        out += u'<td align=right>Broj točnih odgovora:</td>'
        out += '<td>' + correctMsg + '</td>'
        out += '</tr>'

        if comment is not None:
            out += '<tr>'
            out += u'<td align=right>Komentar:</td>'
            out += '<td>' + comment + '</td>'
            out += '</tr>'

        out += '<br>'

        if __test._testInfo["test_report_to_users"]:
            i = 1
            for q in __test._testData:
                j = 1

                # div za pitanje + odgovore
                out += '<div>'

                # div za bodove i vrijeme
                out += '<div><b>'
                out += str(i) + ". " # redni broj pitanja
                out += '[' + str(q["testlog_score"]) + ']' # broj bodova

                # vrijeme kad je pitanje prikazano i/ili odgovoreno
                if q["testlog_display_time"] is not None: # ako je pitanje prikazano
                    if q["testlog_change_time"] is not None: # ako je pitanje odgovoreno
                        if q["testlog_display_time"].strftime("%Y-%m-%d") == q["testlog_display_time"].strftime("%Y-%m-%d"): # ako je isti dan i otvoreno i odgovoreno, nije potrebno ispisati datume
                            questionOpen = q["testlog_display_time"].strftime("%H:%M:%S") + " | "
                            questionEdit = q["testlog_change_time"].strftime("%H:%M:%S") + " | "
                        else: # ako nije isti dan i otvoreno i odgovoreno, ispiši i datume
                            questionOpen = q["testlog_display_time"].strftime("%d.%m.%Y. %H:%M:%S") + " | "
                            questionEdit = q["testlog_change_time"].strftime("%d.%m.%Y. %H:%M:%S") + " | "
                        questionTimeElapsed = str(q["testlog_change_time"] - q["testlog_display_time"])
                    else: # pitanje nije odgovoreno, ispiši samo kad je pitanje prikazano
                        questionOpen = q["testlog_display_time"].strftime("%d.%m.%Y. %H:%M:%S")
                        questionEdit = ""
                        questionTimeElapsed = ""
                else: # pitanje nije ni prikazano ni odgovoreno
                    questionOpen = ""
                    questionEdit = ""
                    questionTimeElapsed = ""

                if len(questionOpen + questionEdit + questionTimeElapsed): # ako je pitanje bar prikazano
                    out += " (" + questionOpen + questionEdit + questionTimeElapsed + ")" # ispiši vrijeme/datum

                out += '</b></div>'
                # end div za bodove i vrijeme

                # div za pitanje
                out += '<div>'
                out += pyTCExamCommon.decodeBBCode(q["question_description"])
                out += '</div><br><br>'
                # end div za pitanje

                if q["question_type"] == 1:
                    # MCSA
                    out += '<table border="1" cellspacing="0" cellpadding="5">'
                    for a in q["answers"]:
                        out += '<tr>'
                        out += '<td width="30" height="20" align="right">' + str(j) + '.</td>'

                        # user
                        out += '<td width="25"'
                        # odgovor je točan
                        if a["answer_isright"]:
                            # user ili nije odgovorio (-1) ili je označio neki drugi odgovor (0)
                            if a["logansw_selected"] == 1:
                                out += u'bgcolor="#A0FFA0" align="center"><b>x</b>'
                            else:
                                out += '>'
                        else:
                            # user je označio ovaj odgovor (1)
                            if a["logansw_selected"] == 1:
                                out += u'bgcolor="#FFA0A0" align="center"><b>x</b>'
                            # user nije označio ovaj odgovor (-1 ili 0)
                            else:
                                out += '>'
                        out += '</td>'

                        # test
                        out += '<td width="25"'
                        if a["answer_isright"]:
                            out += u'bgcolor="#ADD8E6" align="center">●'
                        else:
                            out += '>'
                        out += '</td>'

                        out += '<td>' + a["answer_description"] + '</td>'
                        out += '</tr>'
                        j += 1
                    out += '</table>'
                elif q["question_type"] == 2:
                    # MCMA
                    out += '<table border="1" cellspacing="0" cellpadding="5">'
                    for a in q["answers"]:
                        out += '<tr>'
                        out += '<td width="30" height="20" align="right">' + str(j) + '.</td>'

                        # user
                        out += '<td width="25"'
                        # odgovor je točan
                        if a["answer_isright"]:
                            # user nije odabrao ovaj odgovor (0)
                            if a["logansw_selected"] == 0:
                                out += 'bgcolor="#FFA0A0" align="center">'
                            # user ili nije odgovorio (-1) ili je označio neki drugi odgovor (0)
                            elif a["logansw_selected"] == 1:
                                out += 'bgcolor="#A0FFA0" align="center"><b>x</b>'
                            # user nije odgovorio
                            else:
                                out += '>'
                        else:
                            # user je označio ovaj odgovor (1)
                            if a["logansw_selected"] == 1:
                                out += u'bgcolor="#FFA0A0" align="center"><b>x</b>'
                            # user nije označio ovaj odgovor (-1 ili 0)
                            else:
                                out += '>'
                        out += '</td>'

                        # test
                        out += '<td width="25"'
                        if a["answer_isright"]:
                            out += u'bgcolor="#ADD8E6" align="center">●'
                        else:
                            out += '>'
                        out += '</td>'

                        out += '<td>' + a["answer_description"] + '</td>'
                        out += '</tr>'
                        j += 1
                    out += '</table>'

                elif q["question_type"] == 3: # TEXT
                    correct = False
                    answer = ""
                    t = pyTCExamTest.Test(db=None)
                    for a in q["answers"]:
                        answer = a["testlog_answer_text"]
                        if t.checkTextAnswer(a["answer_description"], a["testlog_answer_text"]):
                            correct = True
                            break

                    if answer == None:
                        answer = ""

                    out += '<span'
                    if correct:
                        out += ' style="background-color: #A0FFA0"'
                    else:
                        out += ' style="background-color: #FFA0A0"'
                    out += '>' + answer + '</span>'


                elif q["question_type"] == 4: # ORDER
                    out += '<table border="1" cellspacing="0" cellpadding="5">'
                    for a in q["answers"]:
                        out += '<tr>'
                        out += '<td width="30" height="20" align="right">' + str(j) + '.</td>'

                        # user
                        out += '<td width="25"'
                        if a["logansw_selected"] > 0:
                            # točan odgovor
                            if a["logansw_position"] == a["answer_position"]:
                                out += 'bgcolor="#A0FFA0"'
                            #pogrešan odgovor
                            else:
                                out += 'bgcolor="#FFA0A0"'
                            out += ' align="center">' + str(a["logansw_position"])
                        # bez odgovora
                        else:
                            out += '>'
                        out += '</td>'

                        # test
                        out += '<td width="25" bgcolor="#ADD8E6" align="center">'
                        out += str(a["answer_position"])
                        out += '</td>'


                        out += '</tr>'
                        j += 1

                    out += '</table>'

                # end div za pitanje + odgovore
                out += '</div><br>'

                # povećaj brojač pitanja
                i += 1

            out += '</table>'

            out += '</div><br><br><br>'
            out += '<hr>'
            out += '<div>'
            out += '<b>Legenda:</b><br />'
            out += u'<span style="background-color: #A0FFA0">Zelenom bojom</span> je označen <b>točan</b> odgovor ispitanika.<br />'
            out += u'<span style="background-color: #FFA0A0">Crvenom bojom</span> je označen <b>netočan</b> odgovor ispitanika.<br />'
            out += u'<span style="background-color: #ADD8E6">Plavom bojom</span> je označen točan odgovor.<br />'
            out += '</div>'

        self.htmlWindowTestReport.SetPage(out)


    #----------------------------------------------------------------------
    def onButtonClose(self, event):
        self.__parent.closeReport()
