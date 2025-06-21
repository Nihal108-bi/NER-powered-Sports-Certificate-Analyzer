

```markdown
# 🏅 Named Entity Recognition for Sports Certificate Extraction

This project implements a **Named Entity Recognition (NER)** pipeline to extract structured information from unstructured sports certificates. Using a combination of **BERT** and **spaCy**, the system identifies key fields like **Participant Name, Winning Position, Sport Name**, and **Year of Organization**.

---

## 🚀 Overview

Many certificates are stored as unstructured text or scanned documents. This project addresses the challenge of extracting essential details using Natural Language Processing (NLP) models, particularly for the sports domain.

---

## 🧠 Models Used

- **BERT (Pretrained - `dslim/bert-base-NER`)**  
  Used for extracting `Participant Name` (PER entity).

- **spaCy**  
  Custom-trained to extract `Winning Position`, `Sport Name`, and `Organization Year`.

---

## 🗂️ Project Structure

```

NER\_SPORTS\_TASK/
│
├── config/
│   └── config.cfg
│
├── data/
│   ├── data.xlsx
│   ├── train\_annotations.json
│   └── test\_annotations.json
│
├── src/
│   ├── components/
│   │   ├── data\_transformation.py
│   │   └── model\_training.py
│   ├── constant/
│   ├── entity/
│   ├── exception/
│   ├── pipeline/
│   │   └── train\_pipeline.py
│   ├── utils/
│   │   └── main\_utils.py
│   ├── app.py
│   └── prediction.py
│
├── report/
│   └── Report.pdf
├── research/
│   ├── sports\_ner.ipynb
│   └── demo.ipynb
├── requirements.txt
└── setup.py

````

---

## ⚙️ Methodology

1. **Data Collection**  
   300 annotated certificate descriptions from Excel.

2. **Data Annotation**  
   Manual tagging using [ner-annotator](https://github.com/tecoholic/ner-annotator).

3. **Preprocessing**  
   - JSON → SpaCy `.spacy` format
   - Train/Test split (90:10)

4. **Modeling**  
   - BERT (Pretrained) for names  
   - spaCy (Custom training) for other fields

5. **Training**  
   - Config generated using `spacy init config`
   - Fine-tuned hyperparameters: batch size, epochs

6. **Serving**  
   - **FastAPI** endpoint for training and predictions

---

## 📊 Evaluation Metrics

| Metric     | Description                  |
|------------|------------------------------|
| `ENTS_F`   | F1 Score for entity spans     |
| `ENTS_P`   | Precision                     |
| `ENTS_R`   | Recall                        |
| `LOSS_NER` | Loss value for NER component  |

---

## 🔧 Tools & Libraries

- [spaCy](https://spacy.io/)
- [HuggingFace Transformers](https://huggingface.co/)
- [PyTorch](https://pytorch.org/)
- [Pandas](https://pandas.pydata.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [NER Annotator](https://github.com/tecoholic/ner-annotator)

---

## 🌐 FastAPI Endpoint

- `POST /train`: Trigger model training
- `POST /predict`: Predict entities from certificate text

---

## 📌 Challenges Faced

- Manual annotation of limited data
- Combining two different model outputs
- Ensuring consistent format for training spaCy

---

## 📥 Installation

```bash
git clone https://github.com/yourusername/ner-sports-certificate.git
cd ner-sports-certificate
pip install -r requirements.txt
````

---

## ▶️ Run the API

```bash
uvicorn src.app:app --reload
```

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgements

* [HuggingFace](https://huggingface.co/)
* [Explosion.ai (spaCy)](https://explosion.ai/)
* [Tecoholic’s NER Annotator](https://github.com/tecoholic/ner-annotator)

---

```

---

```
