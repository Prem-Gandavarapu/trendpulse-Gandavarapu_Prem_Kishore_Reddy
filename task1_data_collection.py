# %%
import requests
import json
import time
from datetime import datetime
import os

# ================================
# Setup: Create output directory
# ================================
# Ensures "data/" folder exists to store output JSON
os.makedirs("data", exist_ok=True)

# ================================
# API Endpoints
# ================================
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# ================================
# Category Definitions (Keyword-based)
# ================================
# Each category contains keywords used to classify stories
categories = {
    "AI": [
        "ai", "artificial intelligence", "gpt", "llm", "ml",
        "machine learning", "deep learning", "neural", "openai"
    ],
    "Programming": [
        "python", "java", "javascript", "typescript", "c++",
        "rust", "golang", "code", "developer", "software",
        "api", "backend", "frontend", "framework", "library"
    ],
    "Startups": [
        "startup", "funding", "venture", "vc", "founder",
        "company", "product", "business", "market", "growth"
    ],
    "Science": [
        "science", "research", "study", "physics", "biology",
        "chemistry", "space", "nasa", "climate", "medicine"
    ],
    "Security": [
        "security", "cyber", "hack", "breach", "malware",
        "vulnerability", "exploit", "privacy", "attack"
    ]
}

# ================================
# Category Priority Order
# ================================
# Ensures more important/specific categories are matched first
priority = ["Security", "AI", "Science", "Startups", "Programming"]

# ================================
# Data Storage Structure
# ================================
# Dictionary to store 25 stories per category
category_data = {key: [] for key in categories}


# ================================
# Function: Fetch Top Story IDs
# ================================
def fetch_top_story_ids():
    """
    Fetch list of top story IDs from Hacker News API
    """
    response = requests.get(TOP_STORIES_URL)
    return response.json()


# ================================
# Function: Fetch Individual Story
# ================================
def fetch_story(story_id):
    """
    Fetch story details using story ID
    Includes retry mechanism (3 attempts)
    """
    for _ in range(3):
        try:
            res = requests.get(ITEM_URL.format(story_id), timeout=5)
            res.raise_for_status()
            return res.json()
        except:
            # Wait before retrying (handles API/network issues)
            time.sleep(0.5)
    return None


# ================================
# Function: Categorize Story Title
# ================================
def get_category(title):
    """
    Assign category based on keywords in title
    Uses priority order to resolve overlaps
    """
    title = title.lower()

    for cat in priority:
        if any(f" {k} " in f" {title} " for k in categories[cat]):
            return cat

    return None  # No matching category


# ================================
# Function: Extract Required Fields
# ================================
def extract_fields(story, category):
    """
    Extract and structure required fields from story data
    """
    return {
        "post_id": story.get("id"),
        "title": story.get("title"),
        "category": category,
        "score": story.get("score"),
        "num_comments": story.get("descendants"),
        "author": story.get("by"),
        "collected_at": datetime.now().isoformat()
    }


# ================================
# Main Execution Function
# ================================
def main():
    # Step 1: Fetch all top story IDs
    story_ids = fetch_top_story_ids()

    # Temporary pool for unmatched stories (fallback)
    fallback_pool = []

    # Step 2: Fetch and classify stories
    for story_id in story_ids:
        story = fetch_story(story_id)

        # Skip invalid or incomplete stories
        if not story or not story.get("title"):
            continue

        category = get_category(story["title"])

        # Store story in category if space available (max 25)
        if category and len(category_data[category]) < 25:
            category_data[category].append(extract_fields(story, category))
        else:
            # Store for fallback use later
            fallback_pool.append(story)

        # Stop early if all categories have 25 stories
        if all(len(v) >= 25 for v in category_data.values()):
            break

        # Small delay to avoid API rate limiting
        time.sleep(0.2)

    # Step 3: Fill remaining slots using fallback pool
    for category in categories:
        while len(category_data[category]) < 25 and fallback_pool:
            story = fallback_pool.pop()

            if not story or not story.get("title"):
                continue

            category_data[category].append(
                extract_fields(story, category)
            )

    # Step 4: Combine all categories into one list
    final_data = []
    for category in categories:
        final_data.extend(category_data[category][:25])

    # Step 5: Save data to JSON file
    date_str = datetime.now().strftime("%Y%m%d")
    file_path = f"data/trends_{date_str}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4)

    # Final output message
    print(f"Collected {len(final_data)} stories. Saved to {file_path}")


# ================================
# Entry Point
# ================================
if __name__ == "__main__":
    main()

# %%
# ==========================================
# JSON Data Validation (WITHOUT PANDAS)
# ==========================================

import json
import pprint

# -------------------------------
# Step 1: Load JSON file
# -------------------------------
file_path = "data/trends_20260405.json"  # update if needed

print("📂 Loading JSON file...")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("✅ File loaded successfully!\n")


# -------------------------------
# Step 2: Basic checks
# -------------------------------
print("🔍 Basic Information:")
print("Total Records:", len(data))
print("Sample Keys:", data[0].keys(), "\n")


# -------------------------------
# Step 3: Pretty print sample record
# -------------------------------
print("🧾 Sample Record:")
pprint.pprint(data[0])
print("\n")


# -------------------------------
# Step 4: Check missing critical fields
# -------------------------------
print("⚠️ Checking for missing critical fields...")

missing_count = 0

for story in data:
    if not story.get("title") or not story.get("author"):
        missing_count += 1

print("Missing Title/Author:", missing_count, "\n")


# -------------------------------
# Step 5: Category distribution
# -------------------------------
print("📊 Category Distribution:")

category_count = {}

for story in data:
    cat = story.get("category", "Unknown")
    category_count[cat] = category_count.get(cat, 0) + 1

for cat, count in category_count.items():
    print(f"{cat}: {count}")

print()


# -------------------------------
# Step 6: Data quality checks
# -------------------------------
print("🔎 Data Quality Checks:")

no_comments = sum(1 for s in data if not s.get("num_comments"))
low_score = sum(1 for s in data if s.get("score", 0) < 10)

print("Stories with no comments:", no_comments)
print("Stories with low score (<10):", low_score, "\n")


# -------------------------------
# Step 7: Final validation summary
# -------------------------------
print("🎯 Final Validation Summary:")

if len(data) >= 100:
    print("✔ Enough records collected")
else:
    print("❌ Not enough records")

if missing_count == 0:
    print("✔ No missing critical fields")
else:
    print("⚠️ Some missing fields found")

if all(count >= 25 for count in category_count.values()):
    print("✔ Balanced categories")
else:
    print("⚠️ Categories may be imbalanced")

print("\n✅ JSON validation completed!")


