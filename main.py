from fastapi import Depends, FastAPI, Body
import schema
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session 
#this wiil create our database if it doesnt already exists

Base.metadata.create_all(engine)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()



@app.get("/")
def getItems(session: Session= Depends(get_session)):
    items = session.query(models.Item).all()
    return items


@app.get("/{id}")
def getItem(id:int, session: Session= Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item


@app.post("/")
def addItem(item:schema.Item, session = Depends(get_session)):
    item = models.Item(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.put("/{id}")
def updateItem(id:int, item:schema.Item, session: Session=Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject

@app.delete("/{id}")
def deleteItem(id:int, session:Session=Depends(get_session)):
    item = session.query(models.Item).get(id)
    session.delete(item)
    session.commit()
    session.close()
    return "Item was deleted"