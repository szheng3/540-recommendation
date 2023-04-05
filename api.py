from typing import Optional

from fastapi import FastAPI
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import re

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


@app.get("/recipes")
async def get_top_10_popular(category: Optional[str] = None, id: Optional[int] = None):
    # Filter by category if provided
    if category:
        filtered_data = data[data['RecipeCategory'] == category]
    else:
        filtered_data = data
    filtered_data = filtered_data.fillna(0)

    # Filter out the images that have the character '0'
    filtered_data['Images'] = filtered_data['Images'].astype(str)
    filtered_data = filtered_data[~filtered_data['Images'].str.contains('0')]

    def extract_first_image_url(image_col):
        # urls = re.findall(r'https?://[-\w@:%._\+~#=]+(?:\.jpg|\.png)', image_col)
        # urls = re.findall(r'\"https?://.+(?:\.jpg|\.png)\"', image_col.lower())
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', image_col.lower())
        return urls[0] if urls else None

    filtered_data['first_image_url'] = filtered_data['Images'].apply(extract_first_image_url)
    # Sort the dataframe by the "ReviewCount" column in descending order

    sorted_data = filtered_data.sort_values('ReviewCount', ascending=False)

    # Select the top 10 rows
    top_10 = sorted_data.head(6)
    print(top_10['Images'])

    # Return the top 10 rows as a list of dictionaries
    return top_10.to_dict(orient='records')
# @app.get("/data")
# async def get_data():
#     return data
#
#
# @app.post("/data")
# async def add_data(new_data: dict):
#     data.append(new_data)
#     return new_data
