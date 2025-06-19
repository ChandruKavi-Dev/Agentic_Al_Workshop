## 🩺 Medical Career Path Mentor – Overview

An AI-powered tool to guide **junior healthcare professionals** in choosing the right career paths using:

* ✅ **Career History Parsing**
* 📚 **Career Path Recommendation (RAG + Gemini 1.5/Flash)**
* 👥 **Mentor & Resource Matching**
* 🌳 **Career Path Visualization**

Built with **LangChain**, **Gemini API**, **Streamlit**, and **Vector DB**.

---

## 🔧 Tech Stack

* **LangChain** (Agents + RAG)
* **Gemini 1.5/Flash**
* **Streamlit UI**
* **FAISS Vector Store**
* **Python**

---

Medical-Career-Mentor/
│
├── 📂 data/
│   ├── 01_fellowships.md
│   ├── 02_mba_in_healthcare.md
│   ├── 03_public_health_policies.md
│   └── 04_career_case_studies.md
│
├── 📂 vector_db/
│   └── faiss_index/
│
├── app.py                
├── agents.py              
├── rag_pipeline.py        
├── visualizer.py        
├── requirements.txt     
└── .env                

## 🚀 Quick Setup

```bash
# 1. Install requirements
pip install -r requirements.txt

# 2. Create .env file
GEMINI_API_KEY=your_key
VECTOR_DB_PATH=./db/

# 3. Load documents and embed
python rag_pipeline/loader.py

# 4. Launch Streamlit app
streamlit run ui/streamlit_app.py
```

---

## 🧠 Agents Overview

1. **Career History Parser** – Extracts education, role, interest
2. **Path Recommender (RAG)** – Suggests paths using documents
3. **Mentor Matcher** – Finds mentors/resources based on path
4. **Path Visualizer** – Shows career evolution tree

---

## ✅ Example

**Input**: MBBS | Junior Doctor | Ophthalmology
**Output**:

* 🎯 Suggest: MS Ophthalmology, ICO Fellowships
* 👤 Mentor: AIIMS-trained doctors
* 🌳 Tree: General → Specialist → Surgeon → Fellowship


