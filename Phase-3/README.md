## 📌 Features

* **Customer Segmentation**: Uses KMeans clustering to group users based on behavior (e.g., average order value and visits).
* **Product Recommendation**: Applies cosine similarity to recommend products based on similar user preferences.
* **Chatbot System**: Responds to user queries using intent-matching logic.
* **Sentiment Analysis**: Analyzes customer feedback text and classifies it as positive, neutral, or negative.
* **Data Encryption**: Demonstrates secure handling of sensitive user data using Fernet encryption.
* **Event Logging**: Logs user interactions (like clicks or views) via a Flask API.

---

## 🛠 Technologies Used

* **Python**
* **Pandas**, **NumPy** – for data manipulation
* **Scikit-learn** – for clustering and similarity analysis
* **TextBlob** – for sentiment analysis
* **Cryptography (Fernet)** – for encryption
* **Flask** – to build a lightweight API and web interface

---

## ⚙️ How It Works

1. **Customer Segmentation**: The system clusters users into segments using KMeans, based on purchase behavior.
2. **Recommendation System**: Cosine similarity compares user-product ratings and suggests products liked by similar users.
3. **Chatbot**: A simple intent-based chatbot replies to user input with predefined responses.
4. **Sentiment Feedback**: User feedback is analyzed using TextBlob to determine sentiment polarity.
5. **Encryption**: Sensitive data (e.g., preferences) is encrypted to ensure privacy.
6. **Web Dashboard**: A Flask-based dashboard allows users to interact with the chatbot, give feedback, and view recommendations in real-time.

---
