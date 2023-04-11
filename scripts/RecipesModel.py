import torch


class RecipeModel(torch.nn.Module):
    def __init__(self, num_recipes, num_authors, max_calories, max_review_counts, embedding_dim=16, num_heads=4):
        super().__init__()

        # Initialize embeddings for recipes, authors, calories, and review counts
        self.recipe_embedding = torch.nn.Embedding(num_recipes, embedding_dim)
        self.author_embedding = torch.nn.Embedding(num_authors, embedding_dim)
        self.calorie_embedding = torch.nn.Embedding(max_calories, embedding_dim)
        self.review_count_embedding = torch.nn.Embedding(max_review_counts, embedding_dim)

        # Initialize multihead attention layer
        self.attention = torch.nn.MultiheadAttention(embed_dim=embedding_dim*4, num_heads=num_heads)

        # Initialize fully connected layers
        self.fc1 = torch.nn.Linear(embedding_dim * 4, 16)
        self.fc2 = torch.nn.Linear(16, 1)

        # Initialize the activation function
        self.activation = torch.nn.Sigmoid()

    def forward(self, recipe_id, author_id, calories, review_counts):
        # Get embeddings for the input features
        recipe_embedded = self.recipe_embedding(recipe_id)
        author_embedded = self.author_embedding(author_id)
        calorie_embedded = self.calorie_embedding(calories.long())
        review_count_embedded = self.review_count_embedding(review_counts.long())

        # Concatenate the embeddings along the last dimension
        x = torch.cat([recipe_embedded, author_embedded, calorie_embedded, review_count_embedded], dim=-1)

        # Add a dimension for the sequence length (required for the attention layer)
        x = x.unsqueeze(1)

        # Apply the multihead attention layer
        attn_output, _ = self.attention(x, x, x)

        # Remove the sequence length dimension
        x = attn_output.squeeze(1)

        # Pass the output through the fully connected layers and the activation function
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.activation(x)

        # Scale the output to match the rating range (0 to 5)
        return (x * 5.0).view(-1)
