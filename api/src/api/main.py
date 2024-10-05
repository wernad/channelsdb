from fastapi import FastAPI
from channelsdb.api.database.database import SessionLocal

app = FastAPI(title='ChannelsDB 2.0 API',
              contact={'name': 'Tomáš Raček', 'email': 'tomas.racek@ceitec.muni.cz'},
              redoc_url=None, docs_url='/',
              version='beta',
              swagger_ui_parameters={'syntaxHighlight': False, 'defaultModelsExpandDepth': -1})

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()