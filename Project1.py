import pandas as pd

# Load the CSV file from a zip archive

file_path = r"C:\Users\Tanmayy\Downloads\archive.zip"
df = pd.read_csv(file_path, compression='zip')
print(df)

# Display the first few rows of the DataFrame
print(df.head())

# Display the last few rows of the DataFrame
# print(df.tail())

# Display the shape of the DataFrame
print(df.shape)

# Display the columns of the DataFrame
print(df.columns)

# Display the data types of the columns
print(df.dtypes)

# Display the summary statistics of the DataFrame
print(df.describe())

# Display the number of missing values in each column
print(df.isnull().sum())

# Display the unique values in each column
for column in df.columns:
    print(f"Unique values in {column}: {df[column].unique()}")

# Display the number of unique values in each column
print(df.nunique())


numeric_cols = df.select_dtypes(include='number').columns
if len(numeric_cols) > 1:
    print(df[numeric_cols].corr())
else:
    print("Not enough numeric columns for correlation matrix.")


    # Drop rows with missing values (or use fillna if you prefer)
df_cleaned = df.dropna()

# Remove duplicate rows
df_cleaned = df_cleaned.drop_duplicates()

# Standardize column names: lowercase and replace spaces with underscores
df_cleaned.columns = df_cleaned.columns.str.lower().str.replace(' ', '_')

# Check the cleaned data
print("Shape after cleaning:", df_cleaned.shape)
print("Missing values after cleaning:\n", df_cleaned.isnull().sum())
print("Column names after cleaning:\n", df_cleaned.columns)


# Remove unnamed index columns if they exist
df_cleaned = df_cleaned.loc[:, ~df_cleaned.columns.str.contains('^unnamed')]

print("Columns after removing unnamed index columns:\n", df_cleaned.columns)

# Display the first few rows of the cleaned DataFrame
print(df_cleaned.head())


# Sort posts by number of likes (descending)
if 'likes' in df_cleaned.columns:
    top_liked = df_cleaned.sort_values(by='likes', ascending=False)
    print("Top 5 most liked posts:")
    print(top_liked[['text', 'likes']].head())

# Sort posts by number of retweets (descending)
if 'retweets' in df_cleaned.columns:
    top_retweeted = df_cleaned.sort_values(by='retweets', ascending=False)
    print("Top 5 most retweeted posts:")
    print(top_retweeted[['text', 'retweets']].head())

# Create a total engagement column (likes + retweets)
if {'likes', 'retweets'}.issubset(df_cleaned.columns):
    df_cleaned['total_engagement'] = df_cleaned['likes'] + df_cleaned['retweets']
    print("Top 5 posts by total engagement:")
    print(df_cleaned.sort_values(by='total_engagement', ascending=False)[['text', 'total_engagement']].head())

    # Analyze the most frequently used hashtags
if 'hashtags' in df_cleaned.columns:
    hashtags = df_cleaned['hashtags'].str.split(',').explode().str.strip()
    print("Top 10 hashtags:")
    print(hashtags.value_counts().head(10))

    # Sentiment trend by month (or year)
if {'sentiment', 'month', 'year'}.issubset(df_cleaned.columns):
    sentiment_trend = df_cleaned.groupby(['year', 'month'])['sentiment'].value_counts().unstack().fillna(0)
    print("Sentiment trend by year and month:")
    print(sentiment_trend)

    # Posts count by platform
if 'platform' in df_cleaned.columns:
    print("Posts count by platform:")
    print(df_cleaned['platform'].value_counts())






# Top hashtags
if 'hashtags' in df_cleaned.columns:
    hashtags = df_cleaned['hashtags'].str.split(',').explode().str.strip()
    top_hashtags = hashtags.value_counts().head(10)
else:
    top_hashtags = pd.Series(dtype=int)

# Top liked posts
if 'likes' in df_cleaned.columns:
    top_liked = df_cleaned.sort_values(by='likes', ascending=False).head(10)
else:
    top_liked = pd.DataFrame()

# Platform counts
if 'platform' in df_cleaned.columns:
    platform_counts = df_cleaned['platform'].value_counts()
else:
    platform_counts = pd.Series(dtype=int)


#  visualization

import matplotlib.pyplot as plt

# Top 10 hashtags
if 'hashtags' in df_cleaned.columns:
    hashtags = df_cleaned['hashtags'].str.split(',').explode().str.strip()
    top_hashtags = hashtags.value_counts().head(10)
    plt.figure(figsize=(10,5))
    top_hashtags.plot(kind='bar')
    plt.title('Top 10 Hashtags')
    plt.xlabel('Hashtag')
    plt.ylabel('Count')
    plt.show()


    # Top 10 most liked posts
if 'likes' in df_cleaned.columns:
    top_liked = df_cleaned.sort_values(by='likes', ascending=False).head(10)
    plt.figure(figsize=(10,5))
    plt.barh(top_liked['text'], top_liked['likes'])
    plt.title('Top 10 Most Liked Posts')
    plt.xlabel('Likes')
    plt.ylabel('Post')
    plt.gca().invert_yaxis()
    plt.show()


    # Posts count by platform
if 'platform' in df_cleaned.columns:
    platform_counts = df_cleaned['platform'].value_counts()
    plt.figure(figsize=(8,5))
    platform_counts.plot(kind='bar')
    plt.title('Posts Count by Platform')
    plt.xlabel('Platform')
    plt.ylabel('Number of Posts')
    plt.show()


summary = """
Social Media Trend Analysis Report

1. Top Hashtags:
   - The most frequently used hashtags are: {}
   - These hashtags indicate trending topics and user interests.

2. Most Liked Posts:
   - The posts with the highest likes are:
{}
   - These posts represent the most engaging content.

3. Platform Activity:
   - Distribution of posts by platform:
{}
   - This shows which platforms are most active/popular.

Key Insights:
- Hashtags such as {} are driving engagement.
- The majority of posts come from the {} platform.
- Content with high likes often includes trending hashtags.

""".format(
    ', '.join(top_hashtags.index) if not top_hashtags.empty else "N/A",
    top_liked[['text', 'likes']].to_string(index=False) if not top_liked.empty else "N/A",
    platform_counts.to_string() if not platform_counts.empty else "N/A",
    ', '.join(top_hashtags.index[:3]) if not top_hashtags.empty else "N/A",
    platform_counts.idxmax() if not platform_counts.empty else "N/A"
)

print(summary)



