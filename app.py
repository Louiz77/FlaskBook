from flask import Flask, render_template, request
import pandas as pd
from sklearn import neighbors
from sklearn.preprocessing import MinMaxScaler

def BookRecommender(book_name, new_book):
    try:
        df = pd.read_csv('books.csv', on_bad_lines='skip')
        df2 = df.copy()

        df2.loc[(df2['average_rating'] >= 0) & (df2['average_rating'] <= 1), 'rating_between'] = "between 0 and 1"
        df2.loc[(df2['average_rating'] > 1) & (df2['average_rating'] <= 2), 'rating_between'] = "between 1 and 2"
        df2.loc[(df2['average_rating'] > 2) & (df2['average_rating'] <= 3), 'rating_between'] = "between 2 and 3"
        df2.loc[(df2['average_rating'] > 3) & (df2['average_rating'] <= 4), 'rating_between'] = "between 3 and 4"
        df2.loc[(df2['average_rating'] > 4) & (df2['average_rating'] <= 5), 'rating_between'] = "between 4 and 5"

        rating = pd.get_dummies(df2['rating_between'])
        lang = pd.get_dummies(df2['language_code'])

        features = pd.concat([rating,
                              lang,
                              df2['average_rating'],
                              df2['ratings_count']

                              ], axis=1)

        scaler = MinMaxScaler()

        features = scaler.fit_transform(features)

        model = neighbors.NearestNeighbors(n_neighbors=6, algorithm='ball_tree')
        model.fit(features)
        dist, idlist = model.kneighbors(features)

        book_list_name = []
        book_id = df2[df2['title'] == book_name].index
        book_id = book_id[0]
        for newid in idlist[book_id]:
            book_list_name.append(df2.loc[newid].title)
            book_list_name = new_book
        return book_list_name
    except Exception as e:
        return e


app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def main():
    book = []
    new_book = []
    name = "Louiz"
    age = 21
    data = pd.read_csv('books.csv', sep = ',', on_bad_lines='skip')
    titles = pd.read_csv('books.csv', on_bad_lines='skip')
    if request.method == "POST":
        if request.form.get("book") in book:
            pass
        elif request.form.get("book"):
            book.append(request.form.get("book"))
            BookRecommender(book[0], new_book)
    return render_template("index.html",
                           name=name,
                           age=age,
                           book=book,
                           new_book=new_book,
                           data=data,
                           titles=titles
                           )

@app.route('/sobre')
def sobre():
    notas = {"A culpa é das estrelas": 4.5, "The Witcher Vol 2": 5.0,"Harry Potter Vol 1": 4.2,"Star Wars - Contos Vol 1": 3.9, "Livro de economia": 3.5}
    return render_template("sobre.html", notas=notas)