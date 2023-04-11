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

## Requirements
See `requirements.txt`

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


## Application

This is a Vue.js application that displays recipe recommendations based on user selections. The application uses the vue-router library to manage navigation and has a main app bar at the top of the page. The app bar contains a Log In button that opens a modal where the user can select their username from a dropdown menu. The app retrieves recipe data from an API using the @tanstack/vue-query library and displays it in a grid of recipe cards. The user can filter the recipe results by category by clicking on a category in the left-hand sidebar. The footer of the page provides information about the project and its developers.

## References
