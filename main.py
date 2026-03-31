import os
import csv
import logging
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq

load_dotenv()

app    = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
AGENT_PHONE = os.getenv("AGENT_PHONE", "8010327720")



FAQ: list[dict] = []

def load_faq():
    global FAQ
    with open("data.csv", newline="", encoding="utf-8") as f:
        FAQ = list(csv.DictReader(f))
    print(f"✅ Loaded {len(FAQ)} FAQ entries")

load_faq()


def get_topics() -> list[str]:
    seen = []
    for row in FAQ:
        t = row["topic"].strip()
        if t not in seen:
            seen.append(t)
    return seen


def get_questions_for_topic(topic: str) -> list[str]:
    return [
        row["question"].strip()
        for row in FAQ
        if row["topic"].strip().lower() == topic.strip().lower()
    ]


def get_answer_for_question(question: str) -> str | None:
    for row in FAQ:
        if row["question"].strip().lower() == question.strip().lower():
            return row["answer"].strip()
    return None


def build_context() -> str:
    lines = []
    for row in FAQ:
        lines.append(f"Q: {row['question'].strip()}\nA: {row['answer'].strip()}")
    return "\n\n".join(lines)



class AskRequest(BaseModel):
    message: str


class CallbackRequest(BaseModel):
    name:    str
    phone:   str
    issue:   str


@app.get("/topics")
def topics():
    return {"topics": get_topics()}


@app.get("/questions/{topic}")
def questions(topic: str):
    qs = get_questions_for_topic(topic)
    if not qs:
        return {"questions": [], "error": "Topic not found"}
    return {"questions": qs}


@app.get("/answer")
def answer(question: str):
    ans = get_answer_for_question(question)
    if not ans:
        return {"found": False, "answer": ""}
    return {"found": True, "answer": ans}


@app.post("/ask")
def ask(req: AskRequest):
    context = build_context()

    system = f"""You are a helpful e-commerce customer support assistant.
Answer ONLY using the FAQ knowledge below.
If the answer is not in the FAQ, say: "I'm not sure about that. Please request a callback and our agent will help you."
Keep answers short, friendly, and clear.

FAQ KNOWLEDGE:
{context}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system",  "content": system},
            {"role": "user",    "content": req.message},
        ],
        temperature=0.2,
        max_tokens=300,
    )

    return {"reply": response.choices[0].message.content.strip()}


@app.post("/callback")
def request_callback(req: CallbackRequest):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line  = (
        f"[{timestamp}] "
        f"Name: {req.name} | "
        f"Phone: {req.phone} | "
        f"Issue: {req.issue}"
    )

    with open("agent_requests.txt", "a", encoding="utf-8") as f:
        f.write(log_line + "\n")

    print(f"📞 Callback requested → {log_line}")

    return {
        "success": True,
        "message": f"Your callback request has been sent. Our agent at {AGENT_PHONE} will call you shortly.",
        "agent_phone": AGENT_PHONE,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")