

class DbQueryProject:
    def __init__(self):
        import sys

        reload(sys)
        sys.setdefaultencoding('utf8')

        import sqlite3
        import matplotlib.pyplot as plt
        import numpy as np
        import operator

        self.operator=operator
        self.plt=plt
        self.np=np

        connection = sqlite3.connect('Gerrit.db')
        connection.text_factory = str
        self.cursor = connection.cursor()

    '''
    year=2017
    cursor.execute("SELECT DISTINCT reviewData from ReviewTable JOIN ChangeTable ON ReviewTable.change_id=ChangeTable.change_id "
                   "WHERE project_name='iotivity' and STRFTIME('%Y',review_Date)=?",([year.__str__()]))
    '''


    def getEligibleReviewerList(self,projectName, reviewNo=10):
        self.cursor.execute(
            "SELECT DISTINCT R1.reviewer FROM ReviewTable R1 JOIN ChangeTable C ON R1.change_id=C.change_id "
            "WHERE C.project_name=? AND ?<=(SELECT COUNT(R2.review_id) FROM ReviewTable R2 "
             "WHERE R2.reviewer=R1.reviewer)", ([projectName, reviewNo]))

        data = self.cursor.fetchall()
        eligibleReviewerList = []
        for d in data:
            reviewer = d[0].lower()
            if (reviewer.startswith("jenkin") or reviewer.endswith("jenkin")
                or reviewer.startswith("jenkins") or reviewer.endswith("jenkins")
                or reviewer.startswith("gerrit") or reviewer.endswith("gerrit")):
                continue

            eligibleReviewerList.append(d[0])
        eligibleReviewer = len(eligibleReviewerList)
        # print(eligibleReviewer)
        return eligibleReviewer, eligibleReviewerList

    def getIndividualTotal(self,projectName, reviewer):
        self.cursor.execute(
            "SELECT COUNT(review_id) FROM ReviewTable JOIN ChangeTable ON ReviewTable.change_id=ChangeTable.change_id "
            "WHERE project_name=? AND reviewer=?", ([projectName, reviewer]))
        data = self.cursor.fetchall()
        # print(data[0][0],reviewer)
        return data[0][0]

    def getIndividualUseful(self,projectName, reviewer):
        self.cursor.execute(
            "SELECT COUNT(review_id) FROM ReviewTable JOIN ChangeTable ON ReviewTable.change_id=ChangeTable.change_id "
            "WHERE project_name=? AND reviewer=? AND (usefulness='A' OR usefulness='B')", ([projectName, reviewer]))
        data = self.cursor.fetchall()
        # print(data[0][0],reviewer)
        return data[0][0]

    def getAnnualTotal(self,projectName):
        self.cursor.execute(
            "SELECT DISTINCT COUNT(review_id) FROM ReviewTable R1 JOIN ChangeTable C ON R1.change_id=C.change_id "
            "WHERE C.project_name=?", ([projectName]))

        data = self.cursor.fetchall()
        # print(data[0][0],reviewer)
        return data[0][0]

    def getAnnualUseful(self,projectName):
        self.cursor.execute(
            "SELECT DISTINCT COUNT(review_id) FROM ReviewTable R1 JOIN ChangeTable C ON R1.change_id=C.change_id "
            "WHERE C.project_name=? AND (usefulness='A' OR usefulness='B')", ([projectName]))

        data = self.cursor.fetchall()
        # print(data[0][0],reviewer)
        return data[0][0]

    def plotGraph(self,projectName, eligibleReviewer, minReviewNo, topTenReviewer, topTenResult, totalReviewList):
        print(eligibleReviewer)
        try:
            self.plt.bar(topTenReviewer, topTenResult, width=0.3, align='center', label="USEFULNESS\n"
                                                                                   "*At least " + minReviewNo.__str__() + " reviews")
            self.plt.bar(topTenReviewer, totalReviewList, width=0.3, align='edge', color='green',
                    label="Project_Usefulness")
            self.plt.legend(fontsize=60)
        except:
            topTenReviewer = [" " for i in range(0, 1)]
            topTenResult = [0.0 for i in range(0, 1)]
            totalReviewList = [0.0 for i in range(0, 1)]

            self.plt.bar(topTenReviewer, topTenResult)
            self.plt.bar(topTenReviewer, totalReviewList)
            # plt.legend(fontsize=60)

        self.plt.title("Project: " + projectName + "\nTOP " + eligibleReviewer.__str__(), fontsize=80)
        self.plt.xlabel("\nReviewer", fontsize=55)
        self.plt.xticks(fontsize=40)
        self.plt.yticks(self.np.arange(0, 110, 10.0), fontsize=50)
        self.plt.ylabel("Percentage", fontsize=55)

        fig = self.plt.gcf()
        fig.set_size_inches(75, 35)
        fig.savefig('Graph/Project_' + projectName + '.png', dpi=100)


    def getProjectResult(self,projectName, winner=10, minReviewNo=10):
        projectName = projectName.__str__()
        eligibleReviewer, eligibleReviewerList = self.getEligibleReviewerList(projectName, minReviewNo)
        eligibleReviewer = min(eligibleReviewer, winner)

        individualTotalDict = {}
        individualUsefulDict = {}

        for reviewer in eligibleReviewerList:
            individualTotalDict[reviewer] = self.getIndividualTotal(projectName, reviewer)
            individualUsefulDict[reviewer] = self.getIndividualUseful(projectName, reviewer)

        individualResultDict = {}
        for reviewer in eligibleReviewerList:
            frac = ((individualUsefulDict[reviewer] + 0.0) / individualTotalDict[reviewer]) * 100.0
            frac = round(frac, 3)
            individualResultDict[reviewer] = frac
            # print(frac)

        sortedIndividualResult = sorted(individualResultDict.items(), key=self.operator.itemgetter(1), reverse=True)
        # print(sortedIndividualResult)

        topTenReviewer = []
        topTenResult = []

        for i in range(0, eligibleReviewer):
            topTenReviewer.append(sortedIndividualResult[i][0])
            topTenResult.append(sortedIndividualResult[i][1])

        annualTotal = self.getAnnualTotal(projectName)
        annualUseful = self.getAnnualUseful(projectName)

        try:
            annualReviewFrac = ((annualUseful + 0.0) / annualTotal) * 100.0
        except:
            annualReviewFrac = 0
            annualReviewList = []
        else:
            annualReviewFrac = round(annualReviewFrac, 3)
            annualReviewList = [annualReviewFrac for i in range(0, eligibleReviewer)]
            # print (annualReviewList)

        # print(annualReviewList)
        self.plotGraph(projectName, eligibleReviewer, minReviewNo, topTenReviewer, topTenResult, annualReviewList)



if __name__=='__main__':
    queryProject=DbQueryProject()
    queryProject.getProjectResult('iotivity')

