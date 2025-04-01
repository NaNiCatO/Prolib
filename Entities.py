from transformers import BertTokenizer, BertModel
import torch
import torch.nn.functional as F

# Load tokenizer & model
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased", output_attentions=True)

# Simulated knowledge base for multi-word and single-word book titles
multi_word_books = {
    "artificial intelligence": ["Artificial Intelligence: A Modern Approach"],
    "deep learning": ["Deep Learning by Ian Goodfellow"],
    "natural language processing": ["Speech and Language Processing"],
}

single_word_books = {
    "ai": ["Artificial Intelligence: A Modern Approach"],
    "python": ["Fluent Python", "Python Crash Course"],
    "data": ["Data Science for Business", "Data Analytics Made Easy"],
    "vision": ["Computer Vision: Algorithms and Applications"],
    "robotics": ["Introduction to Robotics: Mechanics and Control"],
}

# User query
user_query = "Recommend a book on artificial intelligence or deep learning."

# Function to find multi-word entities in the query
def find_multi_word_entities(query, entity_dict):
    found_entities = []
    for phrase in entity_dict.keys():
        if phrase in query.lower():  # Check if phrase exists in query
            found_entities.append(phrase)
    return found_entities

# Detect multi-word book titles in the query
detected_entities = find_multi_word_entities(user_query, multi_word_books)

# Tokenize input
tokens = tokenizer(user_query, return_tensors="pt")

# Get attention scores
outputs = model(**tokens)
attention_scores = outputs.attentions[-1]  # Extract last-layer attention

# Convert token IDs to words
tokens_list = tokenizer.convert_ids_to_tokens(tokens["input_ids"][0])

# Assign importance weights (boosting all words in detected entities)
importance_weights = torch.ones(len(tokens_list))  # Default = 1.0

for entity in detected_entities:
    words = entity.split()  # Split phrase into individual words
    for i, word in enumerate(tokens_list):
        if word in words:
            importance_weights[i] = 1.5  # Boost importance

# Check for single-word entities in the query
for i, word in enumerate(tokens_list):
    if word in single_word_books:
        importance_weights[i] = 1.5  # Boost importance for single-word entities

# Normalize importance scores
importance_weights = importance_weights / importance_weights.mean()

# Modify attention using importance weights
modified_attention = attention_scores.clone()
for head in range(attention_scores.shape[1]):  # Iterate over attention heads
    modified_attention[0, head, :, :] *= importance_weights.unsqueeze(0)

# Renormalize attention using softmax
modified_attention = F.softmax(modified_attention, dim=-1)

# Find the most attended word
max_attention_index = torch.argmax(importance_weights).item()
most_important_word = tokens_list[max_attention_index]

# Match detected multi-word or single-word entity to books
matched_entity = None
if most_important_word in single_word_books:
    matched_entity = most_important_word
else:
    for entity in detected_entities:
        if most_important_word in entity:
            matched_entity = entity
            break

# Recommend books from the matched category
recommended_books = (
    multi_word_books.get(matched_entity, single_word_books.get(matched_entity, ["Sorry, no relevant books found."]))
)

print("Detected Multi-Word Entities:", detected_entities)
print("Recommended Books:", recommended_books)
