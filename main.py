from fastapi import FastAPI, status, HTTPException
import schemas
from dbaccessor import DBAccessor
from encoding import Encoding
from sqlalchemy.orm import Session
import config
import logging

app = FastAPI()

my_settings = config.Settings()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('myapp.log')

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
    my_encoding = Encoding(my_settings)
    shorturl = my_encoding.get_encoding(longurl)
    get_db = DBAccessor(my_settings)
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
    my_settings = config.Settings()
    get_db = DBAccessor(my_settings)
    res = get_db.get_longurl(shorturl)
    if res:
        return schemas.LongUrl(long_url=res)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"cannot find this short url: {shorturl}"
        )