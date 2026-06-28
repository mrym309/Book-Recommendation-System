import streamlit as st
import pickle
import numpy as np

# Load your pickle files
popular = pickle.load(open('popular.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("📚 Book Recommender System")

# ── Tabs for two sections ──
tab1, tab2 = st.tabs(["🔥 Popular Books", "🔍 Recommend by Book"])

# Tab 1: Popular Books
with tab1:
    st.subheader("Top Popular Books")
    for i in range(len(popular)):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(popular.iloc[i]['Image-URL-M'], width=80)
        with col2:
            st.write(f"*{popular.iloc[i]['Book-Title']}*")
            st.write(f"Author: {popular.iloc[i]['Book-Author']}")
            st.write(f"⭐ Rating: {popular.iloc[i]['avg_rating']}")

# Tab 2: Collaborative Filtering Recommendations
with tab2:
    st.subheader("Find Similar Books")
    book_list = pt.index.tolist()
    selected_book = st.selectbox("Select a book:", book_list)

    if st.button("Recommend"):
        # Get index and similarity scores
        index = np.where(pt.index == selected_book)[0][0]
        similar_items = sorted(
            list(enumerate(similarity[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:6]  # top 5

        st.subheader("You might also like:")
        cols = st.columns(5)
        for i, (idx, score) in enumerate(similar_items):
            book_name = pt.index[idx]
            book_data = books[books['Book-Title'] == book_name].drop_duplicates('Book-Title')
            with cols[i]:
                if not book_data.empty:
                    st.image(book_data.iloc[0]['Image-URL-M'], use_column_width=True)
                    st.caption(book_name)


