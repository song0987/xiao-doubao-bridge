from fastapi import FastAPI, Request
import requests
import json
import os

app = FastAPI()

DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY")
DOUBAO_ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
DOUBAO_MODEL = os.getenv("DOUBAO_MODEL", "doubao-pro")

@app.post("/xiaoi")
async def xiaoi_webhook(req: Request):
    data = await req.json()
    user_text = data.get("query", "")
    if not user_text:
        return {"reply": "我没有收到你的问题"}

    payload = {
        "model": DOUBAO_MODEL,
        "messages": [
            {"role": "system", "content": "你是豆包，回答简短，控制在80字以内，口语化，不要markdown。"},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.7
    }
    headers = {
        "Authorization": f"Bearer {DOUBAO_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        resp = requests.post(DOUBAO_ENDPOINT, headers=headers, json=payload, timeout=15)
        res_json = resp.json()
        answer = res_json["choices"][0]["message"]["content"].strip()
    except Exception as e:
        answer = "抱歉，豆包服务暂时出错了。"

    return {"reply": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
