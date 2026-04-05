# %%
# ==========================================
# JSON → DataFrame → Clean → CSV
# ==========================================

import pandas as pd

# -------------------------------
# Step 1: Load JSON file
# -------------------------------
file_path = "data/trends_20260405.json"  # update date if needed

print("Loading JSON file...")
df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories from {file_path}\n")


# -------------------------------
# Step 2: Data Cleaning
# -------------------------------
print("Cleaning data...")

# --- Remove duplicates ---
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# --- Remove missing values ---
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# --- Convert data types ---
df["num_comments"] = df["num_comments"].fillna(0).astype(int)
df["score"] = df["score"].astype(int)

# --- Remove low-quality posts ---
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# --- Clean text ---
df["title"] = df["title"].str.strip()


# -------------------------------
# Step 3: Save to CSV
# -------------------------------
output_path = "data/trends_clean.csv"

df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} rows to {output_path}")


# -------------------------------
# Step 4: Summary
# -------------------------------
print("\nStories per category:")
print(df["category"].value_counts())

# %%



