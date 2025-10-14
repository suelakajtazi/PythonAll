from fastapi import FastAPI

app = FastAPI()
# @app.get("/")
# def home():
#     return {'message':'Halloween'}

# @app.get("/user/{user_id}")
# def get_user(user_id:int):
#     return{"user_id":user_id,"name":"john doe"}


@app.get("/items/")
def readitems():
    return{"item":["item1","item2","item3"]}

@app.post("/items/")
def createitem(name:str,price:foat):
    return{"item+name":name,"item_price":price}
