#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tce_config.php postavke:
    define ('K_BRUTE_FORCE_DELAY_RATIO', 2); - mora biti veće od 0
    define ('K_STRONG_PASSWORD_ENCRYPTION', true);
    define ('K_HIDE_EXPIRED_TESTS', false); - false znači da sakrije testove koji su istekli
"""

class pyTCExamConf(object):

    #----------------------------------------------------------------------
    def __init__(self):
        self.__dbHost = "localhost"             # host na kojem se vrti baza
        self.__dbPort = "3306"                  # port za spajanje na bazu
        self.__dbUser = "root"                  # username za pristup bazi
        self.__dbPassword = "mysqlpassword"     # password za pristup bazi
        self.__dbName = "tcexam"                # ime TCExam baze podataka
        self.__tablePrefix = "tce_"             # prefix tablica
        self.__userLevelForExit = 10            # minimalan level korisnika koji ima dozvolu ugasiti aplikaciju

    #----------------------------------------------------------------------
    def getDbHost(self):
        return self.__dbHost

    #----------------------------------------------------------------------
    def getDbPort(self):
        return self.__dbPort

    #----------------------------------------------------------------------
    def getDbUser(self):
        return self.__dbUser

    #----------------------------------------------------------------------
    def getDbPassword(self):
        return self.__dbPassword

    #----------------------------------------------------------------------
    def getDbName(self):
        return self.__dbName

    #----------------------------------------------------------------------
    def getTablePrefix(self):
        return self.__tablePrefix

    #----------------------------------------------------------------------
    def getUserLevelForExit(self):
        return self.__userLevelForExit