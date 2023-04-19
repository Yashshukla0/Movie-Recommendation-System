from flask import Flask, request,render_template
import pickle
import requests
from patsy import dmatrices
import pandas as pd
movies=pickle.load(open('Model/movie_dict.pkl','rb'))
similarity=pickle.load(open('Model/similarity.pkl','rb'))
def fetch_poster(movie_id):
     url="https://api.themoviedb.org/3/movie/{}?api_key=bd4e6b0c66a04361438fb3434c6e577c".format(movie_id)
     data=requests.get(url)
     data=data.json()
     poster_path=data['poster_path']
     full_path="https://image.tmdb.org/t/p/w500/" + poster_path
     
     return full_path

def recommend(movie):
    movie_idx=movies[movies['title']==movie].index[0]
    distance=similarity[movie_idx]
    movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])
    recommended=[]
    poster=[]
    for i in movie_list[1:6]:
        movie_id=movies.iloc[i[0]].id
        poster.append(fetch_poster(movie_id))
        recommended.append(movies.iloc[i[0]].title)
        
    return recommended,poster

app = Flask(__name__)

@app.route('/')
def home():
     return render_template("index.html")

@app.route('/about')
def about():
     return render_template("about.html")

@app.route('/contact')
def contact():
     return render_template("contact.html")

@app.route('/recommendation' , methods=["GET","POST"])
def  recommendation():
     movie_list=movies['title'].values
     status=False
     if request.method=="POST":
        try:
          movies_name=request.form['movies']
          recommended_movies_name,recommended_movies_poster=recommend(movies_name)
          status=True
          return render_template("recommendation.html", movies_name=recommended_movies_name,movies_poster=recommended_movies_poster, movie_list=movie_list,status=status)

        except Exception as e:
            error={'error':e}
            return render_template('recommendation.html',error=error,movie_list=movie_list,status=status)                        
     else:
         return render_template('recommendation.html',movie_list=movie_list,status=status)

      

if __name__=='__main__':
     app.debug=True
     app.run()