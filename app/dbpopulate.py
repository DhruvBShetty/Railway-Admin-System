import sqlite3
import json
import pandas as pd
import numpy as np

traindf=pd.read_json('/home/epi/test/venv2 copy/dataset/trains.json')
scheduledf=pd.read_json('/home/epi/test/venv2 copy/dataset/schedules.json')
stationdf=pd.read_json('/home/epi/test/venv2 copy/dataset/stations.json')


def tableclean(df):
    df=df.replace(to_replace='None', value=np.nan).dropna()
    return df.reset_index(drop = True)

def cleandf(df2):
    mylist={}
    for i in range(len(df2['features'])):
        mylist["{}".format(i)]=(df2['features'][i]['properties'])
    mylist=json.dumps(mylist)
    cleandf2=pd.read_json(mylist).T
    return tableclean(cleandf2)

def cleanstat(df):
    coordinates=[]
    for i in range(len(df['features'])):
        if df['features'][i]['geometry'] is None:
            coordinates.append('None')
        else:
            coordinates.append(df['features'][i]['geometry']['coordinates'])
    dfcl=cleandf(df)
    dfcl['coordinates']=pd.Series([[round(i[1],4),round(i[0],4)] if i!='None' else i for i in coordinates])
    return tableclean(dfcl)  

scheduledf=tableclean(scheduledf)
traindf=cleandf(traindf)
stationdf=cleanstat(stationdf)

train_col=['number','name','type','from_station_code','to_station_code','departure','arrival','duration_h','duration_m','distance','first_class','chair_car','first_ac','second_ac','third_ac','sleeper']
stat_cols=['code','name','zone','address','state','coordinates']
sched_cols=['id','train_number','station_code','departure','arrival','day']
    


def durationfunc(hours,mins):
    return "{} hrs {} mins".format(hours,mins)

def Addbop(Table,form):
     db=sqlite3.connect('railwaydb1')
     mystring="INSERT INTO {} VALUES ({})".format(Table,','.join(["'{}'"]*(len(form))))
     try:
        db.cursor().execute(mystring.format(*form))
        print('{} {} has been added'.format(Table,form[0]))
     except sqlite3.IntegrityError:
        print('{} {} already exists'.format(Table,form[0]))
     db.commit()
     db.close()

def datafromjson(listind,colist):
    datalist=[]
    for i in range(len(colist)):
        if colist[i]=='duration_h':
            datalist.append(durationfunc(listind[colist[i]],listind[colist[i+1]]))
            continue
        if colist[i]=='duration_m':
            continue
        datalist.append(listind[colist[i]])
    return datalist

#To populate database
for i,row in stationdf.iterrows():
    if i<200:
        Addbop('Station',datafromjson(row,stat_cols))
    
for i,row in traindf.iterrows():
    if i<200:
        Addbop('Train',datafromjson(row,train_col))

for i,row in scheduledf.iterrows():
        if i<200:
            Addbop('Schedule',datafromjson(row,sched_cols))
