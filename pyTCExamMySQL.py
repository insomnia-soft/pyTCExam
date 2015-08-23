#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursordict.html

import re
import mysql.connector
from mysql.connector import Error
import pyTCExamCommon

class DbMySQL(object):
    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.__connect()

    def __connect(self):
        try:
            self.con = mysql.connector.connect(user=self.username,
                                                password=self.password,
                                                host=self.host,
                                                port=self.port,
                                                database=self.database,
                                                autocommit=True,
                                                charset='utf8')

            if not self.con.is_connected():
                return 1

        except Error as e:
            print e
            return 1

        return 0

    def query(self, sql, data=()):
        self.cursor = self.con.cursor(dictionary=True)
        self.cursor.execute(sql, params=data)

    def getLastInsertId(self):
        return self.cursor.lastrowid

    def fetchAllRows(self):
        return self.cursor.fetchall()

    def fetchOneRow(self):
        return self.cursor.fetchone()

    def stripSlashes(self, s):
        r = re.sub(r"\\(n|r)", "\n", s)
        r = re.sub(r"\\", "", r)
        return r
