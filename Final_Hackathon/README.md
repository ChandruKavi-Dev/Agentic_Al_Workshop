🧠 Clinical Fit Evaluator

Agentic AI System for Culture-Aligned Hiring in Healthcare

---

## 🎯 Objective

To build an **Agentic AI-powered Clinical Fit Evaluator** that assesses a candidate’s alignment with a hospital’s clinical philosophy, patient interaction style, and values by:

- Parsing candidate profiles from MedMatch, LinkedIn, bios, and publications.
- Extracting hospital culture from SOPs, websites, and charters using RAG.
- Matching behavioral traits and detecting conflict risks.
- Generating a comprehensive, explainable fit score.

---

## 👤 Participant Details

- **Name**: Chandru Kavi  
- **Project Title**: Clinical Fit Evaluator  
- **Hackathon**: Final Hackathon – Agentic AI Training  
- **Submission Deadline**: ✅ Submitted before June 20, 2025, 5:30 PM IST

---

## 🧱 Project Structure

```bash
clinical-fit-evaluator/
├── backend/
│   ├── agents/               # Multi-agent modules
│   ├── api/                  # FastAPI endpoints
│   └── app/                  # Entry point (main.py)
├── frontend/
│   ├── app/                  # Next.js pages & components
│   └── public/               # Assets
├── data/                     # Sample inputs
├── diagrams/
│   └── agentic_workflow.png  # Visual workflow
├── README.md
└── requirements.txt
````

---

## 🧠 Agentic AI Workflow

A[Upload Candidate Data] --> B[🧑‍⚕️ Candidate Profile Analyzer]

A2[Upload Hospital Documents or URL] --> C[🏥 Hospital Culture Extractor (RAG)]

B --> D[🤝 Trait Matching Agent]
C --> D

D --> E[⚠️ Conflict Risk Detector Agent]

E --> F[📊 Fit Index Generator Agent]

F --> G[🖥️ Display on Dashboard]

<img width="1012" alt="Untitled" src="https://github.com/user-attachments/assets/16328b97-9801-4cad-8fd6-a17660440722" />


## 🚀 Tech Stack

| Layer          | Tech Used                                          |
| -------------- | -------------------------------------------------- |
| **Frontend**   | Next.js, TailwindCSS (w/ ShadCN UI), Framer Motion |
| **Backend**    | Python, FastAPI, LangChain                         |
| **Agents**     | LangChain + Gemini (via langchain-google-genai)    |
| **RAG Stack**  | ChromaDB + GoogleEmbeddings                        |
| **UI Helpers** | Sonner (toasts), Lucide Icons                      |
| **Database**   | MongoDB (or PostgreSQL fallback)                   |


## ⚙️ How to Run the Project

### 🔧 Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 💻 Frontend Setup (Next.js + Tailwind + Shadcn UI)

```bash
cd frontend
npm install
```

#### 📦 Install Additional UI Packages Locally (not globally)

```bash
npm install lucide-react framer-motion
npx shadcn-ui@latest add card button input label textarea progress sonner tabs
```

#### ▶️ Start the Frontend

```bash
npm run dev
```

Once both backend and frontend are running, visit:

```
🔗 Frontend UI: http://localhost:3000  
🧠 Backend API: http://localhost:8000/docs
```

---

## 📊 Frontend Features

* 🗂️ Candidate & Hospital document uploader
* 📊 Real-time trait match visualizer
* 🚦 Risk indicators (Red / Yellow / Green)
* 📄 Downloadable fit reports
* ⚙️ Configurable evaluation preferences

---

## 🔧 Agents & Responsibilities

| Agent                      | Role                                                     |
| -------------------------- | -------------------------------------------------------- |
| 🧑‍⚕️ Profile Analyzer     | Extracts behavioral traits from bio, LinkedIn, MedMatch  |
| 🏥 Culture Extractor (RAG) | Extracts values from SOPs, websites                      |
| 🤝 Trait Matcher           | Compares candidate traits with hospital culture          |
| ⚠️ Conflict Detector       | Flags misalignments in work style or values              |
| 📊 Fit Score Generator     | Produces final score with summary and colored risk zones |

---

## ✅ Sample Output (JSON)

```json
{
  "fit_score": 89,
  "zone": "Green",
  "alignment": {
    "empathy": "High - matched with patient-first culture"
  },
  "conflicts": [
    {
      "trait": "leadership",
      "risk_level": "yellow",
      "reason": "Independent style in hierarchical system"
    }
  ]
}
```

---

## 🧪 Performance Metrics

| Agent                   | Max Time | Target Accuracy |
| ----------------------- | -------- | --------------- |
| Profile Analyzer        | < 2 min  | ≥ 80% traits    |
| Culture Extractor (RAG) | < 1 min  | ≥ 80% values    |
| Trait Matcher           | < 20 sec | ≥ 90% match     |
| Conflict Detector       | < 15 sec | ≥ 85% clashes   |
| Fit Generator           | < 10 sec | 100% coverage   |

---

## 🔒 Ethics & Explainability

* 🧽 Sanitized PII (no race/gender/age bias)
* 💬 Transparent reasoning with LLM-generated justifications
* ✅ Output designed to support—not replace—HR decision-making

---

## 📽️ Demo Video

Watch a complete walkthrough of the **Clinical Fit Evaluator** project in action:

👉 [Click here to view the demo video](https://drive.google.com/file/d/11C_lmeo-6dOnUjVkkRVCNdp-6OFBWktY/view?usp=sharing)


---
## 🙌 Credits

* [LangChain](https://www.langchain.com/)
* [Gemini AI](https://ai.google/)
* [Shadcn UI](https://ui.shadcn.com/)
* [ChromaDB](https://www.trychroma.com/)

---

> *“Built with empathy, AI, and intention to empower smarter clinical hiring decisions.”*
> — **Chandru Kavi** 🚀
