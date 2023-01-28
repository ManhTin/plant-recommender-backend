from fastapi import FastAPI
from recommender.recommender import Recommender

app = FastAPI()
recommender = Recommender()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/recommendation/{plant_id}")
async def read_plant(plant_id: int):
    return recommender.get_recommendations(plant_id).to_dict()
