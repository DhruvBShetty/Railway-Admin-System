import sqlite3
from datetime import datetime
from fastapi import Request
import typing



def CheckNone(tableurl,form):
    for i in form:
        if (i.data=='') or (i.data is None):
            flash('{} is not entered'.format(i.label))
            #return jsonify({"Train":"Invalid entry"})
            return redirect(url_for(tableurl))

def Deleteop(Table,pk,pkdata):
    db=sqlite3.connect('railwaydb1')
    db.cursor().execute("DELETE FROM {} WHERE {}='{}'".format(Table,pk,pkdata))
    db.commit()
    db.close()
    

def Addop(Table,form):
     exclude=['csrf_token','submit','crud']
     nlist=[i.data for i in form if i.id not in exclude]
     db=sqlite3.connect('railwaydb1')
     mystring="INSERT INTO {} VALUES ({})".format(Table,','.join(["'{}'"]*(len(nlist))))
     db.cursor().execute(mystring.format(*nlist))

     db.commit()
     db.close()
     

    
     


def Updateop(Table,form,clist,pk,pkname):
    db=sqlite3.connect('railwaydb1')
    exclude=['csrf_token','submit','crud']
    dlist=[i.data for i in form if i.id not in exclude]
    
    for i in range(len(dlist)):
        if (dlist[i]!='') and (dlist[i] is not None):
            db.cursor().execute("UPDATE {0} SET {1}='{2}' WHERE {3}='{4}'".format(Table,clist[i],dlist[i],pkname,pk.data))
    db.commit()
    db.close()
    



def SeeRaw(Table):
    db=sqlite3.connect('railwaydb1')
    query=db.cursor().execute("SELECT * FROM {}".format(Table)).fetchall()
    db.close()
    return query


def Userquery(Table,key,keyval):
    db=sqlite3.connect('railwaydb1')
    query=db.cursor().execute("SELECT * FROM {} WHERE {}='{}'".format(Table,key,keyval)).fetchone()
    return query

def SeeView(Table,clist):
    db=sqlite3.connect('railwaydb1')
    query=db.cursor().execute("SELECT * FROM {}".format(Table)).fetchall()
    outerl={}
    for i in range(len(query)):
        innerl={}
        for j in range(len(query[i])):
            innerl["{}".format(clist[j])]="{}".format(query[i][j])
        outerl["{}".format(i)]="{}".format(innerl)
    db.commit()
    db.close()
    return outerl

def FormUpd(form,dtcols,query):
    ct=0
    query=list(query)
    for i in form:
        if i.type=="BooleanField":
            if query[ct]=='False':
                query[ct]=0
            if query[ct]=='True':
                query[ct]=1
        if i.id in dtcols:
            i.data=datetime.strptime(query[ct],"%H:%M:%S")
            ct=ct+1
            continue
        if i.id!='csrf_token' and i.id!='submit':
            i.data=query[ct]
            ct=ct+1