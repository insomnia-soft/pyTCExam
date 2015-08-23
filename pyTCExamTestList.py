#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import pyTCExamCommon
import pyTCExamTest

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
class TestList:

    #----------------------------------------------------------------------
    def __init__(self, db):
        self.__db = db
        self.__userId = 0


    #----------------------------------------------------------------------
    def getTestList(self, userId):
        self.__userId = userId
        allTests = {}
        currentTime = pyTCExamCommon.getCurrentTime()

        sql = "SELECT"
        sql += " test_id,"
        sql += " test_duration_time,"
        sql += " test_end_time,"
        sql += " test_results_to_users,"
        sql += " test_name,"
        sql += " test_description,"
        sql += " test_begin_time,"
        sql += " test_score_right,"
        sql += " test_score_wrong,"
        sql += " test_score_unanswered,"
        sql += " test_max_score,"
        sql += " test_score_threshold,"
        sql += " test_report_to_users,"
        sql += " test_password,"
        sql += " test_repeatable"
        sql += " FROM " + pyTCExamCommon.getTableName("TABLE_TESTS")
        sql += " WHERE (test_id IN (SELECT tsubset_test_id"
        sql += " FROM " + pyTCExamCommon.getTableName("TABLE_TEST_SUBJSET")
        sql += ") AND (test_begin_time < %s))"
        sql += " ORDER BY test_begin_time DESC"

        param = (pyTCExamCommon.getCurrentTime(1), )
        self.__db.query(sql, param)
        rows = self.__db.fetchAllRows()

        for row in rows:
            currentTest = {}
            testExpired = False
            testId = int(row['test_id'])
            testDuration = int(row['test_duration_time'])
            testEndTime = row['test_end_time']
            testResultToUser = int(row['test_results_to_users'])

            currentTest['test_name'] = row['test_name']
            currentTest['test_description'] = row['test_description']
            currentTest['test_begin_time'] = row['test_begin_time']
            currentTest['test_end_time'] = row['test_end_time']
            currentTest['test_duration_time'] = row['test_duration_time']
            currentTest['test_score_right'] = row['test_score_right']
            currentTest['test_score_wrong'] = row['test_score_wrong']
            currentTest['test_score_unanswered'] = row['test_score_unanswered']
            currentTest['test_max_score'] = row['test_max_score']
            currentTest['test_score_threshold'] = row['test_score_threshold']
            currentTest['test_results_to_users'] = row['test_results_to_users']
            currentTest['test_report_to_users'] = row['test_report_to_users']
            currentTest['test_repeatable'] = row['test_repeatable']
            currentTest['test_password'] = row['test_password']
            currentTest['status'] = 0
            currentTest['status_msg'] = u"Ispit je omogućen za rješavanje"
            currentTest['status_color'] = 0
            currentTest['expired'] = False
            # TCExam legal values are:
            # 0 = the test generation process is started but not completed;
            # 1 = the test has been successfully created;
            # 2 = all questions have been displayed to the user;
            # 3 = all questions have been answered;
            # 4 = test locked (for timeout);
            t = pyTCExamTest.Test(self.__db)
            testStatus, testUserId = t.checkTestStatus(self.__userId, testId, testDuration)
            currentTest['status'] = testStatus
            if currentTime > testEndTime:
                currentTest['status_color'] = 4
                currentTest['expired'] = True
                currentTest['status_msg'] = u"Rok za rješavanje ispita je istekao"
                testExpired = True

            # status ispita
            if testStatus >= 4 and testResultToUser:
                userTestData = self.__getUserTestStat(testId, self.__userId, testUserId)
                passMsg = ""

                if userTestData.has_key('user_score') and userTestData.has_key('test_score_threshold') and userTestData['test_score_threshold'] > 0:
                    if userTestData['user_score'] >= userTestData['test_score_threshold']:
                        passMsg = " - prolaz"
                        currentTest['status_color'] = 1
                    else:
                        passMsg = " - pad"
                        currentTest['status_color'] = 2

                if userTestData.has_key('user_score'):
                    if userTestData['test_max_score'] > 0:
                        passMsg = str(userTestData['user_score']) + " / " + str(userTestData['test_max_score']) + " (" + str(round((userTestData['user_score'] / userTestData['test_max_score']) * 100, 0)) + ")" + passMsg
                    else:
                        passMsg = str(userTestData['user_score']) + passMsg

                currentTest['status_msg'] = passMsg

            allTests[testId] = currentTest

        return allTests


    #----------------------------------------------------------------------
    def __getUserTestStat(self, testId, userId=0, testUserId=0):
        data = self.__getTestData(testId)
        data.update(self.__getUserTestTotals(testId, userId, testUserId))
        return data

    #----------------------------------------------------------------------
    def __getTestData(self, testId):
        """
        /**
         * Returns the test data.
         * @param $test_id (int) test ID.
         * @return array containing test data.
         */
        """
        sql = "SELECT * FROM "
        sql += pyTCExamCommon.getTableName("TABLE_TESTS")
        sql += " WHERE test_id = %s"
        sql += " LIMIT 1"
        param = (testId, )
        self.__db.query(sql, param)
        row = self.__db.fetchOneRow()
        return row

    #----------------------------------------------------------------------
    def __getUserTestTotals(self, testId, userId=0, testUserId=0):
        """
        /**
        * Returns test-user totals
        * @param $test_id (int) test ID.
        * @param $user_id (int) user ID - if greater than zero, filter stats for the specified user.
        * @param $testuser_id (int) test-user ID - if greater than zero, filter stats for the specified test-user.
        * return $data array containing test-user statistics.
        */
        """
        data = {}
        if testId > 0 and userId > 0 and testUserId > 0:
            sql = "SELECT SUM(testlog_score) AS total_score,"
            sql += " MAX(testlog_change_time) AS test_end_time,"
            sql += " testuser_id,"
            sql += " testuser_creation_time,"
            sql += " testuser_status,"
            sql += " testuser_comment"
            sql += " FROM " + pyTCExamCommon.getTableName("TABLE_TEST_USER")
            sql += " , " + pyTCExamCommon.getTableName("TABLE_TESTS_LOGS")
            sql += " WHERE testlog_testuser_id=testuser_id"
            sql += " AND testuser_id=%s"
            sql += " AND testuser_test_id=%s"
            sql += " AND testuser_user_id=%s"
            sql += " AND testuser_status>0"
            sql += " GROUP BY testuser_id, testuser_creation_time,"
            sql += " testuser_status, testuser_comment"
            param = (testUserId, testId, userId)
            self.__db.query(sql, param)
            row = self.__db.fetchOneRow()
            if row != None:
                data['testuser_id'] = row['testuser_id']
                data['testuser_id'] = row['testuser_id'];
                data['user_score'] = row['total_score'];
                data['user_test_start_time'] = row['testuser_creation_time'];
                data['user_test_end_time'] = row['test_end_time'];
                data['testuser_status'] = row['testuser_status'];
                data['user_comment'] = row['testuser_comment'];

        return data