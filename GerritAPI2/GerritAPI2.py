from pygerrit2.rest import GerritRestAPI
from requests.auth import HTTPDigestAuth

auth = HTTPDigestAuth('username', 'password')

query = ["status:open"]
query += ["limit:1"]

rest = GerritRestAPI(url='https://gerrit.iotivity.org/gerrit/')
#changes = rest.get("/changes/I5eefd50d6dcfcc35fd20ffd3e6e147acbf924e45/detail")
projects=rest.get("/projects/?d")
print(projects)
print(len(projects))
changeOwnerDupList=[]
for change in projects:
    #print(change['change_id'])
    #print(change['subject'])
    #print(change['status'])
    changeOwnerDupList.append(change['owner']['_account_id'])
    #print((changeOwnerDupList))

    #changes = rest.get("/changes/" + change['change_id'] + "/detail")

#print(len(changeOwnerDupList))
changeOwnerList=[]
#changeOwnerList=set(changeOwnerDupList)
#print(len(changeOwnerList))
changeOwners=[]
for index,change in enumerate(projects,1):
   print("Index %s" % index)
   changeDetail=rest.get("/changes/" + change['id'] + "/detail")
   changeOwnerList.append(changeDetail['owner']['name'])

print(len(changeOwnerList))
changeOwners=set(changeOwnerList)
print(len(changeOwners))
for name in changeOwners:
    print(name)
'''
changes = rest.get("/changes/23111/detail")
reviews=changes
comments = rest.get("/changes/23111/comments/")
print((changes))
print(comments)
abc=[]
if changes['status'].lower()=="new" or changes['status'].lower()=="open":
    print(changes['status'])
#file=open("test.txt",'w')
#print(changes['messages'])
for review in reviews['messages']:
    #print("Author:"+str(change['author']['name'])+"  Message:"+str(change['message']),end='\n')
    review['comments'] = []
    for link in comments.keys():
        extraMessage=''
        isFound=False
        for listElem in comments[link]:
            author=listElem['author']
            if ((review['author']['_account_id'] == author['_account_id']) and (review['date']==listElem['updated'])):
                isFound=True
                if not link in review.keys():
                    review[link]=[]
                if not link in review['comments']:
                    review['comments'].append(link)
                if not listElem['id'] in review[link]:
                    review[link].append(listElem['id'])
                extraMessage=extraMessage+'\n'+'Line '+str(listElem['line'])+': '+listElem['message']
        if isFound:
            review['message'] = review['message'] + '\n' + link + extraMessage + '\n'


for review in reviews['messages']:
     print("Author:"+str(review['author']['name'])+"  Message:"+str(review['message'])+"\n")
     print('________________________________')
     print(review['comments'])
     print('________________________________')
     for link in review['comments']:
         print(review[link])
'''
