from ctypes import create_unicode_buffer
from fastapi import FastAPI,APIRouter, Query, HTTPException, Request,status, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional, Any
from crud import Deleteop,Addop,Updateop,CheckNone,SeeView,SeeRaw,Userquery,FormUpd
from forms import StationForm, ScheduleForm,TrainForm
from starlette_wtf import CSRFProtectMiddleware, csrf_protect
from starlette.responses import (PlainTextResponse, RedirectResponse,
                                 HTMLResponse)
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from jinja2 import Template
from starlette.applications import Starlette
from pydantic import BaseModel
from fastapi.responses import RedirectResponse


templates = Jinja2Templates(directory="templates")


app = FastAPI(middleware=[
    Middleware(SessionMiddleware, secret_key='***REPLACEME1***'),
    Middleware(CSRFProtectMiddleware, csrf_secret='***REPLACEME2***')
])
app.mount("/static", StaticFiles(directory="static"), name="static")
api_router = APIRouter()


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.route('/schedule',methods=['GET','POST','DELETE'])
async def schedule(request: Request):
    form= await ScheduleForm.from_formdata(request)
    query=SeeRaw('Schedule')
    return templates.TemplateResponse("schedule.html",{"request": request,"form":form,"query":query})

@app.route('/train',methods=['GET','POST'])
async def train(request: Request):
    form= await TrainForm.from_formdata(request)
    query=SeeRaw('Train')
    return templates.TemplateResponse('train.html',{"request": request,"form":form,"query":query})

@app.route('/station',methods=['GET','POST'])
async def station(request: Request):
    form= await StationForm.from_formdata(request)
    query=SeeRaw('Station')
    return templates.TemplateResponse('station.html',{"request": request,"form":form,"query":query})

@app.get('/Createstation')
@csrf_protect
async def Createstation(request: Request):
    form=await StationForm.from_formdata(request)
    return templates.TemplateResponse('createform.html',{"request": request,"form":form})

@app.post('/Createstation')
@csrf_protect
async def Createstation(request: Request):
    form=await StationForm.from_formdata(request)
    Addop('Station',form)
    return  RedirectResponse('/station')



@app.get('/Createtrain')
@csrf_protect
async def Createtrain(request: Request):
    form=await TrainForm.from_formdata(request)
    return templates.TemplateResponse('createform.html',{"request": request,"form":form})

@app.post('/Createtrain')
@csrf_protect
async def Createtrain(request: Request):
    form=await TrainForm.from_formdata(request)
    Addop('Train',form)
    return  RedirectResponse('/train')


@app.get('/Createschedule')
@csrf_protect
async def Createschedule(request: Request):
    form=await ScheduleForm.from_formdata(request)
    return templates.TemplateResponse('createform.html',{"request": request,"form":form})


@app.post('/Createschedule')
@csrf_protect
async def Createschedule(request: Request):
    form=await ScheduleForm.from_formdata(request)
    Addop('Schedule',form)
    return  RedirectResponse('/schedule')


@app.get('/schedule/{sc_id}')
@csrf_protect
async def sc_id(request: Request,sc_id:str):
    query=Userquery('Schedule','sc_id',sc_id)
    form=await ScheduleForm.from_formdata(request)
    timesls=['departure_time','arrival_time']
    FormUpd(form,timesls,query)
    return templates.TemplateResponse('update.html',{"request": request,"form":form})


@app.post('/schedule/{sc_id}')
@csrf_protect
async def sc_id(request: Request,sc_id:str):
    form=await ScheduleForm.from_formdata(request)
    sched_cols=['sc_id','train_number','station_code','departure_time','arrival_time','day_of_travel']
    Updateop('Schedule',form,sched_cols,form.sc_id,'sc_id')
    return RedirectResponse('/schedule')

@app.delete('/schedule/{sc_id}')
async def del_sched(request: Request,sc_id:str):
    Deleteop('Schedule','sc_id',sc_id)
    
    


@app.get('/train/{number}')
@csrf_protect
async def sc_id(request: Request,number:str):
    query=Userquery('Train','number',number)
    form=await TrainForm.from_formdata(request)
    timesls=['departure_time','arrival_time']
    FormUpd(form,timesls,query)
    return templates.TemplateResponse('update.html',{"request": request,"form":form})


@app.post('/train/{number}')
@csrf_protect
async def number(request: Request, number:str):
    form=await TrainForm.from_formdata(request)
    train_cols=['number','name','type','initial_station_code','final_station_code','initial_departure_time','final_arriving_time',
            'duration','distance','first_class','chair_car','first_ac','second_ac','third_ac','sleeper']
    Updateop('Train',form,train_cols,form.number,'number')
    return RedirectResponse('/train')

@app.delete('/train/{number}')
async def del_train(request: Request,number:str):
    Deleteop('Train','number',number)
    

@app.get('/station/{code}')
@csrf_protect
async def code(request: Request,code:str):
    query=Userquery('Station','code',code)
    form=await StationForm.from_formdata(request)
    timesls=['departure_time','arrival_time']
    FormUpd(form,timesls,query)
    return templates.TemplateResponse('update.html',{"request": request,"form":form})


@app.post('/station/{code}')
@csrf_protect
async def code(request: Request, code:str):
    form=await StationForm.from_formdata(request)
    stat_cols=['code','name','zone','address','state','coordinates']
    Updateop('Station',form,stat_cols,form.code,'code')
    return RedirectResponse('/station')

@app.delete('/station/{code}')
async def del_code(request: Request,code:str):
    Deleteop('Station','code',code)
    


@app.get('/stationmap')
async def stationmap(request: Request):
    query=SeeRaw('Station')
    return templates.TemplateResponse('stationmap.html',{"request": request,"query":query})
    
    
    
    









