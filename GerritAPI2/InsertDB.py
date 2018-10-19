from pygerrit2.rest import GerritRestAPI
from requests.auth import HTTPDigestAuth
import sqlite3

from Classification.Classifier import Classifier
from ReviewExtractor import ReviewExtractor

clf = Classifier()

rest = GerritRestAPI(url='https://gerrit.iotivity.org/gerrit/')
connection=sqlite3.connect('Gerrit.db')
connection.text_factory = str
cursor=connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS ProjectTable(project_name TEXT, project_id TEXT, project_description TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS ChangeTable(change_id TEXT, project_name TEXT, change_subject TEXT, "
               "change_owner TEXT, FOREIGN KEY(project_name) REFERENCES ProjectTable(project_name) ON DELETE CASCADE)")
cursor.execute("CREATE TABLE IF NOT EXISTS ReviewTable(review_id TEXT,change_id TEXT, reviewer TEXT, review_date DATE, reviewData TEXT, "
               "usefulness TEXT, FOREIGN KEY (change_id) REFERENCES ChangeTable(change_id) ON DELETE CASCADE)")


def projectInsert(project_name, project_id, project_description):
    cursor.executemany("INSERT INTO ProjectTable(project_name, project_id, project_description)"
                       " VALUES(?,?,?)",
                       [(project_name, project_id, project_description)])
    connection.commit()

def changeInsert(change_id, project_name, change_subject, change_owner):
    cursor.executemany("INSERT INTO ChangeTable(change_id, project_name, change_subject, change_owner)"
                       " VALUES(?,?,?,?)",
                       [(change_id, project_name, change_subject, change_owner)])
    connection.commit()

def reviewInsert(review_id, change_id, reviewer, review_date, reviewData, usefulness):
    cursor.executemany("INSERT INTO ReviewTable(review_id, change_id, reviewer, review_date, reviewData, usefulness)"
                       " VALUES(?,?,?,?,?,?)",
                       [(review_id, change_id, reviewer, review_date, reviewData, usefulness)])
    connection.commit()










projects=rest.get("/projects/?d")
print(projects)
print(len(projects))
changeOwnerDupList=[]
for project_name in projects.keys():
    print("Inserting in Project Table: "+project_name)
    description=""
    if 'description' in projects[project_name].keys():
        description=projects[project_name]['description']
    projectInsert(project_name, projects[project_name]['id'], description)

    '''
    if True:
        project_name='iotivity'
        reviewExtractor=ReviewExtractor()
        reviewExtractor.query(project_name,30)
    '''
    reviewExtractor=ReviewExtractor()
    reviewExtractor.query(project_name)
    changeList = reviewExtractor.getChangeList()
    for change in changeList:
        change_id=reviewExtractor.getChangeId(change)
        change_subject=reviewExtractor.getChangeSubject(change)
        change_owner=reviewExtractor.getChangeOwner(change)
        print("Inserting in Change Table: " + change_subject)
        changeInsert(change_id,project_name,change_subject,change_owner)

        reviewInfo = reviewExtractor.getReviewInfo(change)
        for index,review in enumerate(reviewInfo,1):
            print("Extrating review in InsertDB Class: "+str(index))
            reviewer = reviewExtractor.getReviewer(review)
            if ((reviewer.startswith("jenkin")) or (reviewer == change_owner)):
                continue
            review_id = reviewExtractor.getReviewId(review)
            review_date = reviewExtractor.getReviewDate(review)
            reviewData = reviewExtractor.getReview(review)
            isLast = reviewExtractor.isLast(change, review)
            clf.feedReview(reviewData, isLast)
            usefulness = clf.getPrediction()
            # file.write("\nUSEFULNESS: " + usefulness+"\n")
            # file.write("\n#################################################\n\n")
            print("Inserting in Review Table: " + str(index))
            reviewInsert(review_id, change_id, reviewer, review_date, reviewData, usefulness)