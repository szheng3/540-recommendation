# Import necessary modules and classes from other script files
from scripts.FetchData import fetchFiles
from scripts.RecipesData import RecipeDataset
from scripts.RecipesRecommendor import RecipeRecommendor
from scripts.clustering import get_similar_recipes

# The main function to run when the script is executed
if __name__ == "__main__":
    # Fetch the required data files from the internet or local storage
    fetchFiles()

    # Create an instance of the RecipeDataset class to hold recipe data
    data = RecipeDataset()

    # Create an instance of the RecipeRecommendor class, using the recipe data
    recipe_recommendor = RecipeRecommendor(data)

    # Set the test user ID for which we want to generate recommendations
    test_userId = 1634

    # Set the recipe category to filter recommendations by
    category = "Dessert"

    # Get similar recipes for the test user based on their preferences and the specified category
    kmeans = get_similar_recipes(test_userId, data.clustering_df, category=category)

    # Create recommendations for the test user by taking into account their preferences, similar recipes, and the specified category
    ratings, recipe_ids = recipe_recommendor.__createrecommendations__(author_id=test_userId,
                                                                       recipe_ids=kmeans,
                                                                       category=category)

    # Get the top 10 recommended recipe IDs based on the ratings
    top_recipe_ids = [recipe_ids[i] for i in sorted(range(len(ratings)), key=lambda i: ratings[i], reverse=True)[:10]]

    # Print the top recipe IDs for the test user
    print("top recipe ids for user: " + str(test_userId))
    print(top_recipe_ids)

    # Set different k values to evaluate the recommendations using Mean Average Precision at k (MAP@k) metric
    k_values = [1, 3, 5, 10]

    # Compute the MAP@k scores for the specified k values
    mapk_scores = recipe_recommendor.evaluate_mapk(k_values)

    # Print the MAP@k scores for each k value
    print(mapk_scores)
