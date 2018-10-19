
class DbQueryIndividual:
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

        self.months=['none','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


    '''
    year=2017
    self.cursor.execute("SELECT DISTINCT reviewData from ReviewTable JOIN ChangeTable ON ReviewTable.change_id=ChangeTable.change_id "
                   "WHERE project_name='iotivity' and STRFTIME('%Y',review_Date)=?",([year.__str__()]))
    '''

    def getReviewerList(self):
        self.cursor.execute("SELECT DISTINCT R1.reviewer FROM ReviewTable R1")

        data = self.cursor.fetchall()
        reviewerList = []
        for d in data:
            reviewer = d[0].lower()
            if (reviewer.startswith("jenkin") or reviewer.endswith("jenkin")
                or reviewer.startswith("jenkins") or reviewer.endswith("jenkins")
                or reviewer.startswith("gerrit") or reviewer.endswith("gerrit")):
                continue

            reviewerList.append(d[0])
        reviewerNo = len(reviewerList)
        # print(reviewer)
        return reviewerNo, reviewerList


    def getIndividualUseful(self,year,month,reviewer):
        self.cursor.execute(
            "SELECT COUNT(review_id) FROM ReviewTable "
            "WHERE STRFTIME('%Y',review_Date)=? AND STRFTIME('%m',review_Date)=? "
            "AND (usefulness='A' OR usefulness='B') AND reviewer=?",([year, month, reviewer]))
        data = self.cursor.fetchall()
        # print(data[0][0],reviewer)
        return data[0][0]

    def getIndividualTotal(self,year,month,reviewer):
        self.cursor.execute(
            "SELECT COUNT(review_id) FROM ReviewTable "
            "WHERE STRFTIME('%Y',review_Date)=? AND STRFTIME('%m',review_Date)=? AND reviewer=?", ([year, month, reviewer]))
        data = self.cursor.fetchall()
        # print(data[0][0],reviewer)
        return data[0][0]

    def getIndividualAnnual(self,year,reviewer):
        individualTotal={}
        individualUseful={}

        for i in range(1,13):
            if(i<10):
                data=self.getIndividualTotal(year,"0"+i.__str__(),reviewer)
                #print(data)
                if(data>0):
                    individualTotal[self.months[i]]=data
                    individualUseful[self.months[i]]=self.getIndividualUseful(year,"0"+i.__str__(),reviewer)
            else:
                data = self.getIndividualTotal(year,i.__str__(), reviewer)
                #print(data)
                if (data > 0):
                    individualTotal[self.months[i]] = data
                    individualUseful[self.months[i]] = self.getIndividualUseful(year,i.__str__(), reviewer)

        return individualTotal,individualUseful


    def getAnnualTotal(self,year,month):
        self.cursor.execute(
            "SELECT COUNT(review_id) FROM ReviewTable "
            "WHERE STRFTIME('%Y',review_Date)=? AND STRFTIME('%m',review_Date)=?", ([year,month]))
        data = self.cursor.fetchall()
        # print(data[0][0],reviewer)
        return data[0][0]

    def getAnnualUseful(self,year,month):
        self.cursor.execute(
            "SELECT COUNT(review_id) FROM ReviewTable "
            "WHERE STRFTIME('%Y',review_Date)=?  AND STRFTIME('%m',review_Date)=? "
            "AND (usefulness='A' OR usefulness='B')", ([year,month]))
        data = self.cursor.fetchall()
        # print(data[0][0],reviewer)
        return data[0][0]

    def getMonthlyAll(self, year):
        monthlyTotal = {}
        monthlyUseful = {}

        for i in range(1, 13):
            if (i < 10):
                data = self.getAnnualTotal(year, "0" + i.__str__())
                if (data > 0):
                    monthlyTotal[self.months[i]] = data
                    monthlyUseful[self.months[i]] = self.getAnnualUseful(year, "0" + i.__str__())
            else:
                data = self.getAnnualTotal(year,i.__str__())
                if (data > 0):
                    monthlyTotal[self.months[i]] = data
                    monthlyUseful[self.months[i]] = self.getAnnualUseful(year,i.__str__())

        return monthlyTotal, monthlyUseful

    def plotGraph(self,year, reviewer, months, individualResult, monthlyResult):
        print(months,individualResult)
        try:
            self.plt.plot(range(len(individualResult)), individualResult, linewidth=10, label="Monthly USEFULNESS\nof "+ reviewer)
            self.plt.scatter(range(len(individualResult)), individualResult, s=500)
            self.plt.plot(range(len(monthlyResult)), monthlyResult, linewidth=10, color='green',label="Overall\nMonthly Usefulness")
            self.plt.scatter(range(len(monthlyResult)), monthlyResult, s=500)
            self.plt.legend(fontsize=60)
            self.plt.xticks(range(len(months)), months, fontsize=60)
        except:
            months = [" " for i in range(0, 1)]
            individualResult = [0.0 for i in range(0, 1)]
            monthlyResult = [0.0 for i in range(0, 1)]

            self.plt.plot(months, individualResult,linewidth=5)
            self.plt.plot(months, monthlyResult,linewidth=5)
            #self.plt.legend(fontsize=60)

        self.plt.title("ANNUAL PERFORMANCE:\n" + reviewer, fontsize=80)
        self.plt.xlabel("\nMonths", fontsize=80)
        self.plt.yticks(self.np.arange(0, 110, 10.0), fontsize=50)
        self.plt.ylabel("Percentage", fontsize=55)

        fig = self.plt.gcf()
        fig.set_size_inches(75, 35)
        fig.savefig('Graph/Annual Preformance'+ reviewer +'.png', dpi=100)

    def getIndividualResult(self,y_in_integer, reviewer):
        year = y_in_integer.__str__()
        reviewer = reviewer.__str__()

        individualTotalDict = {}
        individualUsefulDict = {}
        individualTotalDict,individualUsefulDict=self.getIndividualAnnual(year,reviewer)

        monthlyTotalDict={}
        monthlyUsefulDict={}
        monthlyTotalDict,monthlyUsefulDict=self.getMonthlyAll(year)

        individualResultDict = {}
        for key in individualTotalDict.keys():
            frac = ((individualUsefulDict[key] + 0.0) / individualTotalDict[key]) * 100.0
            frac = round(frac, 3)
            individualResultDict[key] = frac
            # print(frac)

        monthlyResultDict = {}
        for key in monthlyTotalDict.keys():
            frac = ((monthlyUsefulDict[key] + 0.0) / monthlyTotalDict[key]) * 100.0
            frac = round(frac, 3)
            monthlyResultDict[key] = frac
            # print(frac)

        actualMonths=[]
        individualResult=[]
        monthlyResult=[]
        for month in self.months:
            if month in individualResultDict.keys():
                actualMonths.append(month)
                individualResult.append(individualResultDict[month])
                monthlyResult.append(monthlyResultDict[month])

        self.plotGraph(year, reviewer, actualMonths, individualResult, monthlyResult)


        # self.plt.show()


if __name__=='__main__':
    queryIndividual=DbQueryIndividual()
    #print (queryIndividual.getReviewerList())
    queryIndividual.getIndividualResult(2017,"George Nash")