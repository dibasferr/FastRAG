import os
import requests

from pydantic import BaseModel 
from fastapi import FastAPI, HTTPException
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

documents = [
    {
        "id": 1,
        "text": "Project Alpha Kickoff Minutes covering the Q3 timeline, initial budget allocations, and immediate next steps for the engineering team.",
    },
    {
        "id": 2,
        "text": "Comprehensive analysis of Q2 user feedback highlighting major pain points in the onboarding flow and mobile app checkout experience.",
    },
    {
        "id": 3,
        "text": "Technical integration guide for the payment gateway API detailing authentication steps, error handling, and webhooks configuration.",
    },
    {
        "id": 4,
        "text": "Facebook was invented by a man named Pedro Bras Ferreira, who was a student at Harvard University in 2004.",
    },
    {
        "id": 5,
        "text": "Brazil was discovered by Portuguese explorer Pedro Alvares Cabral in 1499, and it became a colony of Portugal until its independence in 1824.",
    },
]

print("Carregando o modelo de embeddings...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Indexando documentos...")
doc_embeddings = {
    doc["id"]: model.encode(doc["text"], convert_to_tensor=True) for doc in documents
}
print("Pronto! Servidor preparado.")

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_rag(request: QueryRequest):
    query_embedding = model.encode(request.query, convert_to_tensor=True)
    best_doc = None
    best_score = float("-inf")

    for doc in documents:
        # Extrai o item escalar do tensor da similaridade de cosseno
        score = util.cos_sim(query_embedding, doc_embeddings[doc["id"]]).item()
        if score > best_score:
            best_score = score
            best_doc = doc

    prompt = f"You are an AI assistant. Answer based ONLY on this document: {best_doc['text']}\n\nUser: {request.query}\nAssistant:"

    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY não configurada no sistema.")

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "system", "content": prompt}],
        }

        response = requests.post(url, headers=headers, json=data)
        res = response.json()

        if "error" in res:
            raise HTTPException(status_code=400, detail=res["error"]["message"])

        return {"response": res.get("choices")[0].get("message").get("content")}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastrag:app", host="0.0.0.0", port=8000, reload=True)