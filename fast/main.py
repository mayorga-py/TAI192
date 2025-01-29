from fastapi import FastAPI 
app= FastAPI() #crear un objeto
#endpoint home
@app.get("/")
def home():
    return {"message":"bienvenido a FastAPI"}