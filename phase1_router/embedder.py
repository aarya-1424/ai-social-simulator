import numpy as np

# -----------------------------------
# SIMPLE LOCAL EMBEDDING (NO INTERNET)
# -----------------------------------

def get_embedding(text: str):
    text = text.lower()

    keywords = [
        "ai", "technology", "future", "jobs",
        "money", "finance", "market",
        "risk", "danger", "inequality"
    ]

    vector = []

    for word in keywords:
        vector.append(text.count(word))

    return np.array(vector, dtype=float)