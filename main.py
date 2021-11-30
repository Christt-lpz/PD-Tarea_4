# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 17:40:38 2021

@author: chris
"""
import io
import  pandas  as pd

from enum     import Enum
from typing   import Dict
from fastapi  import FastAPI
from typing   import Optional
from pydantic import BaseModel

from fastapi.responses import ORJSONResponse, HTMLResponse, StreamingResponse

app =FastAPI()

class  RoleName(str, Enum):
    admin ='Admin'
    write='Write'
    reader='Reader'



##TAREA --------------------

##----SUMA

@app.get("/operacions/{Suma}")
def suma(valorA: int, valorB: int):
    resultado =  valorA + valorB
    return {"Suma":resultado}

##----RESTA 
@app.get("/operacionr/{Resta}")
def resta(valorA: int, valorB: int):
    resultado =  valorA - valorB
    return {"Resta":resultado}

##----MULTIPLICACION
@app.get("/operacionm/{multiplicacion}")
def multiplicacion(valorA: int, valorB: int):
    resultado =  valorA * valorB
    return {"multiplicacion":resultado}


##----DIVICION
@app.get("/operaciond/{division}")
def division(valorA: int, valorB: int):
    resultado =  valorA / valorB
    return {"division":resultado}


@app.post("/operacions/{Suma}")
def sumaB(valorA: int, valorB: int):
    resultado =  valorA + valorB
    return {"Suma":resultado}

##----RESTA 
@app.post("/operacionr/{Resta}")
def restaB(valorA: int, valorB: int):
    resultado =  valorA - valorB
    return {"Resta":resultado}

##----MULTIPLICACION
@app.post("/operacionm/{multiplicacion}")
def multiplicacionB(valorA: int, valorB: int):
    resultado =  valorA * valorB
    return {"multiplicacion":resultado}


##----DIVICION
@app.post("/operaciond/{division}")
def divisionB(valorA: int, valorB: int):
    resultado =  valorA / valorB
    return {"division":resultado}



##TAREA --------------------


@app.get("/")
def root():
    return {"message":"Mensaje de muestra"}

@app.get("/items/{item_id}")
def read_item(item_id: int) ->Dict[str,int]: #el int me fuera a que la variable sea entera 
    return {"item_id":item_id}


@app.get("users/{user_id}")
def read_user(user_id:str):
    return {"user_id": user_id}

@app.get("/roles/{role_name}")
def get_role_permissions(role_name:RoleName):
    if role_name==RoleName.admin:
        return {"role_name": role_name, "Perfimison ":"full access"}
    
    return {"role_name": role_name, "Persimision":"write access"}




fake_item =[{"item_name":"uno"},{"item_name":"dos"},{"item_name":"res"}]


@app.get("/items/")
def  read_items(skip: int =0, limit: int=10 ):
    return fake_item[skip: skip + limit]


@app.get("/items/{idtem_id}")
def read_item_query (item_id: int, query: Optional[str] = None):
    message ={"item_id": item_id}
    if query:
        message['query'] = query 

    return message  


@app.get("/users/{user_id}/items/{item_id}")
def read_user_item (user_id:int, item_id: int, query: Optional[str]=None, describe:bool = False):
    item = {"item_id":item_id, "owner_id": user_id} 
    if query:
        item['query'] = query 
    
    if describe:
        item['description']='this is a long  description for the  item'
        




class Item (BaseModel):
    name: str
    descriptio: Optional[str] = None
    price: float 
    tax: Optional [float]=None
    
    
    
@app.post("/items/")  #pos comumente para crear   
def  freate_item(item: Item):
    return {
        
        "message":"the item was succesfully created",
        "item":item.Dict()
        }
    
#tanto el punt y el post  se pueden usar para lo mismo pero como que no es buena pratica 
@app.put("/item/{}")    #put comumento para actualizar 
def  upadte_item(item_id, int, item: Item):
    if Item.tax==  0 or  item.tax is None: 
        item.tax =item.price * 0.12

    return {
          "message":"the item was succesfully created",
        "item:id": item_id,
        "item":item.Dict()
        
        }




@app.get("/itemsall", response_class=ORJSONResponse) #tambien se puede usar UJSONResponse
def read_long_json():
    return [{"item_id":"item"},{"item_id":"item"},{"item_id":"item"},{"item_id":"item"},
            {"item_id":"item"},{"item_id":"item"},{"item_id":"item"},{"item_id":"item"},
            {"item_id":"item"},{"item_id":"item"},{"item_id":"item"},{"item_id":"item"}]


@app.get("/html", response_class=HTMLResponse)
def read_html():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head><body>
        <h1>Look ma! HTML!</h1>
        </body>
    </html>"""

    
@app.get("/csv")
def get_csv():
        df = pd.DataFrame({"Column A": [1, 2], "Column B": [3, 4]})
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]), media_type='text/csv')
        response.headers['Content-Disposition'] = "attachment; filename=my_awesome_report.csv"
        return response


