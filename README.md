# CENG442 Assignment 1: Azerbaijani Text Processing & Word Embeddings

This project is a pipeline for preprocessing Azerbaijani text data and training Word2Vec and FastText models for sentiment analysis.

**Group Members:**
* Talha Ubeydullah Gamga | 20050111078
* Aziz Önder | 22050141021
* Muhammed Fatih Asan | 23050151026
* Buğra Bildiren | 20050111022

**Trained Models:**
* https://drive.google.com/drive/folders/1JDyQ9jVjnsINwnwt0GCWzyrAAb633duM?usp=sharing 
---

## Project Overview

The main script (`Notebook_ceng442_assignment1_GroupTAFB.ipynb`) performs a complete NLP pipeline:

1.  **Data Loading:** Reads raw Excel files from the `data/` directory.
2.  **Preprocessing:** Applies a series of advanced cleaning and normalization steps.
3.  **File Output:** Saves the cleaned, standardized data (as `cleaned_text`, `sentiment_value`) into the `clean_data/` folder.
4.  **Corpus Building:** Combines all cleaned text into a single `corpus_all.txt` file for training.
5.  **Model Training:** Trains Word2Vec and FastText models (vector size 300, window 5, skip-gram) on the corpus.
6.  **Model Saving:** Saves the trained models to the `embeddings/` folder.
7.  **Evaluation:** Compares the Word2Vec and FastText models on quantitative and qualitative metrics.

## Key Features

* **Azerbaijani-Specific Normalization:** Correctly handles language-specific characters (e.g., `I` → `ı`, `İ` → `i`).
* **Text Cleaning:** Removes HTML tags, URLs, emails, phone numbers, and user mentions.
* **Domain Detection:** Identifies text domain (e.g., "reviews", "news", "social") and applies domain-specific rules.
* **Special Tokenization:** Replaces numbers with `<NUM>`, emojis with `EMO_POS`/`EMO_NEG`, and review-specific terms with `<PRICE>` or `<RATING_POS>`.
* **Sentiment/Negation Handling:** Appends a `_NEG` suffix to words following a negation term (e.g., `yox`, `deyil`).
* **Slang Correction:** Normalizes common slangs (e.g., `slm` → `salam`).

---

## Project Report & Model Evaluation

After training, the Word2Vec and FastText models were evaluated on several metrics.

### 1. Lexical Coverage (Quantitative)

This measures the percentage of unique words from our datasets found in the model's vocabulary. FastText's ability to use subwords means it can generate vectors for any word, but this metric checks for words present in the main trained vocabulary.

* `labeled-sentiment_2col.xlsx`: W2V=0.930, FT(vocab)=0.930
* `test_1_2col.xlsx`: W2V=0.915, FT(vocab)=0.915
* `train_3_2col.xlsx`: W2V=0.919, FT(vocab)=0.919
* `train-00000-of-00001_2col.xlsx`: W2V=0.923, FT(vocab)=0.923
* `merged_dataset_CSV_1_2col.xlsx`: W2V=0.899, FT(vocab)=0.899

### 2. Semantic Similarity (Quantitative)

We measured the cosine similarity for synonym (expected high score) and antonym (expected low score) pairs. The "Separation Score" (Synonym Sim - Antonym Sim) shows how well a model separates opposite meanings. A higher separation is better.

| Metric | Word2Vec | FastText |
| :--- | :--- | :--- |
| **Synonym Similarity** | 0.361 | **0.465** |
| **Antonym Similarity** | 0.335 | 0.424 |
| **Separation Score** | 0.027 | **0.040** |

**Conclusion:** FastText showed a slightly better ability to group synonyms and separate antonyms.

### 3. Nearest Neighbors (Qualitative)

A qualitative check shows the models' learned associations. FastText often captures morphological variations (e.g., `pis`, `pis!`, `pis.`), while Word2Vec sometimes captures related special tokens (e.g., `pis`, `<RATING_NEG>`).

**Seed Word: 'yaxşı' (good)**
* **W2V:** `['<RATING_POS>', 'yaxshi', 'iyi', 'yaxşı.', 'olar.']`
* **FT:** `['yaxşı!', 'yaxşıı', 'yaxşı.', 'yaxşıkı', ',yaxşı']`

**Seed Word: 'pis' (bad)**
* **W2V:** `['<RATING_NEG>', '<STARS_LOW>', 'pis.', 'pisdir', 'pisdi']`
* **FT:** `['pis!', 'pis,', 'pis.', 'pis.pul', 'piis']`

**Seed Word: 'bahalı' (expensive)**
* **W2V:** `['portretlerinə', 'villaları', 'yaxtaları', 'şəbəkədi', 'metallarla']`
* **FT:** `['bahalıı', 'bahalısı', 'bahalıq', 'baharlı', 'baha,']`

---

## How to Run

There are two options to run the full pipeline.

### Option 1: Google Colab (Recommended)

This is the simplest way to run the project without any local setup.

1.  Open the notebook in Google Colab.
2.  Run the **first code cell** in the notebook. This cell will clone the repository, change the directory, and install the necessary Python packages (`pandas`, `gensim`, etc.).

    ```python
    !git clone [https://github.com/eiziiaizii1/ceng442-assignment1-GroupTAFB.git](https://github.com/eiziiaizii1/ceng442-assignment1-GroupTAFB.git)
    %cd ceng442-assignment1-GroupTAFB
    !pip install pandas gensim openpyxl regex ftfy scikit-learn
    ```
3.  Run all subsequent cells in the notebook to perform data processing, model training, and evaluation.

### Option 2: Running Locally

This option requires you to set up a local Python environment.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/eiziiaizii1/ceng442-assignment1-GroupTAFB.git](https://github.com/eiziiaizii1/ceng442-assignment1-GroupTAFB.git)
    cd ceng442-assignment1-GroupTAFB
    ```

2.  **Create and activate a virtual environment:**

    * On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the notebook:**
    Start Jupyter Notebook and open `Notebook_ceng442_assignment1_GroupTAFB.ipynb`.
    ```bash
    jupyter notebook
    ```
    Then, run all cells in the notebook.
