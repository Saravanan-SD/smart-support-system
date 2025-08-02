# **Smart Support System**  
_AI-powered ticket triage with LLMs, background jobs, and a scalable backend._

---

## **🚀 What It Does**

- Accepts **support tickets** from users  
- **Classifies** them with an **LLM** (Category + Priority)  
- **Summarizes** the text for agents  
- **Detects PII** (emails & phone numbers)  
- **Stores lifecycle** in MongoDB  
- **Runs everything asynchronously** for speed & scalability  

---

## **🧩 How It Works**

1. **User submits a ticket** → `/api/classify`  
2. **FastAPI** puts the job in **Redis** (no waiting!)  
3. **Celery workers** process tasks in **two stages**:
   - **Classification Queue** → Quick AI triage  
   - **Enrichment Queue** → Summarization + PII detection  
4. **MongoDB** stores the ticket from **“received” → “completed”**  
5. **Flower Dashboard** shows live job progress and retries  

---

## **⚡ Why It’s Cool**

- **Instant API response** → Background jobs handle heavy LLM work  
- **Multi-queue Celery** → Scales like a real production system  
- **Retries + Monitoring** → No lost tasks, no silent failures  
- **Event-driven pipeline** → Perfect example of **eventual consistency** in system design  

---

## **🛠 Tech Stack**

- **FastAPI** – Async API server  
- **Groq LLM + LangChain** – Ticket classification brain  
- **Celery + Redis** – Background job engine  
- **MongoDB** – Persistent ticket storage  
- **Flower** – Real-time queue monitoring  

---

## **🎯 Quick Start**

```bash
# 1. Start dependencies
docker run -d -p 6379:6379 redis
docker run -d -p 27017:27017 mongo

# 2. Run FastAPI
uvicorn app.main:app --reload

# 3. Start workers
celery -A worker worker --loglevel=info --pool=solo -Q classification
celery -A worker worker --loglevel=info --pool=solo -Q enrichment

