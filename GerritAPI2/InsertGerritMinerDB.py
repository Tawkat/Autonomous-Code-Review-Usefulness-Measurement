# Amiangshu Sir


import sqlite3

connection=sqlite3.connect('GerritMiner.db')
connection.text_factory = str
cursor=connection.cursor()

class InsertMinerDB:

    def saveReviewer(gerrit_id, full_name, preferred_email, username, avatar):
        cursor.executemany("insert into people (gerrit_id,full_name,preferred_email,username,avatar) values(?,?,?,?,?)",
                           [(gerrit_id, full_name, preferred_email, username, avatar)])
        connection.commit()

    def saveReviewRequestList(project_id, gerrit_id, gerrit_key, owner, owner_name,subject,status,project,branch,topic,
                              starred,last_updated_on,sort_key,insertions,deletions,owner_email,created):

        cursor.executemany("insert into requests "
							+ "(project_id,gerrit_id,gerrit_key,owner,owner_name,subject,"
                            + "status,project,branch,topic,starred,last_updated_on,sort_key,"
                            + "insertions,deletions,owner_email,created) values"
							+ "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           [(project_id, gerrit_id, gerrit_key, owner, owner_name,subject,status,project,branch,topic,
                              starred,last_updated_on,sort_key,insertions,deletions,owner_email,created)])
        connection.commit()


    def saveReviewRequestShortList(project_id,gerrit_id,gerrit_key,owner,sort_key):
        cursor.executemany("insert into requests_temp(project_id,gerrit_id,gerrit_key,owner,sort_key) values(?,?,?,?,?)",
                           [(project_id,gerrit_id,gerrit_key,owner,sort_key)])
        connection.commit()

    def saveDetailsRequest( request_id,gerrit_id,project,branch,topic,change_id,subject,status,created,updated,
                            insertions,deletions,sort_key,mergeable,owner,number_patches,curent_patch_id):

        cursor.executemany("INSERT INTO request_detail ( request_id,gerrit_id,project,branch,topic,"
                            + "change_id,subject,status,created,updated,"
                            + "insertions,deletions,sort_key,mergeable,owner,"
                            + "number_patches,curent_patch_id)"
                            + " VALUES ( ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?)",
                           [( request_id,gerrit_id,project,branch,topic,change_id,subject,status,created,updated,
                            insertions,deletions,sort_key,mergeable,owner,number_patches,curent_patch_id)])
        connection.commit()


    def patches(request_id,revision,patchset_number,comment_count,subject,message,checkout,cherrypick,
                            format,pull,author,committer,author_id,created,committed):

        cursor.executemany("INSERT INTO patches ( "+
                            "request_id,revision,patchset_number,"+
                            "comment_count,subject,message,checkout,cherrypick,"+
                            "format,pull,author,committer,author_id,created,committed)"+
                            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           [(request_id,revision,patchset_number,comment_count,subject,message,checkout,cherrypick,
                            format,pull,author,committer,author_id,created,committed)])
        connection.commit()


    def patchDetails(request_id,patchset_id,file_name,change_type,insertions,deletions):
        cursor.executemany("INSERT INTO patch_details "+
                            "(request_id,patchset_id,file_name,change_type,insertions,deletions)"+
                            " VALUES (?, ?, ?, ?, ?, ?)",
                           [(request_id,patchset_id,file_name,change_type,insertions,deletions)])
        connection.commit()


    def ReviewComments(request_id,message_id,patchset_id,author,created,message):
        cursor.executemany("INSERT INTO review_comments "+
                            "(request_id,message_id,patchset_id,author,created,message)"+
                            " VALUES (?,?,?,?,?,?)",
                           [(request_id,message_id,patchset_id,author,created,message)])
        connection.commit()

    def Reviews(request_id,people_id,verified,reviewed,build):
        cursor.executemany("INSERT INTO reviews "+
                            "(request_id,people_id,verified,reviewed,build) "+
                            "VALUES (?,?,?,?,?)",
                           [(request_id,people_id,verified,reviewed,build)])
        connection.commit()


    def inlineComments(comment_id,request_id,in_reply_to,patchset_id,file_name,line_number,author_id,written_on,status,side,
                       message,start_line,end_line,start_character,end_character):

        cursor.executemany("INSERT INTO inline_comments " +
                            "(comment_id,request_id,in_reply_to,patchset_id,file_name,"+
                            "line_number,author_id,written_on,status,side,"+
                            "message,start_line,end_line,start_character,end_character) VALUES " +
                            "(?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?)",
                           [(comment_id,request_id,in_reply_to,patchset_id,file_name,line_number,author_id,
                             written_on,status,side,message,start_line,end_line,start_character,end_character)])
        connection.commit()

