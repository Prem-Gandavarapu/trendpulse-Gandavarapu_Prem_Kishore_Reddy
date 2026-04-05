# %%
# ==========================================
# Task 3: Analysis with Pandas & NumPy
# ==========================================

import pandas as pd
import numpy as np

# -------------------------------
# Step 1: Load and Explore Data
# -------------------------------

file_path = "data/trends_clean.csv"

print("Loading cleaned CSV data...")

df = pd.read_csv(file_path)

print(f"Loaded data: {df.shape}\n")

# First 5 rows
print("First 5 rows:")
print(df.head(), "\n")

# Average values
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"Average score   : {int(avg_score)}")
print(f"Average comments: {int(avg_comments)}\n")


# -------------------------------
# Step 2: Analysis using NumPy
# -------------------------------

print("--- NumPy Stats ---")

scores = df["score"].values  # convert to NumPy array

# Basic stats
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

max_score = np.max(scores)
min_score = np.min(scores)

print(f"Mean score   : {int(mean_score)}")
print(f"Median score : {int(median_score)}")
print(f"Std deviation: {int(std_score)}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}\n")

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"Most stories in: {top_category} ({top_count} stories)")

# Most commented story
max_comments_row = df.loc[df["num_comments"].idxmax()]

print(
    f'Most commented story: "{max_comments_row["title"]}" — {max_comments_row["num_comments"]} comments\n'
)


# -------------------------------
# Step 3: Add New Columns
# -------------------------------

# Engagement = comments per upvote (simple ratio)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular flag based on average score
df["is_popular"] = df["score"] > avg_score


# -------------------------------
# Step 4: Save to CSV
# -------------------------------

output_path = "data/trends_analysed.csv"

df.to_csv(output_path, index=False)

print(f"Saved to {output_path}")

# %%



