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

## 1. Data & Goal

**Datasets:**
This project uses five different Azerbaijani text datasets provided for the assignment:
1.  `labeled-sentiment.xlsx`
2.  `merged_dataset_CSV__1_.xlsx`
3.  `test__1_.xlsx`
4.  `train__3_.xlsx`
5.  `train-00000-of-0001.xlsx`

**Goal:**
The main goal was to clean and preprocess these five datasets to create a unified corpus for sentiment analysis. As required by the assignment, we mapped all sentiment labels to a standard numeric format: **Negative (0.0)**, **Neutral (0.5)**, and **Positive (1.0)**. We kept the neutral $0.5$ value to preserve the three-class polarity, allowing models to learn the distinction between negative, positive, and explicitly neutral sentiments.

## 2. Preprocessing

We developed a comprehensive preprocessing pipeline in the `normalize_text_az` function. This pipeline applies the following rules in order:

* **Emoji Mapping:** Converted a predefined list of positive/negative emojis to special tokens (e.g., `EMO_POS`, `EMO_NEG`).
* **Text Cleaning:** Fixed text encoding (`ftfy`), unescaped HTML entities (`html.unescape`), and removed all HTML tags.
* **Tokenization of Special Entities:** Replaced URLs, emails, phone numbers, and user mentions (e.g., `@username`) with special tokens (`URL`, `EMAIL`, `PHONE`, `USER`).
* **Hashtag Splitting:** Removed the `#` symbol and split camelCase hashtags (e.g., `#QarabagIsBack` -> `qarabag is back`).
* **Language-Specific Lowercasing:** Applied Azerbaijani-aware lowercasing, correctly handling `İ` -> `i` and `I` -> `ı`.
* **Number & Punctuation Handling:** Replaced all digits with a `<NUM>` token and removed all punctuation (except for `.` `!` `?` when splitting sentences for the corpus).
* **Slang/De-asciify:** Corrected common slang and "asciified" words using a map (e.g., `cox` -> `çox`, `yaxsi` -> `yaxşı`).
* **Negation Handling:** When a negator word (like `yox`, `deyil`) was found, the next three tokens were tagged with a `_NEG` suffix (e.g., `yox yaxşı film` -> `yox yaxşı_NEG film_NEG`).
* **Token Filtering:** Removed repeated characters (e.g., `cooool` -> `cool`) and single-letter tokens (except 'o', 'e', 'ə').

**Data Removal:**
Before processing, we cleaned the datasets by:
1.  Dropping rows with missing text.
2.  Dropping rows with empty (whitespace-only) text.
3.  Dropping exact duplicates based on the text column.

**Before/After Examples:**

--- Example 1 ---
Before: @user <p>Men bu filme #BaxmagaDeyer 10 AZN verdim cox gozel idi!!! 🙂
After: user men bu filme baxmaga deyer <NUM> azn verdim çox gozel idi emo pos

--- Example 2 ---
Before: Bu telefon heç yaxsi deyil, batareyasi çabuk bitiyor.😡
After: bu telefon heç yaxşı_NEG deyil batareyasi_NEG çabuk_NEG bitiyor_NEG emo neg

## 3. Mini Challenges

We implemented several of the mini-challenges from the assignment description:

* **Hashtag Split:** Implemented as part of the main preprocessing pipeline.
* **Emoji Mapping:** Implemented with a small dictionary for common positive and negative emojis.
* **Negation Scope (Toggle):** Implemented in our main pipeline. We marked the 3 tokens following a negator with a `_NEG` suffix.
* **Simple Deasciify:** Implemented as part of our `SLANG_MAP`, which corrects `cox` -> `çox` and `yaxsi` -> `yaxşı`.
* **Stopword Research:**  
    We compared Azerbaijani (AZ) stopwords with English (EN) stopwords, as they are related languages. We noticed that many common function words, like conjunctions and pronouns, are very similar.  

    Based on our analysis, we proposed 10 candidate stopwords for removal, which are common and do not carry strong sentiment:

    - və (and)  
    - ilə (with)  
    - amma (but)  
    - ancaq (but/only)  
    - lakin (but)  
    - ya (or)  
    - həm (also)  
    - ki (that)  
    - bu (this)  
    - bir (a/an/one)

    **Why we did not remove negations:**  
    We did not remove negation words like *yox* (no/not), *deyil* (is not), or *heç* (not at all). This is because these words are critical for sentiment analysis.

## 4. Domain-Aware Processing

We implemented a simple domain-aware system as required.

**1. Detection Rules:**
We used regex to detect domains based on keywords:
* `news`: `apa`, `trend`, `azertac`, `reuters`, `bloomberg`, etc.
* `social`: `rt`, `@`, `#`, or common emojis.
* `reviews`: `azn`, `manat`, `qiymət`, `aldım`, `ulduz`, `çox yaxşı`, `çox pis`.
* `general`: Any text not matching the above.

**2. Domain-Specific Normalization:**
After the main cleaning, we applied a special function (`domain_specific_normalize`) *only* for texts detected as "reviews". This function replaced:
* Prices (e.g., `10 azn`) with a `<PRICE>` token.
* Star ratings (e.g., `5 ulduz`) with `<STARS_5>` token.
* Specific phrases (e.g., `çox yaxşı`) with `<RATING_POS>` or `<RATING_NEG>` tokens.

**3. Domain Tagging:**
For the final `corpus_all.txt`, we added a domain tag (e.g., `domnews`, `domreviews`) to the beginning of every line, as generated by the `detect_domain` function.

