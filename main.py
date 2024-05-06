from fastapi import FastAPI, status, HTTPException
import schemas
from dbaccessor import DBAccessor
from encoding import encoding
from sqlalchemy.orm import Session

app = FastAPI()


@app.get("/")
def root():
    return {"message": "this is short url website."}


@app.post(
    "/api/v1/shorturl",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShortUrl,
)
def shorten_request(input: schemas.LongUrl):
    longurl = input.long_url
    shorturl = encoding.hashing(longurl)
    get_db = DBAccessor()
    get_db.insert_url_data(longurl, shorturl)
    result = schemas.ShortUrl(short_url=shorturl)
    return result


@app.get(
    "/api/v1/longurl",
    status_code=status.HTTP_200_OK,
    response_model=schemas.LongUrl,
)
def redirect_request(input: schemas.ShortUrl):
    shorturl = input.short_url
    get_db = DBAccessor()
    res = get_db.get_longurl(shorturl)
    if res:
        return schemas.LongUrl(long_url=res)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"cannot find this short url: {shorturl}",
        )
