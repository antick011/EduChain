import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# Dummy course dataset (you may fetch this from MySQL in production)
courses = pd.DataFrame({
    'course_id': [1, 2, 3, 4],
    'title': ['Python Basics', 'Data Science', 'Web Development', 'Machine Learning'],
    'tags': ['python beginner', 'data science machine learning', 'html css js', 'ml ai deep learning']
})

# Dummy user profile interests (in real app, fetch from DB or user input)
user_profiles = {
    1: 'python machine learning',
    2: 'web frontend html css',
    3: 'data science analytics ai',
}

def get_recommendations(user_id):
    if user_id not in user_profiles:
        return []

    user_interest = user_profiles[user_id]
    
    # Append user interest as a "document"
    all_docs = courses['tags'].tolist() + [user_interest]

    # Vectorize the tags
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(all_docs)

    # Compute cosine similarity
    cosine_sim = cosine_similarity(vectors)

    # Last row is user input vector
    user_sim_scores = cosine_sim[-1][:-1]  # exclude similarity with self

    # Rank courses
    top_indices = np.argsort(user_sim_scores)[::-1]

    recommendations = []
    for idx in top_indices:
        if user_sim_scores[idx] > 0:
            recommendations.append({
                'course_id': int(courses.iloc[idx]['course_id']),
                'title': courses.iloc[idx]['title'],
                'score': float(user_sim_scores[idx])
            })

    return recommendations
