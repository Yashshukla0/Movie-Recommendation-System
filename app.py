import streamlit as st
import pickle
import pandas as pd
import gzip

def recommend(movie):
    movie_idx=movies[movies['title']==movie].index[0]
    distance=similarity[movie_idx]
    movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    recommended=[]
    for i in movie_list:
        recommended.append(movies.iloc[i[0]].title)
    return recommended


similarity=pickle.load(open('similarity.pkl','rb'))
movies_dict=pickle.load(open('movie_dict.pkl','rb'))

with gzip.open('similarity.pkl', 'rb') as ifp:
    similarity=pickle.load(ifp)
with gzip.open('movie_dict.pkl', 'rb') as ifp:
    movie_dict=pickle.load(ifp)


movies=pd.DataFrame(movies_dict)

st.title("Movie Recommendation System")

option =st.selectbox("Select the movie",movies['title'].values)

if st.button("recommend"):
    recommendations=recommend("option")
    for i in recommendations:
       st.write(i)
