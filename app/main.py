from fastapi import FastAPI, Response


app = FastAPI(title="Sofa`s eCommerce API")


@app.get("/favicon.ico, include_in_schema=False")
async def favicon():
    return Response(content="", media_type="image/x-icon")


@app.get("/")
async def read_root():
    return {"message": "hello Sofa!"}


@app.get("/items/{item_id}")
async  def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
