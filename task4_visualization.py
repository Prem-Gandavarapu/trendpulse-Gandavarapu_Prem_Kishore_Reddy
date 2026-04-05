# %%
# ==========================================
# Task 4: Visualizations
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# Step 1: Load data + setup
# -------------------------------

file_path = "data/trends_analysed.csv"

print("Loading analysed data...")
df = pd.read_csv(file_path)

print(f"Data loaded: {df.shape}")

# Create outputs folder if not exists
output_dir = "outputs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# -------------------------------
# Helper: shorten long titles
# -------------------------------
def shorten_title(title, max_len=50):
    if len(title) > max_len:
        return title[:50] + "..."
    return title


# -------------------------------
# Chart 1: Top 10 Stories by Score
# -------------------------------

top_stories = df.sort_values(by="score", ascending=False).head(10)

titles = top_stories["title"].apply(shorten_title)
scores = top_stories["score"]

plt.figure()

plt.barh(titles, scores)
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")

plt.gca().invert_yaxis()  # highest at top

plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.close()


# -------------------------------
# Chart 2: Stories per Category
# -------------------------------

category_counts = df["category"].value_counts()

plt.figure()

plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.xticks(rotation=30)

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.close()


# -------------------------------
# Chart 3: Score vs Comments
# -------------------------------

plt.figure()

# Separate popular vs non-popular
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")

plt.legend()

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()


# -------------------------------
# Bonus: Dashboard
# -------------------------------

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1 (dashboard)
axes[0].barh(titles, scores)
axes[0].set_title("Top Stories")
axes[0].invert_yaxis()

# Chart 2 (dashboard)
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Categories")
axes[1].tick_params(axis='x', rotation=30)

# Chart 3 (dashboard)
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].legend()

plt.suptitle("TrendPulse Dashboard")

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()


print("All charts saved in outputs/ folder")


