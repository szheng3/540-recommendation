import torch


class RecipeModel(torch.nn.Module):
    def __init__(self, num_recipes, num_authors, max_calories, max_review_counts, embedding_dim=16, num_heads=4):
        super().__init__()
        self.recipe_embedding = torch.nn.Embedding(num_recipes, embedding_dim)
        self.author_embedding = torch.nn.Embedding(num_authors, embedding_dim)
        self.calorie_embedding = torch.nn.Embedding(max_calories, embedding_dim)
        self.review_count_embedding = torch.nn.Embedding(max_review_counts, embedding_dim)

        # self.embedding_transform = torch.nn.Linear(embedding_dim * 4, embedding_dim)
        self.attention = torch.nn.MultiheadAttention(embed_dim=embedding_dim*4, num_heads=num_heads)
        # self.fc1 = torch.nn.Linear(embedding_dim * 4, 16)

        self.fc1 = torch.nn.Linear(embedding_dim * 4, 16)
        self.fc2 = torch.nn.Linear(16, 1)
        self.activation = torch.nn.Sigmoid()
        

    def forward(self, recipe_id, author_id, calories, review_counts):
        recipe_embedded = self.recipe_embedding(recipe_id)
        author_embedded = self.author_embedding(author_id)
        calorie_embedded = self.calorie_embedding(calories.long())
        review_count_embedded = self.review_count_embedding(review_counts.long())

        x = torch.cat([recipe_embedded, author_embedded, calorie_embedded, review_count_embedded], dim=-1)
        # x = self.embedding_transform(x)
        
        x = x.unsqueeze(1)

        attn_output, _ = self.attention(x, x, x)
        
        x = attn_output.squeeze(1)

        # x = torch.mean(attn_output, dim=1)  # Compute the mean along the sequence_length dimension

        x = self.fc1(x)
        # x = F.relu(x)
        x = self.fc2(x)
        x = self.activation(x)

        return (x * 5.0).view(-1)
