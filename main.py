from fastapi import FastAPI, status, HTTPException
import schemas
from dbaccessor import DBAccessor
from encoding import Encoder
import config
import logging

app = FastAPI()

url_settings = config.Settings()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

"""
The main website
"""


@app.get("/")
def root():
    return {"message": "this is short url website."}


"""
The website to realize shortening method
"""


@app.post(
    "/api/v1/shorturl",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShortUrl,
)
def shorten_url(input: schemas.LongUrl):
    longurl = input.long_url
    url_encoder = Encoder(url_settings)
    shorturl = url_encoder.get_encoding(longurl)
    url_accessor = DBAccessor(url_settings)
    url_accessor.insert_url_data(longurl, shorturl)
    logger.info("longurl: %s", longurl)
    logger.info("shorturl: %s", shorturl)
    result = schemas.ShortUrl(short_url=shorturl)
    return result


"""
The website to realize redirecting method
"""


@app.get(
    "/api/v1/longurl",
    status_code=status.HTTP_200_OK,
    response_model=schemas.LongUrl,
)
def redirect_url(input: schemas.ShortUrl):
    shorturl = input.short_url
    url_accessor = DBAccessor(url_settings)
    res = url_accessor.get_longurl(shorturl)

    if res:
        return schemas.LongUrl(long_url=res)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"cannot find this short url: {shorturl}",
        )
