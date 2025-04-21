from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# Load CSV
music_data = pd.read_csv('music_data_with_names.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/genres')
def get_genres():
    genres = music_data['genres'].dropna().unique().tolist()
    return jsonify(genres)

@app.route('/filter')
def filter_songs():
    mood = request.args.get('mood', '')
    genre = request.args.get('genre', '')

    filtered = music_data.copy()
    if mood:
        filtered = filtered[filtered['mood'].str.lower() == mood.lower()]
    if genre:
        filtered = filtered[filtered['genres'].str.lower() == genre.lower()]

    result = filtered[['name', 'genres', 'mood', 'popularity']].replace({np.nan: None}).to_dict(orient='records')
    return jsonify(result)

@app.route('/recommend')
def recommend_songs():
    song = request.args.get('song', '').strip().lower()
    mood = request.args.get('mood', '').strip().lower()
    genre = request.args.get('genre', '').strip().lower()

    base_df = music_data[['name', 'genres', 'mood', 'popularity']].dropna()
    base_df['combined'] = base_df['genres'] + " " + base_df['mood']

    if mood:
        base_df = base_df[base_df['mood'].str.lower() == mood]
    if genre:
        base_df = base_df[base_df['genres'].str.lower() == genre]

    if song and song in base_df['name'].str.lower().values:
        song_index = base_df[base_df['name'].str.lower() == song].index[0]

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(base_df['combined'])

        cosine_sim = cosine_similarity(tfidf_matrix[song_index], tfidf_matrix).flatten()
        similar_indices = cosine_sim.argsort()[-11:-1][::-1]

        recommendations = base_df.iloc[similar_indices][['name', 'genres', 'mood', 'popularity']]
    else:
        recommendations = base_df.sort_values(by='popularity', ascending=False).head(10)[['name', 'genres', 'mood', 'popularity']]

    return jsonify(recommendations.replace({np.nan: None}).to_dict(orient='records'))

@app.route('/collaborative')
def collaborative_recommend():
    song = request.args.get('song', '').strip().lower()
    mood = request.args.get('mood', '').strip().lower()
    genre = request.args.get('genre', '').strip().lower()

    filtered_df = music_data.copy()
    if mood:
        filtered_df = filtered_df[filtered_df['mood'].str.lower() == mood]
    if genre:
        filtered_df = filtered_df[filtered_df['genres'].str.lower() == genre]

    pivot = filtered_df.pivot_table(index='name', columns='mood', values='popularity', fill_value=0)

    if song and song in pivot.index.str.lower().values:
        real_name = pivot.index[[s.lower() == song for s in pivot.index]][0]
        song_vector = pivot.loc[real_name].values.reshape(1, -1)

        similarity_scores = cosine_similarity(song_vector, pivot.values).flatten()
        similar_indices = similarity_scores.argsort()[-11:-1][::-1]
        similar_songs = pivot.index[similar_indices]
        result = filtered_df[filtered_df['name'].isin(similar_songs)][['name', 'genres', 'mood', 'popularity']]
    else:
        result = filtered_df.sort_values(by='popularity', ascending=False).head(10)[['name', 'genres', 'mood', 'popularity']]

    return jsonify(result.replace({np.nan: None}).to_dict(orient='records'))

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=True, port=server_port, host='0.0.0.0')
