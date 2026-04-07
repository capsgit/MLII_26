# 😐 Sentiment Analysis App

A simple yet structured **multi-language sentiment analysis tool** built with:

- Streamlit (UI)
- TextBlob (sentiment engine)
- Deep Translator (language support)

---

## 🚀 What this app does

👉 Input a text  
👉 Detect sentiment sentence-by-sentence  
👉 Aggregate overall sentiment  
👉 Show distribution + volatility  

---

## 🧠 Core features

### ✍️ Text analysis
- Sentence-level breakdown
- Polarity scoring
- Sentiment classification

### 🌍 Multi-language support
- EN → direct analysis  
- DE (and others) → translated → analyzed  

### 📊 Metrics dashboard
- Global polarity
- Sentiment distribution
- Volatility (tone variation)

### 🧾 Output
- Summary explanation
- Sentence table
- Visual dashboard

---

## 📊 Example output


        Overall sentiment: neutral
        Positive: 2
        Negative: 1
        Volatility: 0.67


---

## ⚙️ Tech stack

- Python
- Streamlit
- TextBlob
- deep-translator

---

## 📦 Installation

```bash
pip install -r requirements.txt
```
or manually:

```
pip install streamlit pandas textblob deep-translator
```

### ▶️ Run the app
```bash
streamlit run app.py
```

### 🧠 Design decisions

- Sentiment is always computed in English
- Non-English text is translated first
- Simple heuristics (TextBlob) instead of heavy ML models
- UI optimized for readability

### ⚠️ Limitations
- Translation may lose nuance
- TextBlob is rule-based (not deep learning)
- Not ideal for sarcasm or complex language

### 🧩 Future improvements
- Better NLP model (transformers)
- Language auto-detection
- Sentiment timeline visualization
- Export results (CSV / PDF)

## 📌 Status

    🟢 Functional
    🟡 Improving UI & metrics
    🔵 Ready for extension