# Hybrid_Log_Classification
 
A lightweight Splunk-like tool built with **FastAPI** and **Streamlit** to classify log messages using a hybrid AI model — combining regex, ML, and LLM-based classifiers — and visualize log analytics.

---

## 🚀 Features

- 📂 Upload log files (`.csv`)
- 🧠 Automatically classify logs into categories like `Security Alert`, `Workflow Error`, etc.
- 📊 View interactive analytics and dashboards (via Streamlit)
- ⚡ FastAPI backend handles preprocessing and classification
- 🔐 Supports LLM classification via GROQ API

---

## 🗂️ Project Structure

```
.
├── classify.py              # Hybrid classification logic
├── processor_regex.py       # Regex-based classifier
├── processor_lr.py          # ML-based classifier (Logistic Regression)
├── processor_llm.py         # LLM (Groq) based fallback classifier
├── server.py                # FastAPI backend
├── streamlit_app.py         # Streamlit analytics dashboard
├── requirements.txt         # Dependencies
├── resources/
│   └── output.csv           # Classified log output
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/log-analytics-app.git
cd log-analytics-app
```

### 2. Create Conda Env

```bash
conda create -n gm python=3.10
conda activate gm
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you're using LLMs via Groq, set your API key:

```bash
export GROQ_API_KEY=your_api_key_here      # For Linux/macOS
set GROQ_API_KEY=your_api_key_here         # For Windows CMD
$env:GROQ_API_KEY="your_api_key_here"      # For PowerShell
```

Alternatively, you can hardcode it in `processor_llm.py`:

```python
groq = Groq(api_key="your_api_key_here")
```

---

## 🖥️ Running the Project

### 1. Start FastAPI Backend

```bash
uvicorn server:app --reload
```

It will run at: `http://127.0.0.1:8000`

Test the upload via `/docs`.

---

### 2. Start Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

Go to: `http://localhost:8501`

You'll be able to upload a classified `output.csv` and visualize analytics!

---

## 📝 Expected CSV Format

The uploaded CSV file should have the following columns:

```csv
source,log_message
WorkflowManager,Task failed due to timeout...
Security,Unauthorized access attempt detected...
```

---

## 📈 Dashboard Capabilities

- Log category distribution
- Keyword-based filtering
- Source-wise log breakdown
- Temporal analysis (if timestamps available)

---

## 🔒 API Endpoint

### `/classify/` (POST)

Upload CSV file → returns classified file.

**Request**:
- Content-Type: `multipart/form-data`
- File: `.csv` with `source`, `log_message`

**Response**:
- Returns `output.csv` with a new column `target_label`.

---

## 📦 Dependencies

- `fastapi`
- `uvicorn`
- `pandas`
- `sentence-transformers`
- `scikit-learn`
- `streamlit`
- `groq`

---

## 🙌 Credits

Built by Aryan Mengawade, Atharva Deshmukh — inspired by Splunk, powered by hybrid AI models 💡

---

```

Let me know if you want it customized for deployment on Hugging Face, Docker, or to include example logs!