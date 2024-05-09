from fastapi import FastAPI, status, HTTPException
from app import schemas
from app.dbaccessor import DBAccessor
from app.encoder import Encoder
from app import config
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
def shorten_url(data: schemas.LongUrl):
    db_accessor = DBAccessor(url_settings)
    url_encoder = Encoder(url_settings)
    result = shortern_url_processor(data, db_accessor, url_encoder)
    return result


def shortern_url_processor(
    data: schemas.LongUrl, db_accessor: DBAccessor, url_encoder: Encoder
):
    longurl = data.long_url

    if db_accessor.longurl_exists(longurl):
        shorturl = db_accessor.get_shorturl(longurl)
    else:
        shorturl = url_encoder.get_encoding(longurl)
        db_accessor.insert_url_data(longurl, shorturl)

    logger.info("longurl: %s, shorturl: %s", longurl, shorturl)

    result = schemas.ShortUrl(short_url=shorturl)
    return result


"""
The website to realize redirecting method
"""


@app.post(
    "/api/v1/longurl",
    status_code=status.HTTP_200_OK,
    response_model=schemas.LongUrl,
)
def redirect_url(data: schemas.ShortUrl):
    db_accessor = DBAccessor(url_settings)
    return redirect_url_processor(data, db_accessor)


def redirect_url_processor(data: schemas.ShortUrl, db_accessor: DBAccessor):
    shorturl = data.short_url
    if db_accessor.shorturl_exists(shorturl):
        longurl = db_accessor.get_longurl(shorturl)
        return schemas.LongUrl(long_url=longurl)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"cannot find this short url: {shorturl}",
        )
