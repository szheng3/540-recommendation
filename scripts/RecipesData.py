import pandas as pd
import torch
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import Dataset, DataLoader
from torch.utils.data import random_split

from scripts.clustering import generate_data


class RecipeDataset(Dataset):
    def __init__(self):
        # Load data from CSV files and preprocess it
        self.__loaddata__()

        # Initialize encoders for user and item IDs
        self.user_encoder = LabelEncoder()
        self.item_encoder = LabelEncoder()

        # Encode the user and item IDs
        self.recipe_ids = self.item_encoder.fit_transform(self.data["RecipeId"].values)
        self.author_ids = self.user_encoder.fit_transform(self.data["AuthorId_x"].values)

        # Convert data types of ratings, calories, and review counts
        self.ratings = self.data["Rating"].astype(float).values
        self.calories = self.data["Calories"].astype(float).values
        self.review_counts = self.data["ReviewCount"].astype(float).values

    def __loaddata__(self):
        # Load data from CSV files
        self.reviews_df = pd.read_csv('./data/reviews.csv')
        self.recipes_df = pd.read_csv('./data/recipes.csv')

        # Merge data based on RecipeId
        self.data = pd.merge(self.reviews_df, self.recipes_df, on='RecipeId')

        # Generate clustering dataframe for recipes
        clustering_df = generate_data('./data')
        clustering_df = clustering_df[['RecipeId', 'label_cooktime', 'label_ingredients']]

        # Merge clustering data with the main data
        self.clustering_df = pd.merge(self.data, clustering_df, on='RecipeId')

    def __len__(self):
        # Return the total number of records in the dataset
        return len(self.recipe_ids)

    def __getitem__(self, idx):
        # Get the data for a specific index
        recipe_id = self.recipe_ids[idx]
        author_id = self.author_ids[idx]
        rating = self.ratings[idx]
        calories = self.calories[idx]
        review_count = self.review_counts[idx]

        # Return the data as a tuple
        return (recipe_id, author_id, calories, review_count), rating

    def __getmaxcaloriesandreviewcount__(self):
        # Get the unique records from the dataset
        df = self.data[["RecipeId", "AuthorId_x", "Rating", "Calories", "ReviewCount", "RecipeCategory"]]

        # Remove duplicates without considering the first column
        df = df[~df.iloc[:, 1:].duplicated(keep='first', subset=df.columns[1:])]

        # Reset the index and drop the original index column
        df = df.reset_index(drop=True)

        # Calculate the maximum values for Calories and ReviewCount
        max_calories = int(df["Calories"].max())
        max_review_count = int(df["ReviewCount"].max())

        # Sort the dataframe based on review count
        df = df.sort_values('ReviewCount', ascending=False)

        # Return maximum values and the sorted dataframe
        return max_calories, max_review_count, df

    def split(self):
        # Split the dataset into training and validation sets
        train_size = int(0.8 * len(self))
        val_size = len(self.data) - train_size
        train_dataset, val_dataset = random_split(self, [train_size, val_size])

        # Set the batch size for DataLoader
        batch_size = 32

        # Create DataLoader instances for training and validation datasets
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        valid_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

        # Set the directory to save model checkpoints
        saved_models_dir = './saved_models'

        # Determine the device to use for training (GPU or CPU)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Return the DataLoader instances, datasets, saved models directory, device, and batch size
        return train_loader, valid_loader, train_dataset, val_dataset, saved_models_dir, device, batch_size

