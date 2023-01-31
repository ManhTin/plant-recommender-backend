import csv
import random

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

# Endpoint definitions


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


@app.get("/plant_pairs")
async def get_plant_pairs():
    return __generate_plant_pairs()


@app.get("/recommendations_for_plant/{plant_id}")
async def recommendations_for_plant(plant_id: int):
    return recommender.get_recommendations_by_id(plant_id)


@app.post("/recommendations_for_profile")
async def recommendations_for_profile(user_profile: dict):
    return recommender.get_recommendations_by_profile(user_profile)


# Helper functions

def __generate_plant_pairs():
    """
    Generate pairs of dissimilar plants for comparison.
    returns a list of dictionaries with keys 'left' and 'right'
    and 1 plant_id per value.
    """
    random_plant_ids = random.sample(range(1, 56), 4)
    plants_for_comparison = []
    compared_plants = []

    for plant_id in random_plant_ids:
        dissimilar_plants = recommender.get_recommendations_by_id(plant_id, similar_first=False)
        # remove plant_ids and compared_plants from dissimilar_plants
        dissimilar_plants = [
            plant for plant in dissimilar_plants if plant not in compared_plants and plant not in random_plant_ids]
        compared_plants.append(dissimilar_plants[0])
        plant_pair = {'left': plant_id, 'right': dissimilar_plants[0]}
        plants_for_comparison.append(plant_pair)

    return plants_for_comparison
