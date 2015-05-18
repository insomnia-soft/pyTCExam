#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pyTCExamCommon

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
class User(object):

    #----------------------------------------------------------------------
    def __init__(self, db):
        self.id = 0
        self.username = ""
        self.password = ""
        self.firstName = ""
        self.lastName = ""
        self.loginName = ""
        self.db = db

    #----------------------------------------------------------------------
    def userLogin(self, username, password):
        sql = "SELECT"
        sql += " user_id,"
        sql += " user_level,"
        sql += " user_firstname,"
        sql += " user_lastname,"
        sql += " user_name"
        sql += " FROM " + pyTCExamCommon.getTableName("USERS")
        sql += " WHERE user_name=%s"
        sql += " AND user_password=%s"
        param = (username, pyTCExamCommon.getPasswordHash(password))
        self.db.query(sql, param)
        row = self.db.fetchOneRow()
        # login podaci su tocni
        if row != None:
            self.id = int(row['user_id'])
            self.username = username
            self.password = password
            self.firstName = row["user_firstname"]
            self.lastName = row["user_lastname"]
            return True

        return False

    #----------------------------------------------------------------------
    def getName(self):
        out = []
        if self.firstName != None:
            out.append(self.firstName)
        if self.lastName != None:
            out.append(self.lastName)
        out.append("[" + self.username + "]")
        return " ".join(out)