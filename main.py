from fastapi import FastAPI, status
import schemas

app = FastAPI()


@app.get("/")
def root():
    return {"message": "this is short url website."}


@app.get(
    "/shortener", status_code=status.HTTP_201_CREATED, response_model=schemas.LongUrl
)
def shortener(input: schemas.LongUrl):
    print(input.long_url)
    result = schemas.ShortUrl(short_url=input.long_url)
    return result
