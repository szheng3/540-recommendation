import os
import re
from typing import Optional

import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from scripts.FetchData import fetchFiles
from scripts.RecipesData import RecipeDataset
from scripts.RecipesRecommendor import RecipeRecommendor
from scripts.clustering import get_similar_recipes, generate_data

app = FastAPI()

data = []


def read_data():
    fetchFiles()
    global recipes_df, reviews_df, recipe_data, recipe_recommendor
    recipe_data = RecipeDataset()
    recipes_df = recipe_data.recipes_df
    reviews_df = recipe_data.reviews_df

    recipe_recommendor = RecipeRecommendor(recipe_data)

    # read recipes.parquet file
    # recipes_df = pd.read_parquet('data/recipes.parquet')
    # data = pd.merge(reviews_df, recipes_df, on='RecipeId')


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
    top_categories = recipes_df['RecipeCategory'].value_counts().head(10).index.tolist()
    return {'top_categories': top_categories}


@app.get('/author')
async def get_author():
    top_authors = reviews_df[["AuthorId", "AuthorName"]].drop_duplicates().head(10)
    top_authors_list = top_authors.to_dict(orient="records")

    return {'top_authors': top_authors_list}


@app.get("/recipes")
async def get_top_10_popular(category: Optional[str] = None, userId: Optional[int] = None):
    # Filter by category if provided
    if category:
        filtered_data = recipes_df[recipes_df['RecipeCategory'] == category]
    else:
        filtered_data = recipes_df
    filtered_data = filtered_data.fillna(0)

    # Filter out the images that have the character '0'
    filtered_data['Images'] = filtered_data['Images'].astype(str)
    filtered_data = filtered_data[~filtered_data['Images'].str.contains('0')]

    def extract_first_image_url(image_col):

        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                          image_col.lower())
        return urls[0] if urls else None

    filtered_data['first_image_url'] = filtered_data['Images'].apply(extract_first_image_url)
    # Sort the dataframe by the "ReviewCount" column in descending order

    sorted_data = filtered_data.sort_values('ReviewCount', ascending=False)
    if userId:
        # get the recommended recipe IDs and their corresponding ratings
        recipes_ids = get_similar_recipes(user_id=userId,
                                          df=recipe_data.clustering_df, category=category)
        # print(recipes_ids)
        ratings, recipe_ids = recipe_recommendor.__createrecommendations__(author_id=userId, recipe_ids=recipes_ids,
                                                                           category=category)

        # sort the recipe IDs in descending order of their ratings
        top_recipe_ids = [recipe_ids[i] for i in sorted(range(len(ratings)), key=lambda i: ratings[i], reverse=True)]

        # filter the top 10 recipe IDs and keep their original order
        top_10 = []
        for recipe_id in top_recipe_ids:
            if recipe_id in sorted_data['RecipeId'].tolist():
                top_10.append(sorted_data.loc[sorted_data['RecipeId'] == recipe_id])
                if len(top_10) == 6:
                    break

        # concatenate the dataframes and return the result as a list of dictionaries
        result = pd.concat(top_10).to_dict(orient='records')
        return result

    else:
        # Select the top 10 rows
        top_10 = sorted_data.head(6)

        # Return the top 10 rows as a list of dictionaries
        return top_10.to_dict(orient='records')

static_dir = os.path.join(os.path.dirname(__file__), "dist")
app.mount("/", StaticFiles(directory=static_dir,html=True), name="dist")

if __name__ == "__main__":
    fetchFiles()
    generate_data('./data')
    uvicorn.run(app, host="127.0.0.1", port=8000)
