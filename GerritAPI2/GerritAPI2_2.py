from pygerrit2.rest import GerritRestAPI


class ReviewExtractor:

    def __init__(self,url='https://review.gerrithub.io/',auth=None):
        self.changeList = []
        self.url=url
        self.auth=auth

        if auth is not None:
            self.username="Tawkat"
            self.password="7rfXaM1kbYYNWE73X0B4wX0y/+FO3mkffvFYFHw8Rg"
            from requests.auth import HTTPBasicAuth
            from pygerrit2.rest import GerritRestAPI
            self.auth = HTTPBasicAuth(self.username, self.password)

    def query(self,project_name=None,limit=None):
        if limit is None:
            limitRange=""
        else:
            limitRange="n=" + str(limit)

        if project_name is None:
            project_query=""
        else:
            #project_query = "q=project:" + project_name
            limitRange="&"+limitRange

        project_query="q=status:open"
        self.project_name=project_name
        self.limit=limit

        try:
            self.rest = GerritRestAPI(url=self.url, auth=self.auth)
            #self.changes=self.rest.get("/changes/?q=project:" + self.project_name + limitRange)
            #self.changes = self.rest.get("/changes/?" + project_query)
            self.changes = self.rest.get("/changes/?q=status:merged" + "&n=" + str(self.limit))
        except:
            print("Connection Error!")

        else:
            # print(self.changes)
            # self.ownerDupList=[]
            index = 1
            for change in self.changes:
                print("Change Collecting Index in ReviewExtractor.query() %s" % index)
                index += 1
                reviewDict = self.getReviewDict(change)
                if reviewDict is not None:
                    self.changeList.append(reviewDict)
                    # self.ownerDupList.append(self.changeList[-1]['changeDetail']['owner']['name'])


    def getChangeOwner(self,change):
        changeDetail = change['changeDetail']
        changeOwner = changeDetail['owner']['name']
        #return changeOwner.encode('utf-8')
        return changeOwner

    def getOwnerList(self,limit=None):
        if limit is None:
            limitRange=""
        else:
            limitRange="&n=" + str(limit)

        self.ownerDupList = []
        changes = self.rest.get("/changes/?q=project:" + self.project_name + limitRange)
        for index,change in enumerate(changes,1):
            print("Owner Collecting Index in ReviewExtractor.getOwnerList() %s" % index)
            try:
                changeDetail = self.rest.get("/changes/" + change['id'] + "/detail")
            except:
                print("Change['id'] = %s is broken while extracting detail in getOwnerList()." % str(change['id']))
                continue
            else:
                owner=changeDetail['owner']['name']
                #self.ownerDupList.append(owner.encode('utf-8'))
                self.ownerDupList.append(owner)
        ownerList=set(self.ownerDupList)
        return ownerList


    def getProjectReviewers(self):
        rl=[]

        for change in self.changeList:
            reviewInfo=self.getReviewInfo(change)
            for review in reviewInfo:
                reviewer = self.getReviewer(review)
                dummyReviewer=reviewer.lower()
                if (dummyReviewer.startswith("jenkin") or dummyReviewer.endswith("jenkin")
                    or dummyReviewer.startswith("jenkins") or dummyReviewer.endswith("jenkins")):   ###########################################
                    continue

                rl.append(reviewer)

        projectReviewers=set(rl)
        return projectReviewers




    def getReviewDict(self,change):
        reviewDict = {}

        try:
            changeDetail = self.rest.get("/changes/" + change['id'] + "/detail")
        except:
            print("Change['id'] = %s is broken while extracting detail in getReviewDict()." % str(change['id']))
            return None
        else:
            reviewDict['changeDetail'] = changeDetail
            messages = changeDetail['messages']
            reviewDict['messages'] = messages
            comments = self.rest.get("/changes/" + change['id'] + "/comments/")
            reviewDict['comments'] = comments

            modifiedMessages = messages
            for review in modifiedMessages:
                # print("Author:"+str(change['author']['name'])+"  Message:"+str(change['message']),end='\n')
                review['comments'] = []
                for link in comments.keys():
                    extraMessage = ''
                    isFound = False
                    for listElem in comments[link]:
                        author = listElem['author']
                        try:
                            if ((review['author']['_account_id'] == author['_account_id']) and (
                                        review['date'] == listElem['updated'])):
                                isFound = True
                                if not link in review.keys():
                                    review[link] = []
                                if not link in review['comments']:
                                    review['comments'].append(link)
                                if not listElem['id'] in review[link]:
                                    review[link].append(listElem['id'])
                                extraMessage = extraMessage + '\n' + 'Line ' + str(listElem['line']) + ': ' + listElem[
                                    'message']
                        except:
                            isFound = False

                    if isFound:
                        review['message'] = review['message'] + '\n' + link + extraMessage + '\n'

            reviewDict['reviewInfo'] = modifiedMessages

            return reviewDict


    def getChangeList(self):
        return self.changeList


    def getChangeListSubjects(self):
        subjectLists=[]
        for change in self.changeList:
            subjectLists.append(self.getChangeSubject(change))
        return subjectLists



    def getChangeId(self,change):
        changeDetail=change['changeDetail']
        return changeDetail['id']

    def getChangeSubject(self,change):
        changeDetail=change['changeDetail']
        return changeDetail['subject']

    def getChangeSubject(self,change):
        changeDetail=change['changeDetail']
        return changeDetail['subject']

    def getLastPatchCount(self,change):
        changeDetail=change['changeDetail']
        message=changeDetail['messages']
        return (message[-1]['_revision_number'])

    def isLast(self,change,review):
        changeDetail = change['changeDetail']
        if (changeDetail['status'].lower() == "new" or changeDetail['status'].lower() == "open"):
            return 0
        elif (self.getLastPatchCount(change)!=review['_revision_number']):
            return 0
        else:
            return 1


    def getReviewInfo(self,change):
        return change['reviewInfo']


    def getReviewId(self,review):
        return review['id']


    def getReviewer(self,review):
        if 'author' in review.keys():
            reviewer=review['author']['name']
            #return reviewer.encode('utf-8')
            return reviewer
        return "Gerrit-Review"

    def getReview(self,review):
        reviewData=review['message']
        #return reviewData.encode('utf-8')
        return reviewData

    def getReviewDate(self,review):
        return review['date']



if __name__=='__main__':
    reviewExtractor = ReviewExtractor(auth='o')
    reviewExtractor.query(limit=5)
    changeList = reviewExtractor.getChangeList()

    for index,change in enumerate(changeList,start=1):
        print ("Change Id: %s\n" % str(reviewExtractor.getChangeId(change)))
        print ("Change Subject: " + reviewExtractor.getChangeSubject(change)+"\n")