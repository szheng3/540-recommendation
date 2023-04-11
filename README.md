# Recipes Recommendation System

> #### _Iqra, Shuai, Yilun | Spring '23 | Duke AIPI 540 Recommendation Project_


## Project Description
The goal of this project is to recommend top recipes according to ingredients present in the kitchen and users' liking.

This code implements a recipe recommender system using a neural network. The system is designed to recommend recipes to users based on their past ratings and other users' ratings. The code is based on PyTorch.

![image](https://user-images.githubusercontent.com/44442059/230596869-fdf451c8-6d9d-4ad3-aa82-b55a42e9a6f1.png)


## Data Source
For this project, we are using recipes and reviews data from popular cooking website food network.

The recipes dataset contains 522,517 recipes from 312 different categories. This dataset provides information about each recipe like cooking times, servings, ingredients, nutrition, instructions, and more.
The reviews dataset contains 1,401,982 reviews from 271,907 different users. This dataset provides information about the author, rating, review text, and more.

https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews

## Project Structure
```
.
|-- data                      ----if there is no data, will fetch it from s3 after running main.py or api.py
|-- notebooks      
|   |-- recommendation-2-3.ipynb
|   |-- recommendation.ipynb
|   `-- test.ipynb
|-- saved_models              ----best model will be saved here
|   `-- best_model.pt
|-- scripts
|   |-- FetchData.py          ----fetch data from s3 and unzip it
|   |-- RecipesData.py        ----data processing and loading data to pytorch
|   |-- RecipesModel.py       ----recommendation model here
|   |-- RecipesRecommendor.py ----recommendation including training and evluation
|   `-- clustering.py         ----kmeans clustering
|-- README.md
|-- api.py                    ----demo here run with python3 api.py 
|-- main.py                   ----main app here to run with recommendation system
`-- requirements.txt
```

## Requirements
See `requirements.txt`
>pip3 install -r requirements.txt

### Run the code
>python3 main.py

### Run the web demo
>python3 api.py

open http://127.0.0.1:8000

## Model Training and Evaluation

### Content-based recommendor system
This is a content-based recipe recommender system. It generates recommendations based on the features of recipes (i.e., recipe ID, author ID, number of calories, and number of reviews).

The model is trained using the mean squared error loss function and the Adam optimizer. The training data is split into training and validation datasets, and the model is trained for 10 epochs. The best performing model is saved and later used for generating recommendations.

To generate recommendations, the model is loaded, and the predicted ratings are generated for a set of recipes that the user has not yet rated. The top 10 recipes with the highest predicted ratings are then recommended to the user.

One thing to note is that the model is a neural network model with embeddings and a multi-head attention layer, which are commonly used in natural language processing tasks. The model takes in non-sequential input features, and the attention mechanism is used to focus on relevant features and capture interactions between them.

### Neural Network

This code defines a neural network model for a recipe recommender system. The model takes in four inputs: the recipe ID, the author ID, the number of calories, and the number of reviews for a recipe. The model converts each of these inputs into a lower-dimensional representation called an "embedding". These embeddings are then combined into a single vector and passed through a "multi-head attention" layer that helps the model focus on different parts of the input. Finally, the vector is passed through two fully connected layers and a sigmoid activation function to produce a predicted rating for the recipe.

## Results
![image](https://user-images.githubusercontent.com/50161537/231260130-1bb17a5c-e53c-4e48-901c-7a15dd9de562.jpeg)
This document provides a recommendation on the performance of a model based on its MAP@k (Mean Average Precision at k) scores. The MAP@k scores were computed for k = 1, 3, 5, and 10, and the results are presented below:

* MAP@1: 0.1321
* MAP@3: 0.0865
* MAP@5: 0.0682
* MAP@10: 0.0485

The MAP@k is a popular evaluation metric for ranking models, and it measures the average precision at each cutoff k. In this case, the model's performance decreases as the cutoff k increases, indicating that it is better at identifying the top-ranked items than the lower-ranked ones.

The MAP@1 score of 0.1321 suggests that the model performs reasonably well in identifying the top-ranked item, but there is still room for improvement. The MAP@3 score of 0.0865 indicates that the model's performance drops significantly beyond the first item, suggesting that it may not be as effective in identifying the top three items. The MAP@5 score of 0.0682 and the MAP@10 score of 0.0485 indicate that the model's performance further decreases as more items are considered.

## Application

This is a Vue.js application that displays recipe recommendations based on user selections. The application uses the vue-router library to manage navigation and has a main app bar at the top of the page. The app bar contains a Log In button that opens a modal where the user can select their username from a dropdown menu. The app retrieves recipe data from an API using the @tanstack/vue-query library and displays it in a grid of recipe cards. The user can filter the recipe results by category by clicking on a category in the left-hand sidebar. The footer of the page provides information about the project and its developers.

## References
