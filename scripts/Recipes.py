import ast
import gzip
import pickle
import re

import spacy

nlp = spacy.load('en_core_web_sm')


class Recipes:
  def __init__(self, filename):
    with gzip.open(filename, 'rb') as f:
      self.df = pickle.load(f)
    self.preprocessData()
    
    
  def preprocessData(self):
    self.df.fillna('', inplace=True)
    # convert the string representation of the list of ingredients into an actual list of ingredients
    self.df['ingredients'] = self.df['ingredients'].apply(ast.literal_eval)
    self.df['steps'] = self.df['steps'].apply(ast.literal_eval)
    
  def getRecipes(self):
    return self.df.head(20).to_dict(orient='records')

  
  def preprocess_ingredient(self, ingredient):
    pattern = re.compile(r'\d+\s*\d*\/\d*\s*\w*\s*(?P<ingredient>.+)')
    match = pattern.match(ingredient)
    if match:
        return match.group('ingredient').strip().lower()
    else:
        return ingredient.strip().lower()

  def match_ingredient(self, ingredients, my_ing):
    if not isinstance(ingredients, list):
        return False
    ingredients = [self.preprocess_ingredient(ing) for ing in ingredients]  # preprocess the ingredients
    my_ing = [ing.lower() for ing in my_ing]
    num_matches = sum(1 for ing in ingredients if any(item in ing for item in my_ing))
    return num_matches >= 0.9 * len(my_ing)

  def getRecipesByIngredients(self, my_ing):
    my_ing_lower = [ing.lower() for ing in my_ing]
    df = self.df.copy()
    
    # filter the dataframe based on whether it contains at least 80% of the ingredients in my_ing
    filtered_df = df[df['ingredients'].apply(self.match_ingredient,args=(my_ing_lower,))]
    filtered_df = filtered_df.reset_index(drop=True)
    return filtered_df.to_dict(orient='records')
  
# create main for this class
if __name__ == "__main__":
  recipes = Recipes('data/recipes.pk.gz')
  #my_ing = ['salt', 'pepper', 'onion', 'bell pepper', 'potatoes','shallots','parsley','tarragon','olive oil', 
  #        'cheese','vinegar']
  my_ing = ['winter squash', 'mixed spice', 'honey', 'butter', 'olive oil', 'salt']
  #print(recipes.getRecipesByIngredients(my_ing))
