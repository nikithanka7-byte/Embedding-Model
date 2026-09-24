# Embedding Model: Semantic Sentence Similarity

A small Python project that converts sentences into vector embeddings using a pre-trained **Sentence-Transformers** model and uses **cosine similarity** to find sentences with similar meanings.

## Overview

Text embeddings represent the meaning of a sentence as a list of numbers called a **vector**. Sentences with similar meanings can have similar vector representations, even when they use different words.

This project demonstrates how an embedding model can be used for **semantic sentence similarity**.

### The project performs the following steps:

1. Loads the `all-MiniLM-L6-v2` model from Sentence-Transformers.
2. Converts sample sentences into **384-dimensional embeddings**.
3. Calculates pairwise cosine similarity between all sentences.
4. Displays sentence pairs whose similarity score is above `0.5`.

---

## Objectives

* To understand the concept of text embeddings.
* To convert sentences into numerical vector representations.
* To use a pre-trained Sentence-Transformers model.
* To calculate semantic similarity between sentences.
* To identify sentences with related meanings.

---

## Technologies Used

* **Python**
* **Sentence-Transformers**
* **Scikit-learn**
* **all-MiniLM-L6-v2**

---

## Repository Structure

```text
Embedding-Model/
│
├── app.py        # Main Python script
├── output.txt    # Sample output
└── README.md     # Project documentation
```

### `app.py`

Contains the main Python code for generating sentence embeddings and calculating cosine similarity.

### `output.txt`

Contains the output generated after running the Python program, including the embedding information and similarity results.

### `README.md`

Contains the documentation and instructions for the project.

---

## Requirements

* Python 
* sentence-transformers
* scikit-learn

Install the required libraries using:

```bash
pip install sentence-transformers scikit-learn
```

---

## How It Works

The basic implementation is:

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(sentences)

similarity = cosine_similarity(embeddings)
```

### Step 1: Load the Model

```python
model = SentenceTransformer("all-MiniLM-L6-v2")
```

The `all-MiniLM-L6-v2` model is a compact and efficient pre-trained model that converts sentences into **384-dimensional vectors**.

### Step 2: Generate Embeddings

```python
embeddings = model.encode(sentences)
```

The `encode()` function converts each input sentence into a numerical embedding.

For example:

```text
Sentence
    ↓
Embedding Model
    ↓
[0.12, -0.45, 0.78, ...]
```

Each sentence is represented by a 384-dimensional vector.

### Step 3: Calculate Similarity

```python
similarity = cosine_similarity(embeddings)
```

Cosine similarity compares the direction of two vectors and produces a similarity score.

In general:

* **1** → Very similar
* **0** → Little or no similarity
* **Negative values** → Opposite directions

In this project, sentence pairs with a similarity score **greater than 0.5** are displayed.

---

## Similarity Threshold

The project uses a threshold of:

```text
0.5
```

Only sentence pairs with a similarity score above `0.5` are printed.

Changing the threshold changes the number of matching sentence pairs.

For example:

```text
Higher threshold → Stricter matching → Fewer results

Lower threshold → Looser matching → More results
```

---

## Sample Input

The project uses the following sample sentences:

```text
1. I love learning Python.
2. Python programming is interesting to me.
3. I enjoy studying machine learning.
4. I want to build AI applications.
5. Artificial intelligence is useful in many fields.
6. Machine learning is an important part of AI.
7. Data analysis helps us find useful information.
8. The temperature is very high today.
```

---

## Sample Output

The program first displays:

```text
Total number of sentences: 8
Embedding dimension: 384
```

It then displays sentence pairs whose similarity score is above `0.5`.

| Sentence 1                                        | Sentence 2                                      | Similarity |
| ------------------------------------------------- | ----------------------------------------------- | ---------: |
| I love learning Python.                           | Python programming is interesting to me.        |     0.8205 |
| Artificial intelligence is useful in many fields. | Machine learning is an important part of AI.    |     0.7436 |
| I enjoy studying machine learning.                | Machine learning is an important part of AI.    |     0.6089 |
| I love learning Python.                           | I enjoy studying machine learning.              |     0.5760 |
| Python programming is interesting to me.          | I enjoy studying machine learning.              |     0.5187 |
| Artificial intelligence is useful in many fields. | Data analysis helps us find useful information. |     0.5132 |

The complete output, including the generated embedding information and similarity results, is available in [`output.txt`](output.txt).

---

## Project Workflow

```text
Input Sentences
       ↓
Sentence Transformer
       ↓
384-Dimensional Embeddings
       ↓
Cosine Similarity
       ↓
Similarity Score
       ↓
Filter Score > 0.5
       ↓
Similar Sentence Pairs
```

---


## Installation

Clone the repository:

```bash
git clone https://github.com/nikithanka7-byte/Embedding-Model.git
```

Move into the project directory:

```bash
cd Embedding-Model
```

Install the required packages:

```bash
pip install sentence-transformers scikit-learn
```

---

## How to Run

Run the Python program using:

```bash
python app.py
```

The program generates sentence embeddings, calculates cosine similarity, and displays the sentence pairs whose similarity score is above `0.5`.

---

## Conclusion

This project demonstrates the basic working of **text embeddings and semantic similarity** using Python.

The `all-MiniLM-L6-v2` model converts sentences into **384-dimensional numerical vectors**. Cosine similarity is then used to compare these vectors and identify sentences with related meanings.

This project provides a simple introduction to **Natural Language Processing (NLP), embeddings, vector representations, and semantic similarity**, which are important concepts in modern AI applications.
