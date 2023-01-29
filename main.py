import csv

from fastapi import FastAPI
from recommender.recommender import Recommender

plants_data_path = './data/plants_data.csv'
plants_recommender_data_path = './data/plants_recommender.csv'

app = FastAPI()
recommender = Recommender(plants_recommender_data_path)
# read csv file at plants_data_path as a dictionary
with open(plants_data_path, 'r') as f:
    reader = csv.DictReader(f)
    plants_data = list(reader)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/plants")
async def read_plants():
    return plants_data


@app.get("/plants/{plant_id}")
async def read_plant(plant_id: int):
    # return plant with matching id from plants_data
    if plant_id > 0 and plant_id <= len(plants_data):
        return plants_data[plant_id - 1]


@app.get("/recommendations_from_plant/{plant_id}")
async def recommendations_from_plant(plant_id: int):
    return recommender.get_recommendations(plant_id)


@app.get("/recommendations_from_profile/{plant_id}")
async def recommendations_from_profile(plant_id: int):
    return recommender.get_recommendations(plant_id)

# TODO endpoint for getting plant recommendations with user preferences and plant list
