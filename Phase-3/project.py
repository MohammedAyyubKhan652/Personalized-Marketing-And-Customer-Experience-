import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import random
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify

# ----------------- Clustering -----------------
# Sample customer data with user_id, average order value, and monthly visits
customer_data = pd.DataFrame({
    'user_id': ['user_1', 'user_2', 'user_3'],
    'avg_order_value': [120, 300, 150],    # Average purchase amount per order
    'visits_per_month': [10, 5, 8]         # How many times customer visits monthly
})

# Extract relevant features for clustering (excluding user_id)
features = customer_data[['avg_order_value', 'visits_per_month']]

# Create and fit KMeans model to segment customers into 2 groups based on features
kmeans = KMeans(n_clusters=2, random_state=42)
customer_data['segment'] = kmeans.fit_predict(features)  # Assign cluster labels

print("Customer Segments:")
print(customer_data)


# ----------------- Cosine Similarity Recommender -----------------
# User-product rating matrix (rows: users, columns: products)
ratings_df = pd.DataFrame({
    'user_id': ['user_1', 'user_2', 'user_3'],
    'prod_1': [4, 0, 3],  # Ratings, 0 means no rating
    'prod_2': [0, 5, 0],
    'prod_3': [0, 0, 3]
}).set_index('user_id')

# Compute cosine similarity between user rating vectors to find similar users
similarity = cosine_similarity(ratings_df)
similarity_df = pd.DataFrame(similarity, index=ratings_df.index, columns=ratings_df.index)

# Select the target user for whom we want to generate recommendations
target_user = 'user_1'

# Get similarity scores of all other users compared to target_user, exclude target_user itself
similar_users = similarity_df[target_user].drop(target_user).sort_values(ascending=False)

# Identify the most similar user to the target user
top_similar_user = similar_users.idxmax()

print(f"\nTop similar user to {target_user}: {top_similar_user}")

# Get ratings of target user and the most similar user
user_ratings = ratings_df.loc[target_user]
similar_user_ratings = ratings_df.loc[top_similar_user]

# Recommend products rated by the similar user but not yet rated by the target user
recommended_products = similar_user_ratings[(user_ratings == 0) & (similar_user_ratings > 0)]

if not recommended_products.empty:
    recommended_product = recommended_products.idxmax()  # Pick the product with highest rating
    print(f"Recommended product for {target_user}: {recommended_product}")
else:
    print(f"No recommendation available for {target_user}")


# ----------------- Chatbot -----------------
# Predefined response templates for chatbot interactions
intents = {
    "greet": ["Hello!", "Hi there!", "Welcome!"],
    "recommend": ["Try our bestsellers!", "You might love our new arrivals."]
}

def chatbot_response(user_input):
    """
    Basic chatbot function responding with greetings or recommendations
    based on keywords in user input.
    """
    if "recommend" in user_input.lower():
        return random.choice(intents["recommend"])  # Recommend if keyword detected
    return random.choice(intents["greet"])          # Otherwise greet

print("\nChatbot Interaction:")
print("User: Can you recommend something?")
print("Bot:", chatbot_response("Can you recommend something?"))


# ----------------- Encryption -----------------
# Generate a symmetric encryption key for secure data handling
key = Fernet.generate_key()

# Initialize Fernet cipher with the key
cipher = Fernet(key)

# Message (as bytes) to encrypt - sensitive user data example
message = b"Sensitive user preference data"

# Encrypt the message
encrypted = cipher.encrypt(message)

# Decrypt the message back to original
decrypted = cipher.decrypt(encrypted)

print("\nEncrypted:", encrypted.decode())  # Encrypted text (base64)
print("Decrypted:", decrypted.decode())    # Original message


# ----------------- Flask App -----------------
app = Flask(__name__)
click_logs = []  # Store logged events temporarily in memory

@app.route('/log-event', methods=['POST'])
def log_event():
    """
    API endpoint to receive and store user interaction events (e.g., clicks).
    Helps track customer behavior for personalization insights.
    """
    event = request.json
    click_logs.append(event)  # Save event
    print(f"Event logged: {event}")
    return jsonify({"status": "success", "logged": event}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
