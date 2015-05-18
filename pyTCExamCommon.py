#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import md5
import re

"""
tce_config.php postavke:
    define ('K_BRUTE_FORCE_DELAY_RATIO', 2); - mora biti veće od 0
    define ('K_STRONG_PASSWORD_ENCRYPTION', true);
    define ('K_HIDE_EXPIRED_TESTS', false); - false znači da sakrije testove koji su istekli
"""

def getConstant(name):
    if name == "K_SHORT_ANSWERS_BINARY":
        return False

def getTableName(table):
    if table == "USERS":
        return "tce_users"
    elif table == "USER_GROUPS":
        return "tce_usrgroups"
    elif table == "TABLE_TESTS":
        return "tce_tests"
    elif table == "TABLE_TEST_SUBJSET":
        return "tce_test_subject_set"
    elif table == "TABLE_TEST_USER":
        return "tce_tests_users"
    elif table == "TABLE_TESTS_LOGS":
        return "tce_tests_logs"
    elif table == "TABLE_USERGROUP":
        return "tce_usrgroups"
    elif table == "TABLE_TEST_GROUPS":
        return "tce_testgroups"
    elif table == "TABLE_TESTUSER_STAT":
        return "tce_testuser_stat"
    elif table == "TABLE_SUBJECT_SET":
        return "tce_test_subjects"
    elif table == "TABLE_QUESTIONS":
        return "tce_questions"
    elif table == "TABLE_ANSWERS":
        return "tce_answers"
    elif table == "TABLE_LOG_ANSWER":
        return "tce_tests_logs_answers"
    else:
        return ""

def getCurrentTime(formatTime=0):
    if formatTime == 0:
        return datetime.datetime.now()
    else:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

##def getCurrentDate():
##    return datetime.date.today()

##def convertToTime(dbTime):
##    a = dbTime.split(" ")
##    y, mo, d = a[0].split("-")
##    h, mi, s = a[1].split(":")
##    return datetime.datetime(int(y), int(mo), int(d), int(h), int(mi), int(s))

#----------------------------------------------------------------------
def addSecondsToTime(t, sec):
    return t + datetime.timedelta(seconds=sec)


#----------------------------------------------------------------------
def getPasswordHash(password):
    """
    /**
     * Hash password for Database storing.
     * @param $password (string) Password to hash.
     * @return string password hash
     */
    """
    pwLen = len(password)
    salt = pwLen * 2
    for i in range(pwLen):
        salt += ((i + 1) * ord(password[i:i+1]))
    pwHash = "$" + str(salt) + "#" + password[::-1] + "$"
    m = md5.new()
    m.update(pwHash)
    return m.hexdigest()

def getInfoNames():
    return [["test_begin_time", u"Početak:"],
            ["test_end_time", u"Kraj:"],
            ["test_duration_time", u"Trajanje:"],
            ["test_score_right", u"Broj bodova za točan odgovor:"],
            ["test_score_wrong", u"Broj bodova za pogrešan odgovor:"],
            ["test_score_unanswered", u"Broj bodova za nedogovoreno pitanje:"],
            ["test_max_score", u"Maksimalni bodovi:"],
            ["test_score_threshold", u"Broj bodova za prolaz:"],
            ["test_results_to_users", u"Rezultat će biti prikazan polazniku:"],
            ["test_report_to_users", u"Detaljni rezultati će biti prikazani polazniku:"],
            ["test_repeatable", u"Ispit je moguće ponoviti:"]]

#----------------------------------------------------------------------
def decodeBBCode(bbcode):
    bbcode = re.sub("\[b\](.*?)\[/b\]", "<strong>\\1</strong>", bbcode)
    bbcode = re.sub("\[i\](.*?)\[/i\]", "<i>\\1</i>", bbcode)
    bbcode = re.sub("\[u\](.*?)\[/u\]", "<u>\\1</u>", bbcode)
    # ne radi
    # bbcode = re.sub("\[s\](.*?)\[/s\]", "<strike>\\1</strike>", bbcode)
    bbcode = re.sub("\[small\](.*?)\[/small\]", "<small>\\1</small>", bbcode)
    bbcode = re.sub("\[sub\](.*?)\[/sub\]", "<sub>\\1</sub>", bbcode)
    bbcode = re.sub("\[sup\](.*?)\[/sup\]", "<sup>\\1</sup>", bbcode)
    bbcode = re.sub("\[code\](.*?)\[/code\]", "<code>\\1</code>", bbcode)
    bbcode = re.sub("\[img\](.*?)\[/img\]", "<img src=\"\\1\">", bbcode)
    bbcode = re.sub("\\[img=(.*?)x(.*?)\](.*?)\[/img\]", "<img width=\\1 height=\\2 src=\"\\3\">", bbcode)
    bbcode = re.sub("\[url\](.*?)\[/url\]", "\\1", bbcode)
    return bbcode