from fastapi import FastAPI,Depends,HTTPException
from typing import List
from app.crud import create_item,get_item,get_item,delete_item
from app.models import Item
from app.security import get_api_key
from app.database import init_db

app = FastAPI()

init_db

@app.post("/items/",response_model=Item)
def create_new_item(item:Item,api_key:str=Depends(get_api_key)):
    return create_item(item)

@app.get("/items/",response_model=List(Item))
def read_items(api_key:str = Depends(get_api_key)):
    return get_items()

@app.get("/items/{item_id}",response_model=Item)
def read_item(item_id:int,api_key:str=Depends(get_api_key)):
    item = get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404,detail="item not found")
    return item




#foto 2