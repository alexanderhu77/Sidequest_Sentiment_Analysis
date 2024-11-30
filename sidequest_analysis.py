import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob  
from collections import Counter

file_path = 'sidequest_review_scrape.csv'
df = pd.read_csv(file_path)

#Extract ratings
def extract_ratings(df):
    ratings = {}
    for _, row in df.iterrows():
        url, review = row['url'], row['review']
        if "Rating :" in review:
            try:
                rating = float(review.split(":")[1].strip().split()[0])
                ratings[url] = rating
            except ValueError:
                ratings[url] = None
        elif url not in ratings:
            ratings[url] = None
    return ratings

#Sentiment Analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

def extract_sentiments(df):
    sentiments = {}
    for url, group in df.groupby('url'):
        game_reviews = group['review'].tolist()[2:]  # Skip title and rating
        sentiments[url] = [analyze_sentiment(review) for review in game_reviews if "Rating :" not in review]
    return sentiments

#Plot Ratings onto a Graph
def plot_ratings(ratings):
    filtered_ratings = {url: rating for url, rating in ratings.items() if rating is not None}
    unrated_count = len(ratings) - len(filtered_ratings)
    
    print(f"Number of unrated games: {unrated_count}")
    
    rating_values = list(filtered_ratings.values())
    rating_counts = Counter(rating_values)
    
    ratings = list(rating_counts.keys())
    counts = list(rating_counts.values())
    
    plt.figure(figsize=(8, 5))
    plt.scatter(ratings, counts, color='skyblue', alpha=0.7, edgecolors="w", s=100)
    plt.xlabel("Rating (Stars)")
    plt.ylabel("Number of Games")
    plt.title("Distribution of Game Ratings on Sidequest")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    max_y = max(counts) if counts else 0
    plt.yticks(range(0, max_y + 2, 2))
    plt.show()


def print_sentiment_counts(sentiments):
    
    all_sentiments = [sentiment for sentiment_list in sentiments.values() for sentiment in sentiment_list]
    
    
    sentiment_counts = Counter(all_sentiments)
    
    print(f"Positive: {sentiment_counts.get('Positive', 0)}")
    print(f"Negative: {sentiment_counts.get('Negative', 0)}")
    print(f"Neutral: {sentiment_counts.get('Neutral', 0)}")

# Add sentiment, title, or rating as a new column to the csv
def add_sentiment_column(df):


    def label_review_type(row, is_first_row):

        review = row['review']
        if is_first_row:
            return "Game Title"
        elif "Rating :" in review:
            try:

                
                rating = float(review.split(":")[1].strip().split()[0])
                return f"{rating} stars"
            except ValueError:
                return "Rating not parsed"
        else:
            return analyze_sentiment(review)
    
    df['Review Type'] = [
        label_review_type(row, (i == 0 or df.at[i - 1, 'url'] != row['url']))
        for i, row in df.iterrows()
    ]
    output_file_path = 'sidequest_review_with_sentiment.csv'
    
    
    df.to_csv(output_file_path, index=False)
    print(f"New CSV created with added sentiment information at: {output_file_path}")



ratings = extract_ratings(df)
sentiments = extract_sentiments(df)
plot_ratings(ratings)
print_sentiment_counts(sentiments)
add_sentiment_column(df)
