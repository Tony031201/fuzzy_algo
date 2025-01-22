from fuzzywuzzy import process
import uvicorn
import json
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

class QuestionRequest(BaseModel):
    question: str

app = FastAPI()

# 加载问答库
with open("qa.json", "r") as f:
    qa_data = json.load(f)

@app.get('/')
def home():
    return "Hello from your Railway-deployed Python service!"

@app.post("/predict")
def get_answer_fuzzy(request: QuestionRequest):
    try:
        question = request.question
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 获取问题列表
    questions = [item["question"] for item in qa_data]
    # 计算相似度
    best_match, similarity = process.extractOne(question, questions)
    if similarity > 80:  # 设置相似度阈值
        # 返回匹配到的问题的答案
        for item in qa_data:
            if item["question"] == best_match:
                return {
                    "question": question,
                    "answer":item["answer"]
                }
    else:
        return {
            "question": question,
            "answer":"I'm sorry, I don't understand the question."
        }

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0', port=5000)

