import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

CATEGORIES = {
    "politics": ["election", "president", "law", "policy"],
    "economy":  ["money", "stock", "market", "trade"],
    "technology": ["tech", "software", "internet", "computer"],
    "health": ["health", "virus", "medicine", "hospital"],
    "entertainment": ["music", "film", "movie", "celebrity"]
}

def load_dataset(fake_path, true_path):
    df_fake = pd.read_csv(fake_path, names=["title", "text", "subject", "date"])
    df_fake["label"] = "fake"

    df_true = pd.read_csv(true_path, names=["title", "text", "subject", "date"])
    df_true["label"] = "true"

    return pd.concat([df_fake, df_true], ignore_index=True)

data = load_dataset("Fake.csv", "True.csv")

def categorize_data(df):
    category_results = {cat: {"true": [], "fake": []} for cat in CATEGORIES}
    for idx, row in df.iterrows():
        text = f"{row['title']} {row['text']}".lower()
        for cat, keywords in CATEGORIES.items():
            if any(k.lower() in text for k in keywords):
                category_results[cat][row["label"]].append(idx)
    return category_results

categories = categorize_data(data)

def search_data_all(df, phrase):
    """
    Return *all* matching articles sorted by similarity to 'phrase'
    so we can count how many are true/fake across the entire dataset.
    """
    documents = df["title"].fillna("") + " " + df["text"].fillna("")
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(documents)
    user_query_vec = tfidf.transform([phrase])
    cosine_similarities = linear_kernel(user_query_vec, tfidf_matrix).flatten()
    # Sort indices by descending similarity
    sorted_indices = cosine_similarities.argsort()[::-1]
    return df.iloc[sorted_indices]

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Article Categorizer & Search"),
    html.H3("Category Overview"),
    html.Ul([
        html.Li(f"{cat} - TRUE: {len(idx_dict['true'])}, FAKE: {len(idx_dict['fake'])}")
        for cat, idx_dict in categories.items()
    ]),

    html.Label("Number of Results:"),
    dcc.Slider(
        id="results-slider",
        min=1,
        max=10,
        step=1,
        value=5,
        marks={i: str(i) for i in range(1, 11)}
    ),
    html.H3("Search Articles"),
    dcc.Input(
        id="search-input",
        type="text",
        placeholder="Enter a search phrase",
        style={"width": "300px"}
    ),
    html.Button("Search", id="search-button"),
    html.Div(id="search-results")
])

@app.callback(
    Output("search-results", "children"),
    Input("search-button", "n_clicks"),
    State("search-input", "value"),
    State("results-slider", "value")
)
def update_search_results(n_clicks, value, top_n):
    if not n_clicks or not value:
        return "Enter a phrase to search."

    # Get all matches, sorted by relevance
    all_results_df = search_data_all(data, value)
    total_count = len(all_results_df)
    count_true_total = (all_results_df["label"] == "true").sum()
    count_fake_total = (all_results_df["label"] == "fake").sum()

    # Slice only the top N for display
    display_results_df = all_results_df.head(top_n)  

    results_list = [
        html.P(
            f"Total matches for '{value}': {total_count} "
            f"({count_true_total} true, {count_fake_total} fake). "
            f"Displaying top {top_n} results below."
        )
    ]
    for _, row in display_results_df.iterrows():
        snippet = str(row["text"])[:250].replace("\n", " ").strip() + "..."
        results_list.append(
            html.Div([
                html.H4(f"{row['title']} ({row['label'].upper()})"),
                html.P(snippet)
            ])
        )
    return results_list

if __name__ == "__main__":
    app.run(debug=True)