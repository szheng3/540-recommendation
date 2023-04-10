import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import os


class RecipeCluster:
    def __init__(self, recipes_file, reviews_file):
        self.recipes_file = recipes_file
        self.reviews_file = reviews_file

    def read_files(self):
        # Read recipe and review data from CSV files
        print("Start reading files...", end='')
        self.recipes_df = pd.read_csv(self.recipes_file)
        self.reviews_df = pd.read_csv(self.reviews_file)
        print("finished.")

    def preprocess_data(self):
        # Merge the recipes and reviews dataframes based on the recipe ID
        self.df = pd.merge(self.reviews_df, self.recipes_df, on='RecipeId')

        # Select relevant columns from the merged dataframe
        features = ['RecipeId', 'AuthorId_y',
                    'CookTime', 'PrepTime', 'TotalTime',
                    'Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent', 'SodiumContent',
                    'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent',
                    ]
        self.df = self.df[features]

        # Remove duplicate rows
        self.df = self.df[~self.df.duplicated()]

        # Reset the index of the dataframe
        self.df = self.df.reset_index(drop=True)

        # Fill missing CookTime values with 0 seconds
        self.df['CookTime'].fillna('PT0S', inplace=True)

    def convert_time(self, s):
        # Convert the time format to days and hours
        time = s[2:s.find('H')]
        if len(time) > 2:
            days = int(time) // 24
            hours = int(time) - days * 24
            s = s.replace(time, str(days) + 'D' + str(hours))
        return s

    def convert_times(self):
        # Convert CookTime, PrepTime, and TotalTime to seconds
        print("Start time conversion...", end='')
        self.df['CookTime'] = self.df['CookTime'].apply(lambda x: pd.to_timedelta(self.convert_time(x)).total_seconds())
        self.df['PrepTime'] = self.df['PrepTime'].apply(lambda x: pd.to_timedelta(self.convert_time(x)).total_seconds())
        self.df['TotalTime'] = self.df['TotalTime'].apply(
            lambda x: pd.to_timedelta(self.convert_time(x)).total_seconds())
        print("finished.")

    def kmeans_clustering(self, k=1300):
        # Perform k-means clustering on cooking time features
        print("Start k-means clustering on cooking time...", end='')
        df_cookingtime = self.df[self.df.columns[2:5]].to_numpy()
        kmeans_cookingtime = KMeans(n_clusters=k, init='k-means++', n_init='auto', tol=1e-4, random_state=540).fit(
            df_cookingtime)
        self.df['label_cooktime'] = kmeans_cookingtime.labels_
        print("finished.")

        # Perform k-means clustering on ingredient features
        print("Start k-means clustering on ingredients...", end='')
        df_ingredient = self.df[self.df.columns[5:]].to_numpy()
        kmeans_ingredient = KMeans(n_clusters=k, init='k-means++', n_init='auto', tol=1e-4, random_state=540).fit(
            df_ingredient)
        self.df['label_ingredients'] = kmeans_ingredient.labels_
        print("finished.")

    def save_data(self, output_file):
        self.df.to_csv(output_file, index=False)


def get_similar_recipes(user_id):
    df = pd.read_csv('./data/recipes_w_labels.csv')

    # Select the row with the specified user ID
    row = df[df['AuthorId_y'] == user_id]

    # Extract cooktime and ingredients labels
    cooktime_label = row['label_cooktime'].values[0]
    ingredients_label = row['label_ingredients'].values[0]

    # Find recipes with matching cooktime and ingredients labels
    similar_recipes = df[(df['label_cooktime'] == cooktime_label) & (df['label_ingredients'] == ingredients_label)]

    # Return the recipe IDs of similar recipes
    recipe_ids = similar_recipes['RecipeId'].values
    return recipe_ids


def generate_data():
    recipes_file = '../data/recipes.csv'
    reviews_file = '../data/reviews.csv'
    output_file = '../data/recipes_w_labels.csv'
    # Check if the output file already exists
    if not os.path.exists(output_file):
        recipe_cluster = RecipeCluster(recipes_file, reviews_file)
        recipe_cluster.read_files()
        recipe_cluster.preprocess_data()
        recipe_cluster.convert_times()
        recipe_cluster.kmeans_clustering()
        recipe_cluster.save_data(output_file)
    else:
        print(f'{output_file} already exists. Skipping generation.')


if __name__ == "__main__":
    generate_data()
