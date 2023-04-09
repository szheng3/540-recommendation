# scripts for performing k-means clustering on cooking time and ingredients for each recipe
import pandas as pd
from sklearn.cluster import KMeans

# read files
print("Start reading files...", end='')
recipes_df = pd.read_csv('../data/recipes.csv')
reviews_df = pd.read_csv('../data/reviews.csv')
print("finished.")

# merge files based on recipe id (we only want recipes that has reviews)
df = pd.merge(reviews_df, recipes_df, on='RecipeId')

# select all relevant columns of the merged dataframe
features = ['CookTime', 'PrepTime', 'TotalTime',
            'Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent', 'SodiumContent',
            'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent',
           ]
df = df[features]

# remove duplicates
df = df[~df.duplicated()]

# reset the index and drop the original index column
df = df.reset_index(drop=True)
print(f'# of rows: {len(df)}')

# fill the NA CookTime value with time 0 ('PT0S')
df['CookTime'].fillna('PT0S', inplace=True)

# function for converting time due to iso 8601 format error
def convert(s):
    time = s[2:s.find('H')]
    if len(time) > 2: 
        days = int(time)//24
        hours = int(time)-days*24
        s = s.replace(time, str(days)+'D'+str(hours))
    return s

# convert CookTime, PrepTime and TotalTime from iso format to timedelta format
print("Start time convertion...", end='')
df['CookTime'] = df['CookTime'].apply(lambda x: pd.to_timedelta(convert(x)).total_seconds())
df['PrepTime'] = df['PrepTime'].apply(lambda x: pd.to_timedelta(convert(x)).total_seconds())
df['TotalTime'] = df['TotalTime'].apply(lambda x: pd.to_timedelta(convert(x)).total_seconds())
print("finished.")

# Use k-means clustering to select ~1,000 possible alike recipes for each selected recipe for training/validation

print("Start k-means clustering on cooking time...", end='')
# select the cooking time features and convert it to numpy
df_cookingtime = df[df.columns[1:4]]
df_cookingtime = df_cookingtime.to_numpy()

# fit the model
k = 1300 # may be modified later
kmeans_cookingtime = KMeans(n_clusters=k, init='k-means++', n_init='auto', tol=1e-4, random_state=540).fit(df_cookingtime) 

# add the cluster labels to the DataFrame
df['label_cooktime'] = kmeans_cookingtime.labels_
print("finished.")

print("Start k-means clustering on ingredients...", end='')
# select the ingredient features and convert it to numpy
df_ingredient = df[df.columns[4:]]
df_ingredient = df_ingredient.to_numpy()

# fit the model
k = 1300 # may be modified later
kmeans_ingredient = KMeans(n_clusters=k, init='k-means++', n_init='auto', tol=1e-4, random_state=540).fit(df_ingredient) 

# add the cluster labels to the DataFrame
df['label_ingredients'] = kmeans_ingredient.labels_
print("finished.")

# save the df in .csv format
df.to_csv('../data/recipes_w_labels.csv', index=False)


