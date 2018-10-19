import sys

reload(sys)
sys.setdefaultencoding('utf8')

import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import operator

connection=sqlite3.connect('Gerrit.db')
connection.text_factory=str
cursor=connection.cursor()
'''
reviewer="George Nash"
cursor.execute("Select COUNT(review_id) FROM reviewTable WHERE reviewer=?",([reviewer]))
number=cursor.fetchall()
print(number[0])

cursor.execute("Select COUNT(review_id) FROM reviewTable WHERE reviewer=? AND (usefulness='A' OR usefulness='B')",([reviewer]))
number=cursor.fetchall()
print(number[0])
'''

def getProjectReviewersFromDB(cursor, project_name="iotivity"):
    cursor.execute("Select DISTINCT reviewer from reviewTable")
    reviewerData = cursor.fetchall()
    #rl = []
    projectReviewers=[]
    for reviewer in reviewerData:
        if (reviewer != "Gerrit-Review"):
            projectReviewers.append(reviewer[0])
            print(projectReviewers[-1])
    #print(len(rl))
    #projectReviewers = set(rl)
    #print(len(projectReviewers))
    print(projectReviewers)
    return projectReviewers



#projectReviewers=getProjectReviewersFromDB(cursor)
'''
cursor.execute("Select DISTINCT change_subject,review_date FROM ChangeTable JOIN ReviewTable ON ChangeTable.change_id=ReviewTable.change_id WHERE review_date>'2017-11-22 00:00:00'")
changeData=cursor.fetchall()
for change in changeData:
    print(change[0],change[1])
'''

'''
cursor.execute("SELECT DISTINCT reviewer from ReviewTable JOIN ChangeTable ON ReviewTable.change_id=ChangeTable.change_id "
               "WHERE project_name='iotivity'")

'''

cursor.execute("SELECT DISTINCT R1.reviewer from ReviewTable R1 JOIN ChangeTable C ON R1.change_id=C.change_id "
               "WHERE C.project_name='iotivity' AND 9<(SELECT COUNT(R2.review_id) FROM ReviewTable R2 WHERE R2.reviewer=R1.reviewer)")

data=cursor.fetchall()

#print(len(data))
projectReviewer=[]
for d in data:
    projectReviewer.append(d[0])

projectReviewTotal=[]
for reviewer in projectReviewer:
    cursor.execute(
        "SELECT COUNT(review_id) from ReviewTable JOIN ChangeTable ON ReviewTable.change_id=ChangeTable.change_id "
        "WHERE project_name='iotivity' AND reviewer=?",([reviewer]))
    data = cursor.fetchall()
    #print(data[0][0],reviewer)
    projectReviewTotal.append(data[0][0])

projectReviewUseful=[]
for reviewer in projectReviewer:
    cursor.execute(
        "SELECT COUNT(review_id) from ReviewTable JOIN ChangeTable ON ReviewTable.change_id=ChangeTable.change_id "
        "WHERE project_name='iotivity' AND reviewer=? AND (usefulness='A' OR usefulness='B')",([reviewer]))
    data = cursor.fetchall()
    #print(data[0][0],reviewer)
    projectReviewUseful.append(data[0][0])

projectDict={}
projectReview=[]
for i in range(0,len(projectReviewTotal)):
    frac=((projectReviewUseful[i]+0.0)/projectReviewTotal[i])*100.0
    frac=round(frac,3)
    projectReview.append(frac)
    projectDict[projectReviewer[i]]=frac
    print(frac)

sortedProjectReview=sorted(projectDict.items(), key=operator.itemgetter(1),reverse=True)
print(sortedProjectReview)
topTenReviewer=[]
topTenReview=[]

for i in range(0,10):
    topTenReviewer.append(sortedProjectReview[i][0])
    topTenReview.append(sortedProjectReview[i][1])


cursor.execute("SELECT DISTINCT COUNT(review_id) from ReviewTable R1 JOIN ChangeTable C ON R1.change_id=C.change_id "
               "WHERE C.project_name='iotivity'")

data=cursor.fetchall()

totalReview=data[0][0]
cursor.execute("SELECT DISTINCT COUNT(review_id) from ReviewTable R1 JOIN ChangeTable C ON R1.change_id=C.change_id "
               "WHERE C.project_name='iotivity' AND (R1.usefulness='A' OR R1.usefulness='B')")

data=cursor.fetchall()
totalUsefulReview=data[0][0]
totalReviewFrac=((totalUsefulReview+0.0)/totalReview)*100.0
totalReviewFrac=round(totalReviewFrac,3)
totalReviewList=[totalReviewFrac for i in range(0,10)]
print (totalReviewList)

plt.bar(topTenReviewer,topTenReview,width=0.3,align='center',label="USEFULNESS\n*At least 10 reviews")
plt.bar(topTenReviewer,totalReviewList,width=0.3,align='edge',color='green',label="Project_Usefulness")
plt.title("Project: Iotivity\nTOP 10",fontsize=50)
plt.xlabel("\nReviewer",fontsize=55)
plt.xticks(fontsize=40)
plt.yticks(np.arange(0, 110, 10.0),fontsize=50)
plt.ylabel("Percentage",fontsize=55)

plt.legend(fontsize=60)
fig = plt.gcf()
fig.set_size_inches(75, 35)
fig.savefig('Project_Iotivity.png', dpi=100)
#plt.show()