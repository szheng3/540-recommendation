from scripts.RecipesData import RecipeDataset
from scripts.RecipesRecommendor import RecipeRecommendor
from scripts.clustering import get_similar_recipes

if __name__ == "__main__":
    recipe_recommendor = RecipeRecommendor(RecipeDataset())
    test_userId = 1545
    # generate_data()
    ratings, recipe_ids = recipe_recommendor.__createrecommendations__(test_userId,  get_similar_recipes(test_userId))
    top_recipe_ids = [recipe_ids[i] for i in sorted(range(len(ratings)), key=lambda i: ratings[i], reverse=True)[:10]]
    print(top_recipe_ids)
