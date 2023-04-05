from fastapi import FastAPI
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

data = []


def read_data():
    global data
    data = pd.read_csv('./data/recipes.csv')


@app.on_event("startup")
async def startup_event():
    read_data()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/top_categories')
async def get_top_categories():
    top_categories = data['RecipeCategory'].value_counts().head(10).index.tolist()
    return {'top_categories': top_categories}
# @app.get("/data")
# async def get_data():
#     return data
#
#
# @app.post("/data")
# async def add_data(new_data: dict):
#     data.append(new_data)
#     return new_data
