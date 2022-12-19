from fastapi import FastAPI

app = FastAPI()

# 接続テスト
@app.get("/test/")
async def test():
    return 'テスト'
