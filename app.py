import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Advanced News Aggregator",
    page_icon="📰",
    layout="wide"
)

# --------------------------------------------------
# Custom Styling
# --------------------------------------------------

st.markdown("""
<style>
.main {
    padding: 1rem;
}
.article-card {
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("📰 Advanced News Aggregator")
st.caption("Search, Filter and Explore Latest News")

# --------------------------------------------------
# Sidebar Controls
# --------------------------------------------------

st.sidebar.header("News Settings")

api_key = st.sidebar.text_input(
    "News API Key",
    type="password"
)

country = st.sidebar.selectbox(
    "Location",
    [
        "us",
        "in",
        "gb",
        "au",
        "ca",
        "de",
        "fr",
        "jp"
    ]
)

category = st.sidebar.selectbox(
    "Topic",
    [
        "general",
        "business",
        "technology",
        "sports",
        "health",
        "science",
        "entertainment"
    ]
)

keyword = st.sidebar.text_input(
    "Keyword Search",
    placeholder="AI, Tesla, Cricket..."
)

article_count = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=100,
    value=20
)

# --------------------------------------------------
# Fetch News Function
# --------------------------------------------------

@st.cache_data(ttl=600)
def fetch_news(api_key, country, category, keyword, page_size):

    if keyword.strip():
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={keyword}"
            f"&language=en"
            f"&sortBy=publishedAt"
            f"&pageSize={page_size}"
            f"&apiKey={api_key}"
        )
    else:
        url = (
            f"https://newsapi.org/v2/top-headlines?"
            f"country={country}"
            f"&category={category}"
            f"&pageSize={page_size}"
            f"&apiKey={api_key}"
        )

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    return None


# --------------------------------------------------
# Search Button
# --------------------------------------------------

if st.button("🔍 Fetch News"):

    if not api_key:
        st.error("Please enter API Key")
        st.stop()

    with st.spinner("Fetching latest news..."):

        data = fetch_news(
            api_key,
            country,
            category,
            keyword,
            article_count
        )

        if not data:
            st.error("Failed to retrieve news")
            st.stop()

        articles = data.get("articles", [])

        if len(articles) == 0:
            st.warning("No articles found")
            st.stop()

        st.success(f"Found {len(articles)} articles")

        # ------------------------------------------
        # Summary Table
        # ------------------------------------------

        table_data = []

        for article in articles:
            table_data.append({
                "Title": article.get("title"),
                "Source": article.get("source", {}).get("name"),
                "Published": article.get("publishedAt")
            })

        st.subheader("Article Summary")

        df = pd.DataFrame(table_data)

        st.dataframe(
            df,
            use_container_width=True
        )

        st.divider()

        # ------------------------------------------
        # Article Cards
        # ------------------------------------------

        st.subheader("Latest News")

        for article in articles:

            title = article.get("title", "No Title")
            description = article.get(
                "description",
                "No Description"
            )

            image = article.get("urlToImage")
            url = article.get("url")
            source = article.get(
                "source",
                {}
            ).get("name", "Unknown")

            published = article.get(
                "publishedAt",
                ""
            )

            try:
                published = datetime.strptime(
                    published,
                    "%Y-%m-%dT%H:%M:%SZ"
                ).strftime("%d %b %Y %I:%M %p")
            except:
                pass

            with st.container():

                st.markdown(
                    f"### {title}"
                )

                col1, col2 = st.columns(
                    [1, 2]
                )

                with col1:
                    if image:
                        st.image(
                            image,
                            use_container_width=True
                        )

                with col2:
                    st.write(
                        f"**Source:** {source}"
                    )

                    st.write(
                        f"**Published:** {published}"
                    )

                    st.write(description)

                    st.link_button(
                        "Read Full Article",
                        url
                    )

                st.divider()