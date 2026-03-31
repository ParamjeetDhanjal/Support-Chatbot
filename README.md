# Support Chatbot — AI Customer Support System

A structured AI customer support chatbot built with **FastAPI** and **Groq (Llama models)**.  
It combines **pre-written FAQ responses**, **AI-generated answers**, and a **callback system** for unresolved issues.

---

## Features

- **Menu-based guided support** using CSV data  
- **AI-powered responses** for free-text queries  
- **Callback request system** for human follow-up  
- **Easy content updates** — no code changes required  

---

## How It Works

1. **User opens chat**  
2. Bot displays **main topic buttons** (from CSV)  
3. User selects a topic → **sub-questions appear**  
4. User selects a question → **pre-written answer is shown**  
5. If unresolved → **free-text box appears** for AI response  
6. If still unresolved → **callback form appears** to log a request  

---

## Setup & Run Locally

1. **Make environment file**

```

2. **Add your Groq API key** in `.env`:

```env
GROQ_API_KEY=your_api_key_here
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Start the server**

```bash
uvicorn main:app --reload
```

5. **Open in browser**

```text
http://localhost:8000
```

---

## Updating Chatbot Content

* All chatbot content is in **`data.csv`**:

| topic  | question                     | answer            |
| ------ | ---------------------------- | ----------------- |
| Refund | How long does a refund take? | 5–7 business days |

* Add or edit rows  
* Restart the server  
* Changes appear immediately, no code changes required  

---

## Deployment on Render

1. Push the project to **GitHub**  
2. Go to **[Render.com](https://render.com)** → New Web Service → Connect repo  
3. Add **environment variable**:

```env
GROQ_API_KEY=your_api_key_here
```

4. Deploy  

Your chatbot is live on the internet.

---

## Project Structure

```
supportbot/
├── main.py         # Backend API routes
├── data.csv        # Chatbot content
├── static/
│   └── index.html  # Chat UI
├── requirements.txt
├── agent_requests.txt
└── .env
```
