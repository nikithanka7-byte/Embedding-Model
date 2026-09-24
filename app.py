from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "I love learning Python.",
    "Python programming is interesting to me.",
    "I enjoy studying machine learning.",
    "I want to build AI applications.",
    "Artificial intelligence is useful in many fields.",
    "Machine learning is an important part of AI.",
    "Data analysis helps us find useful information.",
    "The temperature is very high today."
]

embeddings = model.encode(sentences)


print("Total number of sentences:", len(sentences))
print("Embedding dimension:", len(embeddings[0]))

print("\n--- Embeddings ---")

for i, sentence in enumerate(sentences):
    print("\nSentence:", sentence)
    print("Embedding:", embeddings[i])

similarity = cosine_similarity(embeddings)

print("\n--- Semantic Similarity ---")

for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):

        if similarity[i][j] > 0.5:
            print(
                f"\nSentence 1: {sentences[i]}"
                f"\nSentence 2: {sentences[j]}"
                f"\nSimilarity: {similarity[i][j]:.4f}"
            )
