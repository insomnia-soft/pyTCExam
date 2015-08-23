#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import md5
import re
import pyTCExamConf

#----------------------------------------------------------------------
def getConstant(name):
    if name == "K_SHORT_ANSWERS_BINARY":
        return False

#----------------------------------------------------------------------
def getTableName(table):
    conf = pyTCExamConf.pyTCExamConf()
    prefix = conf.getTablePrefix()

    if table == "USERS":
        return prefix + "users"
    elif table == "USER_GROUPS":
        return prefix + "usrgroups"
    elif table == "TABLE_TESTS":
        return prefix + "tests"
    elif table == "TABLE_TEST_SUBJSET":
        return prefix + "test_subject_set"
    elif table == "TABLE_TEST_USER":
        return prefix + "tests_users"
    elif table == "TABLE_TESTS_LOGS":
        return prefix + "tests_logs"
    elif table == "TABLE_USERGROUP":
        return prefix + "usrgroups"
    elif table == "TABLE_TEST_GROUPS":
        return prefix + "testgroups"
    elif table == "TABLE_TESTUSER_STAT":
        return prefix + "testuser_stat"
    elif table == "TABLE_SUBJECT_SET":
        return prefix + "test_subjects"
    elif table == "TABLE_QUESTIONS":
        return prefix + "questions"
    elif table == "TABLE_ANSWERS":
        return prefix + "answers"
    elif table == "TABLE_LOG_ANSWER":
        return prefix + "tests_logs_answers"
    else:
        return ""

#----------------------------------------------------------------------
def getCurrentTime(formatTime=0):
    if formatTime == 0:
        return datetime.datetime.now()
    else:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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

#----------------------------------------------------------------------
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
    # ne radi, bug u html kontroli
    # bbcode = re.sub("\[s\](.*?)\[/s\]", "<strike>\\1</strike>", bbcode)
    bbcode = re.sub("\[small\](.*?)\[/small\]", "<small>\\1</small>", bbcode)
    bbcode = re.sub("\[sub\](.*?)\[/sub\]", "<sub>\\1</sub>", bbcode)
    bbcode = re.sub("\[sup\](.*?)\[/sup\]", "<sup>\\1</sup>", bbcode)
    bbcode = re.sub("\[code\](.*?)\[/code\]", "<code>\\1</code>", bbcode)
    bbcode = re.sub("\[img\](.*?)\[/img\]", "<img src=\"\\1\">", bbcode)
    bbcode = re.sub("\\[img=(.*?)x(.*?)\](.*?)\[/img\]", "<img width=\\1 height=\\2 src=\"\\3\">", bbcode)
    bbcode = re.sub("\[url\](.*?)\[/url\]", "\\1", bbcode)
    return bbcode

#
##	// [dir=ltr]text direction: ltr, rtl[/dir]
##	$pattern[++$i] = "#\[dir=(.*?)\](.*?)\[/dir\]#si";
##	$replacement[++$i] = '<span dir="\1">\2</span>';
##
##	// [align=left]text alignment: left, right, center, justify[/align]
##	$pattern[++$i] = "#\[align=(.*?)\](.*?)\[/align\]#si";
##	$replacement[++$i] = '<span style="text-align:\1;">\2</span>';
##
##	// [code] and [/code] display text as source code
##	$pattern[++$i] = "#\[code\](.*?)\[/code\]#si";
##	$replacement[++$i] = '<div class="tcecodepre">\1</div>';
##
##	// [o] and [/o] for overlined text.
##	$pattern[++$i] = "#\[o\](.*?)\[/o\]#si";
##	$replacement[++$i] = '<span style="text-decoration:overline;">\1</span>';
##
##
##	// [ulist] and [/ulist] unordered list
##	$pattern[++$i] = "#\[ulist\](.*?)\[/ulist\]#si";
##	$replacement[++$i] = '<ul class="tcecode">\1</ul>';
##
##	// [olist] and [/olist] ordered list.
##	$pattern[++$i] = "#\[olist\](.*?)\[/olist\]#si";
##	$replacement[++$i] = '<ol class="tcecode">\1</ol>';
##
##	// [olist=1] and [/olist] ordered list.
##	$pattern[++$i] = "#\[olist=1\](.*?)\[/olist\]#si";
##	$replacement[++$i] = '<ol class="tcecode" style="list-style-type:arabic-numbers">\1</ol>';
##
##	// [olist=a] and [/olist] ordered list.
##	$pattern[++$i] = "#\[olist=a\](.*?)\[/olist\]#si";
##	$replacement[++$i] = '<ol class="tcecode" style="list-style-type:lower-alpha">\1</ol>';
##
##	// [li] list items [/li]
##	$pattern[++$i] = "#\[li\](.*?)\[/li\]#si";
##	$replacement[++$i] = '<li class="tcecode">\1</li>';
##
##	// [color=#RRGGBB] and [/color]
##	// [color=rgb(red,green,blue)] and [/color]
##	// [color=html_color_name] and [/color]
##	$pattern[++$i] = "#\[color=(.*?)\](.*?)\[/color\]#si";
##	$replacement[++$i] = '<span style="color:\1">\2</span>';
##
##	// [bgcolor=#RRGGBB] and [/bgcolor]
##	// [bgcolor=rgb(red,green,blue)] and [/bgcolor]
##	// [bgcolor=html_color_name] and [/bgcolor]
##	$pattern[++$i] = "#\[bgcolor=(.*?)\](.*?)\[/bgcolor\]#si";
##	$replacement[++$i] = '<span style="background-color:\1">\2</span>';
##
##	// [font=value] and [/font]
##	$pattern[++$i] = "#\[font=(.*?)\](.*?)\[/font\]#si";
##	$replacement[++$i] = '<span style="font-family:\1">\2</span>';
##
##	// [size=value] and [/size]
##	// [size=+value] and [/size]
##	// [size=value%] and [/size]
##	$pattern[++$i] = "#\[size=([+\-]?[0-9a-z\-]+[%]?)\](.*?)\[/size\]#si";
##	$replacement[++$i] = '<span style="font-size:\1">\2</span>';
##
##	$newtext = preg_replace($pattern, $replacement, $newtext);
##
##	// line breaks
##	$newtext = preg_replace("'(\r\n|\n|\r)'", '<br />', $newtext);
##	$newtext = str_replace('<br /><li', '<li', $newtext);
##	$newtext = str_replace('</li><br />', '</li>', $newtext);
##	$newtext = str_replace('<br /><param', '<param', $newtext);
##
##	// restore newline chars on [code] tag
##	//$newtext = preg_replace("'@n@'si", "\n",  $newtext);
