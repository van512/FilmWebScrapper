import streamlit as st   # type: ignore
import pandas as pd      # type: ignore
#import seaborn as sns                #add to requirements.txt if I use it
#import matplotlib.pyplot as plt      #same
import plotly.express as px # type: ignore

st.set_page_config(page_title="🎬 Film & People Explorer", layout="wide")

# Load data
@st.cache_data
def load_data():
    movies = pd.read_csv('data/movies.csv')
    people = pd.read_csv('data/people.csv')
    return movies, people

movies, people = load_data()


# helper function
def filter_by_multi_select(df, column, selected_values):
    if not selected_values:
        return df
    df[column] = df[column].fillna('')
    return df[df[column].apply(lambda x: any(val in x for val in selected_values))]


st.title("🎬 Movie & People Metadata Explorer")

# --- Sidebar ---
# having both movie and people filters in the sidebar is a little counterintuitive 
with st.sidebar: 
    st.header("🎛️ Filters")

    # Movie Filters
    st.subheader("🎞️ Movie Filters")
    genres = sorted(set(g for genre_list in movies['genres'].dropna() for g in genre_list.split(', ')))
    selected_genres = st.multiselect("Genres", genres)

    watch_providers = sorted(set(p for provider_list in movies['watch_providers'].dropna() for p in provider_list.split(', ')))
    selected_providers = st.multiselect("Providers", watch_providers)

    years = movies['release_year'].dropna().astype(int)
    min_year, max_year = int(years.min()), int(years.max())
    year_range = st.slider("Release Year", min_year, max_year, (min_year, max_year))

    # People Filters
    st.subheader("👥 People Filters")
    roles = people['role'].unique().tolist()
    selected_role = st.selectbox("Role", roles)
    min_years_active = st.slider("Minimum Years Active", 0, 60, 5)

# --- Movie Data Filter ---
filtered_movies = movies.copy()
filtered_movies = filter_by_multi_select(filtered_movies, 'genres', selected_genres)
filtered_movies = filter_by_multi_select(filtered_movies, 'watch_providers', selected_providers)

filtered_movies = filtered_movies[
    filtered_movies['release_year'].astype(int).between(year_range[0], year_range[1])
]

# --- People Data Filter ---
filtered_people = people[
    (people['role'] == selected_role) &
    (people['years_active'].fillna(0) >= min_years_active)
]

# --- Main Content ---
tab1, tab2, tab3 = st.tabs(["🎞️ Movies", "👥 People", "📈 Visual Analytics"])

# --- Movies Tab ---
with tab1:
    st.subheader(f"🎥 {len(filtered_movies)} Movies Matching Filters")
    st.dataframe(filtered_movies[['title', 'release_year', 'genres', 'revenue', 'vote_average', 'runtime']]) # fix the horizontal scroll

    st.markdown("### Revenue vs. Vote Average")
    st.markdown("trying out a scatter plot")
    fig1 = px.scatter(
        filtered_movies,
        x='vote_average',
        y='revenue',
        hover_name='title',
        labels={'vote_average': 'TMDb Score', 'revenue': 'Revenue'}, #check currency of revenue
        height=500
    )
    st.plotly_chart(fig1, use_container_width=True)

# --- People Tab ---
with tab2:
    st.subheader(f"👤 {len(filtered_people)} {selected_role}s with ≥ {min_years_active} Years Active")
    st.dataframe(filtered_people[['person_name', 'debut_year', 'years_active', 'last_five_films']]) # fix the horizontal scroll

# --- Visual Analytics Tab ---
with tab3:
    st.subheader("📊 Analytics")

    st.markdown("maybe do some data analysis here")
