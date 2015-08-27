#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random
from decimal import *
import pyTCExam
import pyTCExamCommon

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
class Test:

    #----------------------------------------------------------------------
    def __init__(self, db):
        self.__db = db
        self.__testId = 0
        self.__userId = 0
        self._testInfo = {}
        self._testData = []
        self._selectedQuestionId = 0
        self._displayTime = None
        self.__updateQuery = []


    #----------------------------------------------------------------------
    def setSelectedQuestion(self, question_id):
        self._selectedQuestionId = question_id
        self.__updateTestlogDisplayTime()
        self._displayTime = pyTCExamCommon.getCurrentTime()


    #----------------------------------------------------------------------
    def resetUpdateQuery(self):
        self.__updateQuery = []


    #----------------------------------------------------------------------
    def executeUpdateQuery(self):
        for sql, param in self.__updateQuery:
            self.__db.query(sql, param)
        self.resetUpdateQuery()


    #----------------------------------------------------------------------
    def initTest(self, userId, testId):
        self.__userId = userId
        self.__testId = testId
        self.refreshTest()


    #----------------------------------------------------------------------
    def refreshTest(self):
        self._testInfo = self.__getTestInfo()
        self._testData = self.__getTestData()


    #----------------------------------------------------------------------
    def getQuestionsCount(self):
        return len(self._testData)


    #----------------------------------------------------------------------
    def getUserId(self):
        return self.__userId


    #----------------------------------------------------------------------
    def getTestId(self):
        return self.__testId


    #----------------------------------------------------------------------
    def setComment(self, comment):
        sql = "UPDATE "
        sql += pyTCExamCommon.getTableName("TABLE_TEST_USER")
        sql += " SET "
        sql += " testuser_comment = %s"
        sql += " WHERE "
        sql += " testuser_id = %s"
        param = (comment, self._testInfo["testuser_id"])
        self.__updateQuery.append((sql, param))


    #----------------------------------------------------------------------
    def setQuestionData(self, field, value):
        score = self.__calculateScore()
        time = (pyTCExamCommon.getCurrentTime() - self._displayTime)
        reaction = (time.days * 24 * 60 * 60 * 1000) + (time.seconds * 1000) + (time.microseconds / 1000)
        self._testData[self._selectedQuestionId][field] = value
        sql = "UPDATE " + pyTCExamCommon.getTableName("TABLE_TESTS_LOGS")
        sql += " SET"
        sql += " " + field + "=%s,"
        sql += " testlog_score=%s,"
        sql += " testlog_reaction_time=%s"
        sql += " WHERE testlog_id=%s"

        param = (value, score, reaction, self._testData[self._selectedQuestionId]["testlog_id"])
        self.__updateQuery.append((sql, param))


    #----------------------------------------------------------------------
    def setAnswerData(self, field, answer_dict):
        if len(answer_dict):
            for a in self._testData[self._selectedQuestionId]["answers"]:

                sql = "UPDATE " + pyTCExamCommon.getTableName("TABLE_LOG_ANSWER")
                sql += " SET "
                if type(field) is tuple:
                    sql += ",".join([str(f)+"=%s" for f in field])
                else:
                    sql += " " + field + "=%s"
                sql += " WHERE logansw_testlog_id=%s"
                sql += " AND logansw_answer_id=%s"
                if type(field) is tuple:
                    param = answer_dict[a["logansw_answer_id"]] + (self._testData[self._selectedQuestionId]["testlog_id"], a["logansw_answer_id"])
                    for i in range(len(field)):
                        a[field[i]] = answer_dict[a["logansw_answer_id"]][i]
                else:
                    param = (answer_dict[a["logansw_answer_id"]], self._testData[self._selectedQuestionId]["testlog_id"], a["logansw_answer_id"])
                    a[field] = answer_dict[a["logansw_answer_id"]]
                self.__updateQuery.append((sql, param))


    #----------------------------------------------------------------------
    def checkTextAnswer(self, testAnswer, userAnswer):
        testAnswer = testAnswer.strip()
        if userAnswer:
            userAnswer = userAnswer.strip()
        else:
            userAnswer = ""
        if pyTCExamCommon.getConstant("K_SHORT_ANSWERS_BINARY") == True:
            if testAnswer == userAnswer:
                return True
        else:
            if testAnswer.lower() == userAnswer.lower():
                return True

        return False


    #----------------------------------------------------------------------
    def __calculateScore(self):
        questionId = self._selectedQuestionId
        num_answers = 0
        question_type = self._testData[questionId]["question_type"]
        question_score = Decimal(0)
        question_difficulty = Decimal(self._testData[questionId]["question_difficulty"])
        question_right_score = Decimal(self._testInfo["test_score_right"] * question_difficulty)
        question_wrong_score = Decimal(self._testInfo["test_score_wrong"] * question_difficulty)
        question_unanswered_score = Decimal(self._testInfo["test_score_unanswered"] * question_difficulty)

        if question_type == 3:
            if (self._testData[questionId]["testlog_answer_text"] == None or
                len(self._testData[questionId]["testlog_answer_text"]) == 0):
                question_score = question_unanswered_score
            else:
                question_score = question_wrong_score
                for a in self._testData[questionId]["answers"]:
                    if self.checkTextAnswer(a["answer_description"], self._testData[questionId]["testlog_answer_text"]):
                        question_score = question_right_score
                        break
        else:
            for a in self._testData[questionId]["answers"]:
                num_answers += 1
                if question_type == 1:
                    # MCSA
                    if a["logansw_selected"] == -1:
                        question_score = question_unanswered_score
                    elif a["logansw_selected"] == 1:
                        if a["answer_isright"] == 1:
                            question_score = question_right_score
                        else:
                            question_score = question_wrong_score

                elif question_type == 2:
                    # MCMA
                    if a["logansw_selected"] == -1:
                        question_score += question_unanswered_score
                    elif (a["logansw_selected"] == 0 and a["answer_isright"] == 0 or
                          a["logansw_selected"] == 1 and a["answer_isright"] == 1):
                        question_score += question_right_score
                    elif (a["logansw_selected"] == 0 and a["answer_isright"] == 1 or
                          a["logansw_selected"] == 1 and a["answer_isright"] == 0):
                        question_score += question_wrong_score

                elif question_type == 4:
                    # ORDER
                    if a["logansw_selected"] == -1:
                        question_score += question_unanswered_score
                    else:
                        if a["answer_position"] == a["logansw_position"]:
                            question_score += question_right_score
                        else:
                            question_score += question_wrong_score

            if question_type > 1:
                # normalize score
                if self._testInfo["test_mcma_partial_score"]:
                    # use partial scoring for MCMA and ORDER questions
                    question_score = Decimal(round((question_score / num_answers), 3))
                else:
                    # all-or-nothing points
                    if question_score >= (question_right_score * num_answers):
                        # right
                        question_score = question_right_score
                    elif question_score == (question_unanswered_score * num_answers):
                        # unanswered
                        question_score = question_unanswered_score
                    else:
                        # wrong
                        question_score = question_wrong_score

        return question_score


    #----------------------------------------------------------------------
    def __updateTestlogDisplayTime(self):
        if self._testData[self._selectedQuestionId]["testlog_display_time"] == None:
            currentTime = pyTCExamCommon.getCurrentTime()
            sql = "UPDATE " + pyTCExamCommon.getTableName("TABLE_TESTS_LOGS")
            sql += " SET testlog_display_time=%s"
            sql += " WHERE testlog_id=%s"
            param = (currentTime, self._testData[self._selectedQuestionId]["testlog_id"])
            self.__db.query(sql, param)
            self._testData[self._selectedQuestionId]["testlog_display_time"] = currentTime


    #----------------------------------------------------------------------
    def __checkValidTestUser(self):
        """
        /**
         * Check if user is authorized to execute the specified test
         * @param $test_id (int) ID of the selected test
         * @return true if is user is authorized, false otherwise
         */
        """
        sql = "SELECT COUNT(*) AS numrows"
        sql += " FROM " + pyTCExamCommon.getTableName('TABLE_USERGROUP') + ", " + pyTCExamCommon.getTableName('TABLE_TEST_GROUPS')
        sql += " WHERE usrgrp_group_id=tstgrp_group_id"
        sql += " AND tstgrp_test_id=%s"
        sql += " AND usrgrp_user_id=%s"
        sql += " LIMIT 1"
        param = (self.__testId, self.__userId)
        self.__db.query(sql, param)
        row = self.__db.fetchOneRow()
        if len(row) == 1 and row['numrows'] == 1:
            return True

        return False


    #----------------------------------------------------------------------
    def __getTestInfo(self):
        """
        /**
         * Returns the test data.
         * @param $test_id (int) test ID.
         * @return array containing test data.
         */
        """
        # test info
        sql = "SELECT * FROM "
        sql += pyTCExamCommon.getTableName("TABLE_TESTS")
        sql += " WHERE test_id = %s"
        sql += " LIMIT 1"
        param = (self.__testId, )
        self.__db.query(sql, param)
        info = self.__db.fetchOneRow()

        # testcomment
        testUserId = self.__getTestUserId()
        if testUserId:
            sql = "SELECT"
            sql += " testuser_comment,"
            sql += " testuser_creation_time"
            sql += " FROM " + pyTCExamCommon.getTableName("TABLE_TEST_USER")
            sql += " WHERE"
            sql += " testuser_id=%s"
            param = (testUserId, )
            self.__db.query(sql, param)
            row = self.__db.fetchOneRow()
            if row:
                info.update(row)
                info["testuser_id"] = testUserId
                info["testuser_comment"] = row["testuser_comment"]
                info["testuser_creation_time"] = row["testuser_creation_time"]

        return info


    #----------------------------------------------------------------------
    def __getTestData(self):
        testData = []
        sql = "SELECT"
        sql += " testlog_id,"
        sql += " testuser_comment"
        sql += " FROM " + pyTCExamCommon.getTableName("TABLE_TEST_USER")
        sql += " , " + pyTCExamCommon.getTableName("TABLE_TESTS_LOGS")
        sql += " WHERE testlog_testuser_id=testuser_id"
        sql += " AND testuser_test_id=%s"
        sql += " AND testuser_user_id=%s"
        sql += " AND testuser_status<5"
        sql += " ORDER BY testlog_id"

        param = (self.__testId, self.__userId)

        self.__db.query(sql, param)
        rows = self.__db.fetchAllRows()

        for q in rows:
            question = {}
            testlog_id = int(q["testlog_id"])

            # question info
            sql = "SELECT *"
            sql += " FROM " + pyTCExamCommon.getTableName("TABLE_QUESTIONS")
            sql += ", " + pyTCExamCommon.getTableName("TABLE_TESTS_LOGS")
            sql += " WHERE question_id=testlog_question_id"
            sql += " AND testlog_id=%s"
            sql += " LIMIT 1"

            param = (testlog_id, )

            self.__db.query(sql, param)
            row = self.__db.fetchOneRow()

            question.update(row)
            question["answers"] = []

            # answers
            if row["question_type"] == 3:
                sqla = "SELECT *"
                sqla += " FROM " + pyTCExamCommon.getTableName("TABLE_ANSWERS")
                sqla += " , " + pyTCExamCommon.getTableName("TABLE_TESTS_LOGS")
                sqla += " WHERE answer_question_id=testlog_question_id"
                sqla += " AND testlog_id=%s"
            else:
                sqla = "SELECT *"
                sqla += " FROM " + pyTCExamCommon.getTableName("TABLE_ANSWERS")
                sqla += " , " + pyTCExamCommon.getTableName("TABLE_LOG_ANSWER")
                sqla += " WHERE logansw_answer_id=answer_id"
                sqla += " AND logansw_testlog_id=%s"
                sqla += " ORDER BY logansw_order"

            param = (testlog_id, )

            self.__db.query(sqla, param)
            sqla_rows = self.__db.fetchAllRows()

            for a in sqla_rows:
                question["answers"].append(a)

            testData.append(question)

        return testData


    #----------------------------------------------------------------------
    def executeTest(self):
        currentTime = pyTCExamCommon.getCurrentTime()
        sql = "SELECT"
        sql += " test_id,"
        sql += " test_duration_time,"
        sql += " test_repeatable"
        sql += " FROM " + pyTCExamCommon.getTableName("TABLE_TESTS")
        sql += " WHERE test_id=%s"
        sql += " AND test_begin_time < %s"
        sql += " AND test_end_time > %s"
        param = (self.__testId, currentTime, currentTime)
        self.__db.query(sql, param)
        row = self.__db.fetchOneRow()
        if len(row):
            if self.__checkValidTestUser() == True:
                testStatus, testUserId = self.checkTestStatus(self.__userId, self.__testId, row['test_duration_time'])

                if testStatus > 4 and self._testInfo['test_repeatable']:
                    return self.__createTest()

                if testStatus == 0:
                    return self.__createTest()
                elif testStatus == 1 or testStatus == 2 or testStatus == 3:
                    return True
                elif testStatus == 4:
                    return False

        return False


    #----------------------------------------------------------------------
    def repeatTest(self):
        """
        /**
         * Mark previous test attempts as repeated.
         * @param $test_id (int) Test ID
         */
        """
        sql = "SELECT"
        sql += " test_id"
        sql += " FROM " + pyTCExamCommon.getTableName("TABLE_TESTS")
        sql += " WHERE test_id=%s"
        sql += " AND test_repeatable=1"
        sql += " LIMIT 1"
        param = (self.__testId, )
        self.__db.query(sql, param)
        rows = self.__db.fetchAllRows()

        for row in rows:
            sqls = "SELECT"
            sqls += " testuser_id"
            sqls += " FROM " + pyTCExamCommon.getTableName("TABLE_TEST_USER")
            sqls += " WHERE testuser_test_id=%s"
            sqls += " AND testuser_user_id=%s"
            sqls += " AND testuser_status>3"
            sqls += " ORDER BY testuser_status DESC"
            param = (self.__testId, self.__userId)
            self.__db.query(sqls, param)
            rows_s = self.__db.fetchAllRows()
            for row_s in rows_s:
                sqld = "UPDATE "
                sqld += pyTCExamCommon.getTableName("TABLE_TEST_USER")
                sqld += " SET testuser_status=testuser_status+1"
                sqld += " WHERE testuser_id=%s"
                param = (row_s["testuser_id"], )
                self.__db.query(sqld, param)


    #----------------------------------------------------------------------
    def terminateTest(self):
        """
        /**
         * Terminate user's test<br>
         * @param $test_id (int) test ID
         * @since 4.0.000 (2006-09-27)
         */
         """
        sql = "UPDATE " + pyTCExamCommon.getTableName("TABLE_TEST_USER")
        sql += " SET testuser_status=4"
        sql += " WHERE testuser_test_id=%s"
        sql += " AND testuser_user_id=%s"
        sql += " AND testuser_status<4"

        param = (self.__testId, self.__userId)
        self.__db.query(sql, param)


    #----------------------------------------------------------------------
    def __createTest(self):
        """
        /**
         * Create user's test and returns TRUE on success.
         * @param $test_id (int) test ID.
         * @param $user_id (int) user ID.
         * @return boolean TRUE in case of success, FALSE otherwise.
         */
        """
        #todo
        #if self.__checkTestLimits() == True:
        #    return False
        firstTest = 0
        random_questions = self._testInfo['test_random_questions_select'] or self._testInfo['test_random_questions_order']
        sql_answer_position = ""

        if not bool(self._testInfo['test_random_answers_order']) and self._testInfo['test_answers_order_mode'] == 0:
            sql_answer_position = " AND answer_position>0"

        sql_questions_order_by = ""

        if self._testInfo['test_questions_order_mode'] == 0: # position
            sql_questions_order_by = " AND question_position>0 ORDER BY question_position"
        elif self._testInfo['test_questions_order_mode'] == 1: # alphabetic
			sql_questions_order_by = " ORDER BY question_description"
        elif self._testInfo['test_questions_order_mode'] == 2: # ID
            sql_questions_order_by = " ORDER BY question_id"
        elif self._testInfo['test_questions_order_mode'] == 3: # type
            sql_questions_order_by = " ORDER BY question_type"
        elif self._testInfo['test_questions_order_mode'] == 4: # subject ID
            sql_questions_order_by = " ORDER BY question_subject_id"

        # IDs of MCSA questions with more than one correct answer
        right_answers_mcsa_questions_ids = ""
        # IDs of MCSA questions with more than one wrong answer
        wrong_answers_mcsa_questions_ids = []
        # IDs of MCMA questions with more than one answer
        answers_mcma_questions_ids = {}
        # IDs of ORDER questions with more than one ordering answer
        answers_order_questions_ids = ""

        # 1. create user's test entry
        currentDateTime = pyTCExamCommon.getCurrentTime()
        sql = "INSERT INTO " + pyTCExamCommon.getTableName("TABLE_TEST_USER")
        sql += " (testuser_test_id,"
    	sql += " testuser_user_id,"
        sql += " testuser_status,"
        sql += " testuser_creation_time"
        sql += ") VALUES ("
        sql += "%s, %s, 0, %s)"
        param = (self.__testId, self.__userId, currentDateTime)
        self.__db.query(sql, param)

        testuser_id = self.__db.getLastInsertId()

        self.__updateTestuserStat(currentDateTime)

        # get ID of first user's test (if exist)
        firstTest = self.__getFirstTestUser()

        # select questions
        if self._testInfo['test_random_questions_select'] or firstTest == 0:
            ##
            # selected questions IDs
            selected_questions = "0"
            # 2. for each set of subjects
            sql = "SELECT *"
            sql += " FROM " + pyTCExamCommon.getTableName("TABLE_TEST_SUBJSET")
            sql += " WHERE tsubset_test_id=%s"
            sql += " ORDER BY tsubset_type,"
            sql += " tsubset_difficulty,"
            sql += " tsubset_answers DESC"
            param = (self.__testId, )
            self.__db.query(sql, param)
            rows = self.__db.fetchAllRows()
            questions_data = []
            for m in rows:
                # 3. select the subjects IDs
                selected_subjects = "0"
                sql = "SELECT subjset_subject_id"
                sql += " FROM " + pyTCExamCommon.getTableName("TABLE_SUBJECT_SET")
                sql += " WHERE subjset_tsubset_id=%s"
                param = (m["tsubset_id"], )
                self.__db.query(sql, param)
                rows2 = self.__db.fetchAllRows()
                for row2 in rows2:
                    selected_subjects += ", " + str(row2['subjset_subject_id'])

                # 4. select questions
                sqlq = "SELECT question_id,"
                sqlq += " question_type,"
                sqlq += " question_difficulty,"
                sqlq += " question_position"
                sqlq += " FROM " + pyTCExamCommon.getTableName("TABLE_QUESTIONS")
                sqlq += " WHERE question_subject_id IN (" + selected_subjects + ")"
                sqlq += " AND question_difficulty=%s"
                sqlq += " AND question_enabled=1"
                sqlq += " AND question_id NOT IN (" + selected_questions + ")"
                sqlq_param = []
                #sqlq_param.append(selected_subjects)
                sqlq_param.append(m["tsubset_difficulty"])
                #sqlq_param.append(selected_questions)

                if m['tsubset_type'] > 0:
                    sqlq += " AND question_type=%s"
                    sqlq_param.append(m["tsubset_type"])

                if m['tsubset_type'] == 1:
                    # (MCSA : Multiple Choice Single Answer)
                    # get questions with the right number of answers
                    if len(right_answers_mcsa_questions_ids) == 0:
                        right_answers_mcsa_questions_ids = "0"
                        sqlt = "SELECT DISTINCT"
                        sqlt += " answer_question_id"
                        sqlt += " FROM " + pyTCExamCommon.getTableName("TABLE_ANSWERS")
                        sqlt += " WHERE answer_enabled=1"
                        sqlt += " AND answer_isright=1"
                        sqlt += sql_answer_position
                        self.__db.query(sqlt)
                        sqlt_rows = self.__db.fetchAllRows()
                        for mt in sqlt_rows:
                            right_answers_mcsa_questions_ids += ", " + str(mt["answer_question_id"])
                    sqlq += " AND question_id IN (%s)"
                    sqlq_param.append(right_answers_mcsa_questions_ids)

                    if m['tsubset_answers'] > 0:
                        if not wrong_answers_mcsa_questions_ids.has_key(m["tsubset_answers"]):
                            wrong_answers_mcsa_questions_ids[m["tsubset_answers"]] = "0"
                            sqlt = "SELECT answer_question_id"
                            sqlt += " FROM " + pyTCExamCommon.getTableName("TABLE_ANSWERS")
                            sqlt += " WHERE answer_enabled=1"
                            sqlt += " AND answer_isright=0"
                            sqlt += sql_answer_position
                            sqlt += " GROUP BY answer_question_id"
                            sqlt += " HAVING (COUNT(answer_id)>=%s"
                            sqlt_param = (m['tsubset_answers'] - 1, )
                            self.__db.query(sqlt, sqlt_param)
                            sqlt_rows = self.__db.fetchAllRows()
                            for mt in sqlt_rows:
                                wrong_answers_mcsa_questions_ids[m["tsubset_answers"]] += ", " + mt["answer_question_id"]
                        sqlq += " AND question_id IN (%s)"
                        sqlt_param.append(wrong_answers_mcsa_questions_ids[m["tsubset_answers"]])

                elif m['tsubset_type'] == 2:
                    # (MCMA : Multiple Choice Multiple Answers) -------
                    # get questions with the right number of answers
                    if m["tsubset_answers"] > 0:
                        if not answers_mcma_questions_ids.has_key(m["tsubset_answers"]):
                            answers_mcma_questions_ids[m["tsubset_answers"]] = "0"
                            sqlt = "SELECT answer_question_id"
                            sqlt += " FROM " + pyTCExamCommon.getTableName("TABLE_ANSWERS")
                            sqlt += " WHERE answer_enabled=1"
                            sqlt += sql_answer_position
                            sqlt += " GROUP BY answer_question_id HAVING (COUNT(answer_id)>=%s)"
                            sqlt_param = (m['tsubset_answers'], )
                            self.__db.query(sqlt, sqlt_param)
                            sqlt_rows = self.__db.fetchAllRows()
                            for mt in sqlt_rows:
                                answers_mcma_questions_ids[m["tsubset_answers"]] += ", " + mt["answer_question_id"]

                        sqlq += " AND question_id IN (%s)"
                        sqlq_param.append(answers_mcma_questions_ids[m["tsubset_answers"]])

                elif m['tsubset_type'] == 4:
                    # ORDERING ----------------------------------------
                    if len(answers_order_questions_ids):
                        answers_order_questions_ids = "0"
                        sqlt = "SELECT answer_question_id"
                        sqlt += " FROM " + pyTCExamCommon.getTableName("TABLE_ANSWERS")
                        sqlt += " WHERE answer_enabled=1"
                        sqlt += " AND answer_position>0"
                        sqlt += " GROUP BY answer_question_id HAVING (COUNT(answer_id)>1)"
                        self.__db.query(sqlt)
                        sqlt_rows = self.__db.fetchAllRows()
                        for mt in sqlt_rows:
                            answers_order_questions_ids += ", " + str(mt["answer_question_id"])
                    sqlq += " AND question_id IN (%s)"
                    sqlq_param.append(answers_order_questions_ids)

                if random_questions:
                    sqlq += " ORDER BY RAND()"
                else:
                    sqlq += sql_questions_order_by

                sqlq += " LIMIT %s"
                sqlq_param.append(m["tsubset_quantity"])

                self.__db.query(sqlq, tuple(sqlq_param))
                sqlq_rows = self.__db.fetchAllRows()

                for mq in sqlq_rows:
                    # store questions data
                    tmp_data = {}
                    tmp_data["id"] = mq["question_id"]
                    tmp_data["type"] = mq["question_type"]
                    tmp_data["answers"] = m["tsubset_answers"]
                    tmp_data["score"] = (self._testInfo["test_score_unanswered"] * mq["question_difficulty"])
                    tmp_data["question_position"] = mq["question_position"]

                    questions_data.append(tmp_data)
                    selected_questions += ',' + str(mq['question_id'])

                # end while for each set of subjects

            # 5. STORE QUESTIONS AND ANSWERS
            if random_questions:
                random.shuffle(questions_data)
            else:
                questions_data = sorted(questions_data, key=lambda k: k["question_position"])

            # add questions to database
            question_order = 0
            for q in questions_data:
                question_order += 1
                testlog_id = self.__newTestLog(testuser_id, q["id"], q["score"], question_order, q["answers"])
                if not self.__addQuestionAnswers(testlog_id, q["id"], q["type"], q["answers"], firstTest):
                    return False

            # --- end 2
            ##
        else:
            # same questions for all test-takers
            sql = "SELECT *"
            sql += " FROM " + pyTCExamCommon.getTableName("TABLE_TESTS_LOGS")
            sql += ", " + pyTCExamCommon.getTableName("TABLE_QUESTIONS")
            sql += " WHERE question_id=testlog_question_id"
            sql += " AND testlog_testuser_id=%s"
            if self._testInfo["test_random_questions_order"]:
                sql += " ORDER BY RAND()"
            else:
                sql += " ORDER BY testlog_order"

            param = (firstTest, )
            self.__db.query(sql, param)
            rows = self.__db.fetchAllRows()
            question_order = 0;
            for m in rows:
                question_order += 1
                # copy values to new user test
                question_unanswered_score = self._testInfo["test_score_unanswered"] * m['question_difficulty']
                testlog_id = self.__newTestLog(testuser_id, m["testlog_question_id"], question_unanswered_score, question_order, m["testlog_num_answers"])
                # Add answers
                if not self.__addQuestionAnswers(testlog_id, m["question_id"], m["question_type"], m["testlog_num_answers"], firstTest):
                    return False

        # 6. update user's test status as 1 = the test has been successfully created
        sql = "UPDATE " + pyTCExamCommon.getTableName("TABLE_TEST_USER")
        sql += " SET testuser_status=1,"
        sql += " testuser_creation_time=%s"
    	sql += " WHERE testuser_id=%s"
        param = (pyTCExamCommon.getCurrentTime(), testuser_id)
        self.__db.query(sql, param)

        return True

        #                                 ,_-=(!7(7/zs_.
        #                              .='  ' .`/,/!(=)Zm.
        #                .._,,._..  ,-`- `,\ ` -` -`\\7//WW.
        #           ,v=~/.-,-\- -!|V-s.)iT-|s|\-.'   `///mK%.
        #         v!`i!-.e]-g`bT/i(/[=.Z/m)K(YNYi..   /-]i44M.
        #       v`/,`|v]-DvLcfZ/eV/iDLN\D/ZK@%8W[Z..   `/d!Z8m
        #      //,c\(2(X/NYNY8]ZZ/bZd\()/\7WY%WKKW)   -'|(][%4.
        #    ,\\i\c(e)WX@WKKZKDKWMZ8(b5/ZK8]Z7%ffVM,   -.Y!bNMi
        #    /-iit5N)KWG%%8%%%%W8%ZWM(8YZvD)XN(@.  [   \]!/GXW[
        #   / ))G8\NMN%W%%%%%%%%%%8KK@WZKYK*ZG5KMi,-   vi[NZGM[
        #  i\!(44Y8K%8%%%**~YZYZ@%%%%%4KWZ/PKN)ZDZ7   c=//WZK%!
        # ,\v\YtMZW8W%%f`,`.t/bNZZK%%W%%ZXb*K(K5DZ   -c\\/KM48
        # -|c5PbM4DDW%f  v./c\[tMY8W%PMW%D@KW)Gbf   -/(=ZZKM8[
        # 2(N8YXWK85@K   -'c|K4/KKK%@  V%@@WD8e~  .//ct)8ZK%8`       This is a euphemism for how my code is structured.
        # =)b%]Nd)@KM[  !'\cG!iWYK%%|   !M@KZf    -c\))ZDKW%`
        # YYKWZGNM4/Pb  '-VscP4]b@W%     'Mf`   -L\///KM(%W!
        # !KKW4ZK/W7)Z. '/cttbY)DKW%     -`  .',\v)K(5KW%%f          If you're reading this, you have probably been put in charge
        # 'W)KWKZZg)Z2/,!/L(-DYYb54%  ,,`, -\-/v(((KK5WW%f           of maintaining this application.
        #  \M4NDDKZZ(e!/\7vNTtZd)8\Mi!\-,-/i-v((tKNGN%W%%
        #  'M8M88(Zd))///((|D\tDY\\KK-`/-i(=)KtNNN@W%%%@%[           I am so, so sorry for you.
        #   !8%@KW5KKN4///s(\Pd!ROBY8/=2(/4ZdzKD%K%%%M8@%%
        #    '%%%W%dGNtPK(c\/2\[Z(ttNYZ2NZW8W8K%%%%YKM%M%%.          God speed.
        #      *%%W%GW5@/%!e]_tZdY()v)ZXMZW%W%%%*5Y]K%ZK%8[
        #       ‘*%%%%8%8WK\)[/ZmZ/Zi]!/M%%%%@f\ \Y/NNMK%%!
        #         ’VM%%%%W%WN5Z/Gt5/b)((cV@f`  - |cZbMKW%%|
        #            ‘V*M%%%WZ/ZG\t5((+)L\’-,,/  -)X(NWW%%
        #                 `~`MZ/DZGNZG5(((\,    ,t\\Z)KW%@
        #                    ‘M8K%8GN8\5(5///]i!v\K)85W%%f
        #                      YWWKKKKWZ8G54X/GGMeK@WM8%@
        #                       !M8%8%48WG@KWYbW%WWW%%%@
        #                         VM%WKWK%8K%%8WWWW%%%@`
        #                           ~*%%%%%%W%%%%%%%@~
        #                              ~*MM%%%%%%@f`
        #                                  '''''

    def __addQuestionAnswers(self, testlog_id, question_id, question_type, num_answers, firsttest):
        """
        /**
         * Add answers to selected question.
         * @param $testlog_id (int) testlog ID.
         * @param $question_id (int) question ID.
         * @param $question_type (int) type of question.
         * @param $num_answers (int) number of alternative answers to display.
         * @param $firsttest (int) ID of first test testuser_id.
         * @param $testdata (array) array of test data.
         * @return boolean TRUE in case of success, FALSE otherwise.
         */
        """
        if question_type == 3:
            # free text question
            return True

        randorder = self._testInfo["test_random_answers_order"]
        ordmode = self._testInfo["test_answers_order_mode"]

        if self._testInfo["test_random_questions_select"] or self._testInfo["test_random_answers_select"] or firsttest == 0:
            answers_ids = [] # array used to store answers IDs
            if question_type == 1: # MCSA
                # select first right answer
                answers_ids.extend(self.__selectAnswers(question_id, "1", False, 1, 0, randorder, ordmode))

                # select remaining answers
                answers_ids.extend(self.__selectAnswers(question_id, "0", False, (num_answers - 1), 1, randorder, ordmode))

                if ordmode == 1:
                    #reorder answers alphabetically
                    sql = "SELECT answer_id"
                    sql += " FROM " + pyTCExamCommon.getTableName("TABLE_ANSWERS")
                    sql += " WHERE answer_id IN (%s)"
                    sql += " ORDER BY answer_description"
                    param = tuple([x[1] for x in answers_ids])
                    answers_ids = []
                    self.__db.query(sql, param)
                    rows = self.__db.fetchAllRows()
                    index = 0
                    for m in rows:
                        answers_ids.extend((index, m["answer_id"]))
                        index += 1

            elif question_type == 2: # MCMA
                # select answers
                answers_ids.extend(self.__selectAnswers(question_id, "", False, num_answers, 0, randorder, ordmode))

            elif question_type == 4: # ORDERING
                # select answers
                randorder = True
                answers_ids.extend(self.__selectAnswers(question_id, "", True, 0, 0, randorder, ordmode))

            # randomizes the order of the answers
            if randorder:
                random.shuffle(answers_ids)
            else:
                sorted(answers_ids, lambda get_key: getkey[0])

            # add answers
            self.__addLogAnswers(testlog_id, answers_ids)

        else:
            # same answers for all test-takers
            # --------------------------------
            sql = "SELECT logansw_answer_id"
            sql += " FROM " + pyTCExamCommon.getTableName("TABLE_LOG_ANSWER") + ", " + pyTCExamCommon.getTableName("TABLE_TESTS_LOGS")
            sql += " WHERE logansw_testlog_id=testlog_id"
            sql += " AND testlog_testuser_id=%s"
            sql += " AND testlog_question_id=%s"
            if randorder:
                sql += " ORDER BY RAND()"
            else:
                sql += " ORDER BY logansw_order"
            param = (firsttest, question_id)

            self.__db.query(sql, param)
            rows = self.__db.fetchAllRows()
            answers_ids = []
            index = 0
            for m in rows:
                answers_ids.append((index, m["logansw_answer_id"]))
            self.__addLogAnswers(testlog_id, answers_ids)

        return True


    #----------------------------------------------------------------------
    def __selectAnswers(self, question_id, isright="", ordering=False, limit=0, startindex=0, randorder=True, ordmode=0):
        """
        /**
         * Return an array containing answer_id field of selected answers.<br>
         * @param $question_id (int) Question ID.
         * @param $isright (int) Value (0 = false, 1 = true), if non-empty checks for answer_isright value on WHERE clause.
         * @param $ordering (int) Ordering type question (0 = false, 1 = true).
         * @param $limit (int) Maximum number of IDs to return.
         * @param $startindex (int) Array starting index (default = 0).
         * @param $randorder (boolean) If true user random order.
         * @param $ordmode (int) Ordering mode: 0=position; 1=alphabetical; 2=ID.
         * @return array id of selected answers
         */
         """
        answers_ids = [] # stores answers IDs
        sql_param = []
        if ordering:
            randorder = True

        sql_order_by = ""

        if ordmode == 0:
            sql_order_by = " AND answer_position>0 ORDER BY answer_position"
        elif ordmode == 1:
            sql_order_by = " ORDER BY answer_description"
        elif ordmode == 2:
            sql_order_by = " ORDER BY answer_id"

        sql = "SELECT answer_id, answer_position"
        sql += " FROM " + pyTCExamCommon.getTableName("TABLE_ANSWERS")
        sql += " WHERE answer_question_id=%s"
        sql += " AND answer_enabled=1"

        sql_param.append(question_id)

        if ordering:
            sql += " AND answer_position>0"
        elif len(isright) > 0: # MCSA
            sql += " AND answer_isright=%s"
            sql_param.append(isright)

        if randorder:
            sql += " ORDER BY RAND()"
        else:
            sql += sql_order_by

        if limit > 0:
            sql += " LIMIT %s"
            sql_param.append(limit)

        self.__db.query(sql, sql_param)
        rows = self.__db.fetchAllRows()
        for m in rows:
            if randorder or ordmode != 0:
                if ordmode == 2:
                    # order by ID
                    answers_ids.append((m["answer_id"], m["answer_id"]))
                else:
                    # default
                    answers_ids.append((startindex, m["answer_id"]))
                    startindex += 1
            else:
                answers_ids.append(m["answer_position"], m["answer_id"])

        return answers_ids


    #----------------------------------------------------------------------
    def __addLogAnswers(self, testlog_id, answers_ids):
        """
        /**
         * Add specified answers on tce_tests_logs_answer table.
         * @param $testlog_id (int) testlog ID
         * @param $answers_ids (array) array of answer IDs to add
         * @return boolean true in case of success, false otherwise
         */
        """
        i = 0
        for ans_id in answers_ids:
            i += 1
            sql = "INSERT INTO " + pyTCExamCommon.getTableName("TABLE_LOG_ANSWER")
            sql += " (logansw_testlog_id,"
            sql += " logansw_answer_id,"
            sql += " logansw_selected,"
            sql += " logansw_order"
            sql += ") VALUES ("
            sql += "%s, %s, -1, %s)"
            param = (testlog_id, ans_id[1], i)
            self.__db.query(sql, param)

        return True


    #----------------------------------------------------------------------
    def __newTestLog(self, testuser_id, question_id, score, order, num_answers=0):
        """
        /**
         * Creates a new tce_tests_logs table entry and returns inserted ID.
         * @param $testuser_id (int) ID of tce_tests_users
         * @param $question_id (int) question ID
         * @param $score (int) score for unanswered questions
         * @param $order (int) question display order
         * @param $num_answers (int) number of alternative answers
         * @return int testlog ID
         */
        """
        sql = "INSERT INTO " + pyTCExamCommon.getTableName("TABLE_TESTS_LOGS")
        sql += "(testlog_testuser_id,"
        sql += "testlog_question_id,"
        sql += "testlog_score,"
        sql += "testlog_creation_time,"
        sql += "testlog_reaction_time,"
        sql += "testlog_order,"
        sql += "testlog_num_answers"
    	sql += ") VALUES ("
        sql += "%s, %s, %s, %s, 0, %s, %s)"
        param = (testuser_id, question_id, score, pyTCExamCommon.getCurrentTime(), order, num_answers)
        self.__db.query(sql, param)
        return self.__db.getLastInsertId()


    #----------------------------------------------------------------------
    def __getFirstTestUser(self):
        """
        /**
         * Returns the ID of the tce_tests_users table corresponding to a complete test of $test_id type.
         * @param $test_id (int) test ID
         * @return int testuser ID
         */
        """
        sql = "SELECT testuser_id FROM "
        sql += pyTCExamCommon.getTableName("TABLE_TEST_USER")
    	sql += " WHERE testuser_test_id=%s"
        sql += " AND testuser_status>0"
    	sql += " LIMIT 1"
        param = (self.__testId, )
        self.__db.query(sql, param)
        row = self.__db.fetchOneRow()
        if row != None and len(row) == 1:
            return row['testuser_id']

        return 0


    #----------------------------------------------------------------------
    def __updateTestuserStat(self, dateTime):
        """
        /**
         * Track generated tests.
         * @param $date (string) date-time when the test was generated.
         */
        """
        sql = "INSERT INTO "
        sql += pyTCExamCommon.getTableName("TABLE_TESTUSER_STAT")
        sql += " (tus_date) VALUES (%s)"
        param = (dateTime, )
        self.__db.query(sql, param)


    #----------------------------------------------------------------------
    def __getTestUserId(self):
        testUserId = 0
        sql = "SELECT"
        sql += " testuser_id"
        sql += " FROM " + pyTCExamCommon.getTableName("TABLE_TEST_USER")
        sql += " WHERE testuser_test_id = %s"
        sql += " AND testuser_user_id = %s"
        sql += " ORDER BY testuser_status"
        sql += " LIMIT 1"
        param = (self.__testId, self.__userId)
        self.__db.query(sql, param)
        row = self.__db.fetchOneRow()
        if row != None:
            testUserId = int(row['testuser_id'])
        return testUserId


    #----------------------------------------------------------------------
    # static function
    def checkTestStatus(self, userId, testId, duration):
        """
        * @return array of (test_status_code, testuser_id).
        test_status_code:
            0 = the test generation process is started but not completed
            1 = the test has been successfully created
            2 = all questions have been displayed to the user
            3 = all questions have been answered
            4 = test locked (for timeout) - test se zaključao jer nije na vrijeme rješio ispit
            5 or more = old version of repeated test
        """
        currentTime = pyTCExamCommon.getCurrentTime()
        testStatus = 0
        testUserId = 0

        sql = "SELECT testuser_id, testuser_status,"
        sql += " testuser_creation_time FROM "
        sql += pyTCExamCommon.getTableName("TABLE_TEST_USER")
        sql += " WHERE testuser_test_id = %s"
        sql += " AND testuser_user_id = %s"
        sql += " ORDER BY testuser_status"
        sql += " LIMIT 1"
        param = (testId, userId)
        self.__db.query(sql, param)
        row = self.__db.fetchOneRow()
        if row != None:
            testUserId = int(row['testuser_id'])
            testStatus = int(row['testuser_status'])
            endTime = pyTCExamCommon.addSecondsToTime(row['testuser_creation_time'], duration * 60)

            if testStatus > 0 and testStatus < 4 and currentTime > endTime:
                sql = "UPDATE " + pyTCExamCommon.getTableName("TABLE_TEST_USER")
                sql += " SET testuser_status=4"
                sql += " WHERE testuser_id=%s"
                param = (testUserId, )
                self.__db.query(sql, param)
                testStatus = 4
            else:
                if testStatus == 0:
                    sql = "DELETE FROM "
                    sql += pyTCExamCommon.getTableName("TABLE_TEST_USER")
                    sql += " WHERE testuser_id= %s"
                    param = (testUserId, )
                    self.__db.query(sql, param)
                elif testStatus == 1:
                    sql = "SELECT COUNT(testlog_id) FROM "
                    sql += pyTCExamCommon.getTableName("TABLE_TESTS_LOGS")
                    sql += " WHERE testlog_testuser_id=%s"
                    sql += " AND testlog_display_time IS NULL"
                    param = (testUserId, )
                    self.__db.query(sql, param)
                    row = self.__db.fetchOneRow()
                    if int(row['COUNT(testlog_id)']) == 0:
                        sql = "UPDATE "
                        sql += pyTCExamCommon.getTableName("TABLE_TEST_USER")
                        sql += " SET testuser_status=2"
                        sql += " WHERE testuser_id=%s"
                        param = (testUserId, )
                        self.__db.query(sql, param)
                        testStatus = 2
                elif testStatus == 2:
                    sql = "SELECT COUNT(testlog_id) FROM "
                    sql += pyTCExamCommon.getTableName("TABLE_TESTS_LOGS")
                    sql += " WHERE testlog_testuser_id=%s"
                    sql += " AND testlog_change_time IS NULL"
                    param = (testUserId, )
                    self.__db.query(sql, param)
                    row = self.__db.fetchOneRow()
                    if int(row['COUNT(testlog_id)']) == 0:
                        sql = "UPDATE "
                        sql += pyTCExamCommon.getTableName("TABLE_TEST_USER")
                        sql += " SET testuser_status=3"
                        sql += " WHERE testuser_id=%s"
                        param = (testUserId, )
                        self.__db.query(sql, param)
                        testStatus = 3

        return (testStatus, testUserId)
