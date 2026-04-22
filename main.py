from fastapi import FastAPI


app = FastAPI(title="Sofa`s eCommerce API")


@app.get("/")
async def read_root():
    return {"message": "hello Sofa!"}


@app.get("/items/{item_id}")
async  def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
