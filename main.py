from scripts.RecipesData import RecipeDataset
from scripts.RecipesRecommendor import RecipeRecommendor
from scripts.clustering import get_similar_recipes, generate_data

if __name__ == "__main__":
    generate_data('./data')
    data = RecipeDataset()

    recipe_recommendor = RecipeRecommendor(data)
    # test_userId = 1545
    test_userId = 2008
    output=get_similar_recipes(test_userId, data.clustering_df,category="Dessert")
    print(output)
    ratings, recipe_ids = recipe_recommendor.__createrecommendations__(author_id=test_userId,
                                                                       recipe_ids=get_similar_recipes(test_userId, data.clustering_df, category="Dessert"),
                                                                       category="Dessert")
    # ratings, recipe_ids = recipe_recommendor.__createrecommendations__(author_id=test_userId,
    #                                                                    recipe_ids=get_similar_recipes(test_userId, data.clustering_df),
    #                                                                    category=None)
    print(f"ratings: {ratings}")
    top_recipe_ids = [recipe_ids[i] for i in sorted(range(len(ratings)), key=lambda i: ratings[i], reverse=True)[:10]] if len(ratings) > 0 else recipe_ids[:10]
    print(top_recipe_ids)
