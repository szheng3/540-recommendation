import pandas as pd
from torch.utils.data import Dataset
from sklearn.preprocessing import LabelEncoder
import torch
from torch.utils.data import random_split
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import LabelEncoder

class RecipeDataset(Dataset):
    def __init__(self):
        self.__loaddata__
        self.user_encoder = LabelEncoder()
        self.item_encoder = LabelEncoder()
        self.recipe_ids = self.item_encoder.fit_transform(self.data["RecipeId"].values)
        self.author_ids = self.user_encoder.fit_transform(self.data["AuthorId_y"].values)

        self.ratings = self.data["Rating"].astype(float).values
        self.calories = self.data["Calories"].astype(float).values
        self.review_counts = self.data["ReviewCount"].astype(float).values
        
    def __loaddata__(self):
        reviews_df = pd.read_parquet('data/reviews.parquet')
        recipes_df = pd.read_parquet('data/recipes.parquet')
        self.data = pd.merge(reviews_df, recipes_df, on='RecipeId')

    def __len__(self):
        return len(self.recipe_ids)

    def __getitem__(self, idx):
        recipe_id = self.recipe_ids[idx]
        author_id = self.author_ids[idx]
        rating = self.ratings[idx]
        calories = self.calories[idx]
        review_count = self.review_counts[idx]
        return (recipe_id, author_id, calories, review_count), rating
    
    def __getmaxcaloriesandreviewcount__(self):
        df = self.data[["RecipeId", "AuthorId_y", "Rating", "Calories", "ReviewCount"]]

        # remove duplicates without considering the first column
        df = df[~df.iloc[:, 1:].duplicated(keep='first', subset=df.columns[1:])]

        # reset the index and drop the original index column
        df = df.reset_index(drop=True)
        # Calculate the maximum values for Calories and ReviewCount
        max_calories = int(df["Calories"].max())
        max_review_count = int(df["ReviewCount"].max())
        return max_calories, max_review_count, df
    
    def split(self):
        # Split the dataset into training and validation sets
        train_size = int(0.8 * len(self.data))
        val_size = len(self.data) - train_size
        train_dataset, val_dataset = random_split(self.data, [train_size, val_size])

        # train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

        batch_size = 32
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        valid_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        saved_models_dir = 'saved_models'
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        return train_loader, valid_loader, train_dataset, val_dataset, saved_models_dir, device, batch_size
