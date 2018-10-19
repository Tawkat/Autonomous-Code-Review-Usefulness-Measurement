
class DbQueryYear:
    def __init__(self):
        import sys

        reload(sys)
        sys.setdefaultencoding('utf8')

        import sqlite3
        import matplotlib.pyplot as plt
        import numpy as np
        import operator

        self.operator = operator
        self.plt = plt
        self.np = np

        connection = sqlite3.connect('Gerrit.db')
        connection.text_factory = str
        self.cursor = connection.cursor()

    '''
    year=2017
    self.cursor.execute("SELECT DISTINCT reviewData from ReviewTable JOIN ChangeTable ON ReviewTable.change_id=ChangeTable.change_id "
                   "WHERE project_name='iotivity' and STRFTIME('%Y',review_Date)=?",([year.__str__()]))
    '''

    def getEligibleReviewerList(self,year, reviewNo=10):
        self.cursor.execute("SELECT DISTINCT R1.reviewer FROM ReviewTable R1 "
                       "WHERE STRFTIME('%Y',review_Date)=? AND ?<=(SELECT COUNT(R2.review_id) FROM ReviewTable R2 "
                       "WHERE R2.reviewer=R1.reviewer)", ([year, reviewNo]))

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

    def getIndividualTotal(self,year, reviewer):
        self.cursor.execute(
            "SELECT COUNT(review_id) FROM ReviewTable "
            "WHERE STRFTIME('%Y',review_Date)=? AND reviewer=?", ([year, reviewer]))
        data = self.cursor.fetchall()
        # print(data[0][0],reviewer)
        return data[0][0]

    def getIndividualUseful(self,year, reviewer):
        self.cursor.execute(
            "SELECT COUNT(review_id) FROM ReviewTable "
            "WHERE STRFTIME('%Y',review_Date)=? AND (usefulness='A' OR usefulness='B') AND reviewer=?",
            ([year, reviewer]))
        data = self.cursor.fetchall()
        # print(data[0][0],reviewer)
        return data[0][0]

    def getAnnualTotal(self,year):
        self.cursor.execute(
            "SELECT COUNT(review_id) FROM ReviewTable "
            "WHERE STRFTIME('%Y',review_Date)=?", ([year]))
        data = self.cursor.fetchall()
        # print(data[0][0],reviewer)
        return data[0][0]

    def getAnnualUseful(self,year):
        self.cursor.execute(
            "SELECT COUNT(review_id) FROM ReviewTable "
            "WHERE STRFTIME('%Y',review_Date)=? AND (usefulness='A' OR usefulness='B')", ([year]))
        data = self.cursor.fetchall()
        # print(data[0][0],reviewer)
        return data[0][0]

    def plotGraph(self,year, eligibleReviewer, minReviewNo, topTenReviewer, topTenResult, totalReviewList):
        print(eligibleReviewer)
        try:
            self.plt.bar(topTenReviewer, topTenResult, width=0.3, align='center', label="USEFULNESS\n"
                                                                                   "*At least " + minReviewNo.__str__() + " reviews")
            self.plt.bar(topTenReviewer, totalReviewList, width=0.3, align='edge', color='green',
                    label="Annual_Usefulness")
            self.plt.legend(fontsize=60)
        except:
            topTenReviewer = [" " for i in range(0, 1)]
            topTenResult = [0.0 for i in range(0, 1)]
            totalReviewList = [0.0 for i in range(0, 1)]

            self.plt.bar(topTenReviewer, topTenResult)
            self.plt.bar(topTenReviewer, totalReviewList)
            #self.plt.legend(fontsize=60)

        self.plt.title("ANNUAL RESULT: " + year + "\nTOP " + eligibleReviewer.__str__(), fontsize=80)
        self.plt.xlabel("\nReviewer", fontsize=55)
        self.plt.xticks(fontsize=40)
        self.plt.yticks(self.np.arange(0, 110, 10.0), fontsize=50)
        self.plt.ylabel("Percentage", fontsize=55)

        fig = self.plt.gcf()
        fig.set_size_inches(75, 35)
        fig.savefig('Graph/Annual '+year+'_Judgement.png', dpi=100)

    def getAnnualResult(self,y_in_integer, winner=10, minReviewNo=10):
        year = y_in_integer.__str__()
        eligibleReviewer, eligibleReviewerList = self.getEligibleReviewerList(year, minReviewNo)
        eligibleReviewer = min(eligibleReviewer, winner)

        individualTotalDict = {}
        individualUsefulDict = {}

        for reviewer in eligibleReviewerList:
            individualTotalDict[reviewer] = self.getIndividualTotal(year, reviewer)
            individualUsefulDict[reviewer] = self.getIndividualUseful(year, reviewer)

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

        annualTotal = self.getAnnualTotal(year)
        annualUseful = self.getAnnualUseful(year)

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
        self.plotGraph(year, eligibleReviewer, minReviewNo, topTenReviewer, topTenResult, annualReviewList)


        # self.plt.show()


if __name__=='__main__':
    queryYear=DbQueryYear()
    queryYear.getAnnualResult(2018)