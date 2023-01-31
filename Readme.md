# Plant Recommender Backend
Web app for the Homeplant Recommender System project in Data Integration 22/23 at WWU Münster

## Installation and Setup

Getting started

### Prerequisites

- Python 3.11
    - We recommend to use [miniforge](https://github.com/conda-forge/miniforge#install) (or [miniconda](https://docs.conda.io/en/latest/miniconda.html)). Since you can manage Python versions and virtual environments with it. Follow the setup steps below if you use miniforge (or miniconda)
    - after successful installation of miniforge (or miniconda) the command `conda` should be available
    - follow the setup guide from step 4 if you use another method of managing virtual environments
- Setup project and install dependencies
    1. `cd` into this directory
    1. Create virtual environment for project: `conda create --name plant-recommender-backend python=3.11`
    1. Activate virtual environment of project: `conda activate plant-recommender-backend`
    1. Install dependencies: `pip install -r requirements.txt`
- Run API server
    1. `cd` into this directory
    1. Activate virtual environment of project: `conda activate plant-recommender-backend`
    1. Run server: `uvicorn main:app --reload`

Data Preparation Stuff (Optional):
- Run scraper: `python scrapers/how_many_plants_scraper.py` -> exports to `scrapers/...`
- Start jupyter server: `jupyter notebook`
