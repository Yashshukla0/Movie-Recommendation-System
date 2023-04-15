import streamlit as st
import pickle
import pandas as pd

def recommend(movie):
    movie_idx=movies[movies['title']==movie].index[0]
    distance=similarity[movie_idx]
    movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    recommended=[]
    for i in movie_list:
        recommended.append(movies.iloc[i[0]].title)
    return recommended

# with open('similarity.pkl') as sim:
#     similarity=pickle.load(sim)
# with open("movie_dict.pkl") as tim:
#     movies_dict=pickle.load(tim)
similarity=pickle.load(open('similarity.pkl','rb'))
movies_dict=pickle.load(open('movie_dict.pkl','rb'))
# file = open('similarity.pkl', 'rb')
# similarity = pickle.load(file)
# file.close()

# file = open('movie_dict.pkl', 'rb')
# movie_dict = pickle.load(file)
# file.close()

movies=pd.DataFrame(movies_dict)

st.title("Movie Recommendation System")

option =st.selectbox("Select the movie",movies['title'].values)

if st.button("recommend"):
    recommendations=recommend("option")
    for i in recommendations:
       st.write(i)
