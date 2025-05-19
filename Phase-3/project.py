import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import random
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify

# ----------------- Clustering -----------------
customer_data = pd.DataFrame({
    'user_id': ['user_1', 'user_2', 'user_3'],
    'avg_order_value': [120, 300, 150],
    'visits_per_month': [10, 5, 8]
})

features = customer_data[['avg_order_value', 'visits_per_month']]
kmeans = KMeans(n_clusters=2, random_state=42)
customer_data['segment'] = kmeans.fit_predict(features)
print("Customer Segments:")
print(customer_data)

# ----------------- Cosine Similarity Recommender -----------------
ratings_df = pd.DataFrame({
    'user_id': ['user_1', 'user_2', 'user_3'],
    'prod_1': [4, 0, 3],
    'prod_2': [0, 5, 0],
    'prod_3': [0, 0, 3]
}).set_index('user_id')

similarity = cosine_similarity(ratings_df)
similarity_df = pd.DataFrame(similarity, index=ratings_df.index, columns=ratings_df.index)

# Recommend products for user_1 based on similar users
target_user = 'user_1'
similar_users = similarity_df[target_user].drop(target_user).sort_values(ascending=False)
top_similar_user = similar_users.idxmax()

print(f"\nTop similar user to {target_user}: {top_similar_user}")

# Recommend a product rated by the similar user but not yet by the target user
user_ratings = ratings_df.loc[target_user]
similar_user_ratings = ratings_df.loc[top_similar_user]

recommended_products = similar_user_ratings[(user_ratings == 0) & (similar_user_ratings > 0)]
if not recommended_products.empty:
    recommended_product = recommended_products.idxmax()
    print(f"Recommended product for {target_user}: {recommended_product}")
else:
    print(f"No recommendation available for {target_user}")

# ----------------- Chatbot -----------------
intents = {
    "greet": ["Hello!", "Hi there!", "Welcome!"],
    "recommend": ["Try our bestsellers!", "You might love our new arrivals."]
}

def chatbot_response(user_input):
    if "recommend" in user_input.lower():
        return random.choice(intents["recommend"])
    return random.choice(intents["greet"])

print("\nChatbot Interaction:")
print("User: Can you recommend something?")
print("Bot:", chatbot_response("Can you recommend something?"))

# ----------------- Encryption -----------------
key = Fernet.generate_key()
cipher = Fernet(key)
message = b"Sensitive user preference data"
encrypted = cipher.encrypt(message)
decrypted = cipher.decrypt(encrypted)
print("\nEncrypted:", encrypted.decode())
print("Decrypted:", decrypted.decode())

# ----------------- Flask App -----------------
app = Flask(__name__)
click_logs = []

@app.route('/log-event', methods=['POST'])
def log_event():
    event = request.json
    click_logs.append(event)
    print(f"Event logged: {event}")
    return jsonify({"status": "success", "logged": event}), 200

if __name__ == '__main__':
    app.run(debug=True)