## 5. Embeddings

We trained Word2Vec (W2V) and FastText (FT) models on the combined `corpus_all.txt`.

**Training Settings:**

| Parameter | Word2Vec (gensim) | FastText (gensim) |
| :--- | :--- | :--- |
| `vector_size` | 300 | 300 |
| `window` | 5 | 5 |
| `min_count` | 3 | 3 |
| `sg` (model) | 1 (Skip-gram) | 1 (Skip-gram) |
| `epochs` | 10 | 10 |
| `negative` | 10 | (N/A) |
| `min_n` (char n-gram) | (N/A) | 3 |
| `max_n` (char n-gram) | (N/A) | 6 |

**Results: Lexical Coverage (In-Vocabulary)**
This measures how many tokens from each dataset were found in the model's vocabulary.

| Dataset | W2V Coverage | FT Coverage |
| :--- | :--- | :--- |
| labeled-sentiment | 0.932 | 0.932 |
| test__1_ | 0.987 | 0.987 |
| train__3_ | 0.990 | 0.990 |
| train-00000-of-00001 | 0.943 | 0.943 |
| merged_dataset_CSV__1_ | 0.949 | 0.949 |

**Results: Semantic Similarity**
We measured cosine similarity for synonym (higher is better) and antonym (lower is better) pairs.

| Metric | Word2Vex (W2V) | FastText (FT) |
| :--- | :--- | :--- |
| Synonyms (avg. similarity) | 0.365 | 0.439 |
| Antonyms (avg. similarity) | 0.336 | 0.424 |
| **Separation (Syn - Ant)** | **0.029** | **0.015** |

**Results: Nearest Neighbors (Qualitative)**

| Seed Word | W2V Neighbors | FT Neighbors |
| :--- | :--- | :--- |
| `yaxşı` | ['iyi', 'yaxshi', '<RATING_POS>', 'yaxwi', 'deməy'] | ['yaxşıı', 'yaxşıkı', 'yaxşıca', 'yaxş', 'yaxşıya'] |
| `pis` | ['günd', 'vərdişlərə', '<RATING_NEG>', 'xalçalardan', 'kardeşi'] | ['piis', 'pisdii', 'pisə', 'pi', 'pixlr'] |
| `çox` | ['gözəldir', 'bəyənilsin', 'çöx', 'çoox', 'çoxx'] | ['çoxçox', 'çoxx', 'çoxh', 'ço', 'çoh'] |
| `bahalı` | ['yaxtaları', 'portretlerinə', 'villaları', 'metallarla', 'kantakt'] | ['bahalıı', 'bahalısı', 'bahalıq', 'baharlı', 'pahalı'] |
| `ucuz` | ['düzəltdirilib', 'sorbasi', 'şeytanbazardan', 'alinmis', 'keyfiyetli'] | ['ucuzu', 'ucuza', 'ucuzdu', 'ucuzluğa', 'ucuzdur'] |
| `<RATING_POS>` | ['süper', 'deneyin', 'internetli', 'öyrədici', 'uygulama'] | ['<RATING_NEG>', 'süperr', 'çookk', 'çokk', 'süper'] |

**Domain Drift Analysis:**
We also conducted a domain drift analysis (see Notebook Cell 27) to see if word meanings changed between the "reviews" and "general" domains. We trained separate models on *balanced* samples (5,145 sentences each) and found that words like `telefon` ($0.529$ drift) and `yaxşı` ($0.477$ drift) showed a noticeable change in context, while `film` ($0.264$ drift) remained stable.

## 6. Conclusions

### Model Comparison

Both Word2Vec and FastText achieved similar **lexical coverage** (93-99% across datasets), indicating that our preprocessing pipeline successfully standardized the vocabulary. However, the models showed distinct characteristics:

**Word2Vec** demonstrated slightly better semantic discrimination with a separation score of **0.029** compared to FastText's **0.015**. This suggests Word2Vec better distinguishes between synonyms and antonyms in our Azerbaijani sentiment corpus. The nearest neighbor analysis revealed that Word2Vec captures more contextually meaningful relationships (e.g., `<RATING_POS>` neighbors include sentiment-related words like 'süper', 'öyrədici').

**FastText**, while showing lower separation scores, excelled at handling morphological variations - its neighbors for seed words often included inflected forms (e.g., `bahalı` → `bahalısı`, `bahalıq`). This is particularly valuable for Azerbaijani, an agglutinative language with rich morphology.

### Why Word2Vec Performed Better

For our specific **sentiment analysis** task, Word2Vec's stronger semantic separation makes it the preferred choice. The ability to clearly distinguish positive from negative sentiment is more critical than handling rare word forms, especially since our preprocessing (deasciification, slang correction) already normalized most common variations.

### Next Steps

1. **Expand domain coverage**: Our dataset was heavily skewed toward "general" (118,950 sentences) versus "reviews" (5,145 sentences). Collecting more balanced domain-specific data would improve domain-aware embeddings.

2. **Implement lemmatization**: Adding morphological analysis could reduce vocabulary size and improve generalization, particularly beneficial for FastText.

3. **Fine-tune for sentiment**: Train domain-specific models or use the embeddings as input to a downstream sentiment classifier (e.g., LSTM, BERT-style transformer) to evaluate their practical impact.

4. **Explore contextualized embeddings**: Modern approaches like multilingual BERT or language-specific transformers might capture sentiment nuances better than static embeddings.

## 7. Reproducibility

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
