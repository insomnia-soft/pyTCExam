#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# http://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursordict.html

import re
import mysql.connector
from mysql.connector import Error
import pyTCExamCommon

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
class DbMySQL(object):

    #----------------------------------------------------------------------
    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connected = False
        self.connError = ""

        self.__connect()


    #----------------------------------------------------------------------
    def isConnected(self):
        return self.connected


    #----------------------------------------------------------------------
    def getError(self):
        return self.connError


    #----------------------------------------------------------------------
    def __connect(self):
        try:
            self.con = mysql.connector.connect(user=self.username,
                                                password=self.password,
                                                host=self.host,
                                                port=self.port,
                                                database=self.database,
                                                autocommit=True,
                                                charset='utf8')

            if self.con.is_connected():
                self.connected = True

        except Error as e:
            self.connError = str(e)
            self.connected = False


    #----------------------------------------------------------------------
    def query(self, sql, data=()):
        self.cursor = self.con.cursor(dictionary=True)
        self.cursor.execute(sql, params=data)


    #----------------------------------------------------------------------
    def getLastInsertId(self):
        return self.cursor.lastrowid


    #----------------------------------------------------------------------
    def fetchAllRows(self):
        return self.cursor.fetchall()


    #----------------------------------------------------------------------
    def fetchOneRow(self):
        return self.cursor.fetchone()
