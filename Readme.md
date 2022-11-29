# Plant Recommender App
Web app for the Homeplant Recommender System project in Data Integration 22/23 at WWU Münster

## Installation and Setup

Getting started

### Prerequisites

- Python 3.10
    - We recommend to use [miniforge](https://github.com/conda-forge/miniforge#install) (or [miniconda](https://docs.conda.io/en/latest/miniconda.html)). Since you can manage Python versions and virtual environments with it. Follow the setup steps below if you use miniforge (or miniconda)
    - after successful installation of miniforge (or miniconda) the command `conda` should be available
    - follow the setup guide from step 4 if you use another method of managing virtual environments
- Setup project
    1. `cd` into this directory
    1. Create virtual environment for project: `conda create --name plant-recommender-app python=3.10`
    1. Activate virtual environment of project: `conda activate plant-recommender-app`
    1. Install dependencies into virtual env: `pip install -r requirements.txt`
    1. Run database migrations: `python manage.py migrate`
    1. Start server: `python manage.py runserver`
