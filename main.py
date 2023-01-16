from flask import Flask, render_template
from flask_compress import Compress
from flask import Flask,request,jsonify
import pandas as pd
from pandas import DataFrame, read_csv;
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
#import flask_restful
from flask_restful import Api

#app = Flask(__name__, static_folder='templates/static')
app = flask.Flask(__name__, template_folder='templates')

Compress(app)
api = Api(app)
app.secret_key = 'secret_key'
@app.route('/recommend.html',methods=['GET','POST'])
def recommend():
    #movie=request.form['movie_name']
    #print(movie)
   # user={
   #     "name" : request.form.get('movie_name', 'nception')

    #}
    #data[0].name = request.form.get('movie_name', 'nception')
    file = r'dataset\movie_list.csv'
    df = pd.read_csv(file)
    file = r'dataset\similarity.csv'
    similarity_table=pd.read_csv(file)
    movie_name2=request.form.get('movie_name', 'Inception')
    if movie_name2 in df['title'].values:
        print(True)
        i= df.loc[df['title']==movie_name2].index[0]
        print(df.loc[i])
        distances = sorted(list(enumerate(similarity_table.loc[i])), reverse=True, key=lambda x: x[1])
        #similar_index_row=list(enumerate(similarity_table[i]))
        #ordering the list in sorted order
        #distance=sorted(similar_index_row,key=lambda  x : x[1],reverse=True)
        closest_distance=distances[0:17]
        final_list_of_movies = []
        for i in range(len(closest_distance)):
            idx=closest_distance[i][0]
            final_list_of_movies.append(df['title'][idx])
    else:
        print(False)
    print(final_list_of_movies)
    df.to_html(header="true", table_id="table")
    #movie_name1= request.form['movie_name']
    #print(movie_name1)
    return render_template('recommend.html', movie_list=final_list_of_movies)
    #return render_template('recommend.html',tables = [df.to_html(classes='data')], titles = df.columns.values)
    #return render_template('recommend.html',movie=movie_name2)
@app.route('/', methods=['GET', 'POST'])
def index_page():
    if flask.request.method == 'GET':
        return (flask.render_template('base.html'))
    #else:
    #    movie_name1 = request.form['movie_name']
    #    print("calling from index_page")
    #    return render_template('recommend.html',movie = movie_name1)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 8000, debug=True)