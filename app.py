from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

data = pd.read_csv('netflix_recommendation.csv')

# Initialize the recommendation system
vectorizer = TfidfVectorizer()
all_text_features = vectorizer.fit_transform(data['text'])
all_similarity_matrix = cosine_similarity(all_text_features)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []

    if request.method == 'POST':
        
        # Get user input (title) from the form
        user_input = request.form['title']
        
        user_input = user_input.lower()
        
        content_data = data
        similarity_matrix = all_similarity_matrix
        
        content_index = content_data[content_data['title'].str.lower() == user_input].index

        if len(content_index) == 0:
            return render_template('index.html', recommendations=[], message='This title was not found in the dataset. Please choose another one.')

        content_index = content_index[0]
        
        content_similarity = similarity_matrix[content_index]
        
        similarity_index = pd.DataFrame({'cosine_similarity': content_similarity, 'index': np.arange(len(content_data))})
        
        similarity_index = similarity_index.sort_values(by='cosine_similarity', ascending=False)
        
        top_similar = 10
        
        content_indices = similarity_index['index'].iloc[1:top_similar + 1]
        
        recommendation_content = content_data.iloc[content_indices]
        recommendations = recommendation_content.to_dict(orient='records')

    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
