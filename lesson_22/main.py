from pydantic import BaseModel , conint ,constr

# class User(BaseModel):
#     id: int
#     name: str
#     age: int
#     email: str

# user = User(id=1,name="lis",age="20",email="lisi@gmail.com")
# print(user)

class User(BaseModel):
    id: int
    name: str
    age: Optional[int]= None
    email: Optional[str] = None

user = User(id=1,name="lis",age=20,email="lisi@gmail.com")
print(user)

user2 = User(id=2 , name="Darsej" , email="darsej@gmail.com")
print(user2)


class another_user(BaseModel):
    id:conint(gt=0) #<0
    name:constr(min_leangth = 2 ,max_length=50)

valid_user = another_user(id=1 , name="lis")
print(valid_user)