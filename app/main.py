from typing import Optional
import psycopg2
import time
from fastapi import Body, FastAPI,status,HTTPException,Depends
from pydantic import BaseModel
app = FastAPI()
import models
from database import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)




## using direct database connection 


class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    # rating : Optional[int] = None


# # connecting postgres sql
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database="fast-api", user="postgres", 
#                             password="lavalava", port="5432")

#         cursor = conn.cursor()
#         # To receive data results
#         print("Database connection was successfully")
#         break
#     except Exception as err:
#         print("error was",err)
#         time.sleep(2)

# @app.get('/posts',status_code=status.HTTP_200_OK)
# def get_all_post():
#     try:
#         cursor.execute(""" SELECT * FROM post """)
#         data = cursor.fetchmany()
#         return {"data":data}
#     except BaseException as err:
#         print(err)
#         return("error",err)

# # @app.post('/post')
# # def post(payload : dict = Body(...)):
# #     return{"message":f"its a post method {payload}"}



# # validation for post data create data schema  using pydantic 
# # title : str ,  


# @app.post('/post',status_code=status.HTTP_201_CREATED)
# def post(post : Post):
#     try:
#         cursor.execute(""" INSERT INTO post(title, context, published) VALUES (%s,%s,%s) 
#         RETURNING * """,
#                         (post.title,post.context,post.published))
#         data = cursor.fetchall()
#         conn.commit()

#         return{"message":"New post is created","data":data}
#     except BaseException as err:
#         print(err)
#         return{"error",err}
    
# @app.get('/post/{id}',status_code=status.HTTP_201_CREATED)
# def get_post(id:int):
#     try:
#         cursor.execute(""" SELECT * FROM post where id= %s """,(str(id),))
#         data = cursor.fetchone()
#         if not data:
#             raise HTTPException(status_code=404, detail="Item not found")
#         return {"data":data}
#     except BaseException as err:
#         print(err)
#         return("error",err)
    
# @app.delete('/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     try:
#         cursor.execute(""" DELETE FROM post where id= %s RETURNING *""",(str(id),))
#         deleted_post =cursor.fetchone()
#         print(deleted_post)
#         conn.commit()
#         if deleted_post is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
#     except BaseException as err:
#         print(err)
#         return("error",err)
    
# @app.put('/update/{id}',status_code=status.HTTP_200_OK)
# def delete_post(id:int,post:Post):
#     try:
#         cursor.execute(""" Update  post set title= %s ,context=%s ,published= %s where id = %s RETURNING *""",
#                        (post.title,post.context,post.published,str(id)))
#         post =cursor.fetchone()
#         conn.commit()
#         if post is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
#         return {"data":post}
#     except BaseException as err:
#         print(err)
#         return("error",err)




@app.post('/post',status_code=status.HTTP_201_CREATED)
def create_post(post:Post,db: Session = Depends(get_db)):
    try:
        # data=models.Post(title=post.title,content=post.content,published=post.published)
        data=models.Post(**post.dict())
        db.add(data)
        db.commit()
        db.refresh(data)
        
        return{"message":"New post is created","data":data}
    except BaseException as err:
        print(err)
        return{"error",err}




@app.get('/posts',status_code=status.HTTP_200_OK)
def get_all_post(db: Session = Depends(get_db)):
    try:
        data=db.query(models.Post).all()
        
        return {"data":data}
    except BaseException as err:
        print(err)
        return("error",err)
    

@app.get('/post/{id}',status_code=status.HTTP_201_CREATED)
def get_post(id:int,db: Session = Depends(get_db)):
    try:
        data = db.query(models.Post).filter(models.Post.id == id).first()
        if not data:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"data":data}
    except BaseException as err:
        print(err)
        return("error",err)
    


@app.delete('/delete/{id}',status_code=status.HTTP_200_OK)
def delete_post(id:int,db: Session = Depends(get_db)):
    try:
        deleted_post = db.query(models.Post).filter(models.Post.id == id)
        if deleted_post.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        deleted_post.delete(synchronize_session=False)
        db.commit()
        return{"message":"post is Deleted"}    
    except BaseException as err:
        print(err)
        return("error",err)



@app.put('/update/{id}',status_code=status.HTTP_200_OK)
def update_post(id:int,post:Post,db: Session = Depends(get_db)):
    try:
        updated_post = db.query(models.Post).filter(models.Post.id == id)
        db.commit()
        if updated_post.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        updated_post.update(post.dict(),synchronize_session=False)
        db.commit()
        return {"message":"Post is Successfully Updated","data":updated_post.first()}
    except BaseException as err:
        print(err)
        return("error",err)
