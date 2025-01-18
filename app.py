from flask import Flask,render_template,request
import pickle
import numpy as np

import os

popular_path = os.path.join(os.path.dirname(__file__), 'popular.pkl')
pt_path = os.path.join(os.path.dirname(__file__), 'pt.pkl')

if os.path.exists(popular_path):
    popular_df = pickle.load(open(popular_path, 'rb'))
else:
    raise FileNotFoundError(f"File not found: {popular_path}")

if os.path.exists(pt_path):
    pt = pickle.load(open(pt_path, 'rb'))
else:
    raise FileNotFoundError(f"File not found: {pt_path}")
import os

books_path = os.path.join(os.path.dirname(__file__), 'books.pkl')
if os.path.exists(books_path):
    books = pickle.load(open(books_path, 'rb'))
else:
    raise FileNotFoundError(f"File not found: {books_path}")
similarity_scores_path = os.path.join(os.path.dirname(__file__), 'similarity_scores.pkl')
if os.path.exists(similarity_scores_path):
    similarity_scores = pickle.load(open(similarity_scores_path, 'rb'))
else:
    raise FileNotFoundError(f"File not found: {similarity_scores_path}")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    if user_input in pt.index:
        index = np.where(pt.index == user_input)[0][0]
    else:
        return render_template('recommend.html', data=[], error="Book not found")
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)