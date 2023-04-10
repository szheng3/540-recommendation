from scripts.RecipesModel import RecipeModel
import os
import torch
from torch.utils.data import DataLoader

from scripts.RecipesModel import RecipeModel
import numpy as np


class RecipeRecommendor:

    def __init__(self, data):
        self.data = data
        max_calories, max_review_count, self.df = self.data.__getmaxcaloriesandreviewcount__()
        self.model = RecipeModel(num_recipes=len(self.data.item_encoder.classes_) + 1,
                                 num_authors=len(self.data.user_encoder.classes_) + 1,
                                 max_calories=max_calories + 1,
                                 max_review_counts=max_review_count + 1)

        self.train_loader, self.valid_loader, self.train_dataset, self.val_dataset, self.saved_models_dir, self.device, self.batch_size = self.data.split()
        self.model.load_state_dict(torch.load(f"{self.saved_models_dir}/best_model.pt", map_location=self.device))
        self.model = self.model.to(self.device)  # Send model to GPU if available

    def __train__(self):
        # Initialize the best validation loss to a large value
        best_valid_loss = float('inf')

        # Create a directory for the saved models if it doesn't exist
        os.makedirs(self.saved_models_dir, exist_ok=True)
        # RecipeModel(num_recipes=data.loc[:,'RecipeId'].max()+1, num_authors=data.loc[:,"AuthorId_y"].max()+1)
        model = self.model.to(self.device)  # Send model to GPU if available

        criterion = torch.nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        num_epochs = 10
        for epoch in range(num_epochs):
            model.train()
            train_loss = 0
            for batch, targets in self.train_loader:
                optimizer.zero_grad()
                batch = [b.to(self.device) for b in batch]
                targets = targets.float().to(self.device)
                preds = model(*batch)

                loss = criterion(preds, targets)
                loss.backward()
                optimizer.step()
                train_loss += loss.item() * batch[0].shape[0]
            train_loss /= len(self.train_dataset)

            model.eval()
            valid_loss = 0
            with torch.no_grad():
                for batch, targets in self.valid_loader:
                    batch = [b.to(self.device) for b in batch]
                    targets = targets.float().to(self.device)
                    preds = model(*batch)
                    loss = criterion(preds, targets)
                    valid_loss += loss.item() * batch[0].shape[0]
                valid_loss /= len(self.val_dataset)

            print(f"Epoch {epoch + 1}/{num_epochs}, Train Loss: {train_loss:.4f}, Valid Loss: {valid_loss:.4f}")

            # Check if the current validation loss is lower than the best validation loss
            if valid_loss < best_valid_loss:
                best_valid_loss = valid_loss
                print(f"Validation loss improved. Saving the model to {self.saved_models_dir}/best_model.pt")
                torch.save(model.state_dict(), f"{self.saved_models_dir}/best_model.pt")

    def __createrecommendations__(self, author_id, recipe_ids=None, category=None):
        # self.model.load_state_dict(torch.load(f"{self.saved_models_dir}/best_model.pt",map_location=self.device))
        # model = self.model.to(self.device)  # Send model to GPU if available

        df = self.df
        if category:
            df = df[df['RecipeCategory'] == category]
        else:
            df = df

        print(df.head(10))
        print(f"# of rows of df: {len(df)}")
        if recipe_ids is None:
            recipe_ids = df["RecipeId"].unique()[:1000]
        else:
            recipe_ids = recipe_ids
            
        user_has_ratings = author_id in df["AuthorId_x"].values

        if user_has_ratings:
            user_rated_recipe_ids = df[df["AuthorId_x"] == author_id]["RecipeId"].unique()
        else:
            user_rated_recipe_ids = []

        # Create a recommendation dataset
        recommendation_data = []
        for recipe_id in recipe_ids:
            if not user_has_ratings or (user_has_ratings and recipe_id not in user_rated_recipe_ids):
                if not len(df[df["RecipeId"] == recipe_id]): continue
                recipe_data = df[df["RecipeId"] == recipe_id].iloc[0]
                recipe_id_transformed = self.data.item_encoder.transform([recipe_id])[0]
                recommendation_data.append(
                    (recipe_id_transformed, author_id, recipe_data["Calories"], recipe_data["ReviewCount"]))

        recommendation_dataset = [(torch.tensor(a).to(self.device), torch.tensor(b).to(self.device),
                                   torch.tensor(c).to(self.device), torch.tensor(d).to(self.device)) for a, b, c, d in
                                  recommendation_data]
        recommendation_loader = DataLoader(recommendation_dataset, batch_size=self.batch_size, shuffle=False)
        # Model evaluation
        self.model.eval()
        with torch.no_grad():
            ratings = []
            for inputs in recommendation_loader:
                rating = self.model(*inputs)
                ratings.extend(rating.detach().cpu().numpy())
        return ratings, recipe_ids


    def apk(self, actual, predicted, k=10):
        if len(predicted) > k:
            predicted = predicted[:k]

        score = 0.0
        num_hits = 0.0

        for i, p in enumerate(predicted):
            if p in actual and p not in predicted[:i]:
                num_hits += 1.0
                score += num_hits / (i + 1.0)

        if not actual:
            return 0.0

        return score / min(len(actual), k)

    def mapk(self, actual, predicted, k=10):
        return np.mean([self.apk(a, p, k) for a, p in zip(actual, predicted)])

    def evaluate_mapk(self, k_values):
        mapk_scores = []

        for k in k_values:
            actual = []
            predicted = []

            with torch.no_grad():
                for batch, targets in self.valid_loader:
                    batch = [b.to(self.device) for b in batch]
                    targets = targets.float().to(self.device)
                    preds = self.model(*batch)

                    actual.append(list(targets.detach().cpu().numpy()))
                    predicted.append(list(np.argsort(-preds.detach().cpu().numpy())))

            mapk_score = self.mapk(actual, predicted, k=k)
            mapk_scores.append(mapk_score)
            print(f"MAP@{k}: {mapk_score:.4f}")

        return mapk_scores