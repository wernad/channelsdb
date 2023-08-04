import json
from pathlib import Path

from api.main import app
from api.config import config


@app.get('/content', name='Database content', tags=['General'], description='Returns the counts of tunnels for each stored entry')
async def get_content() -> dict[str, list[int]]:
    with open(Path(config['dirs']['base']) / 'db_content.json') as f:
        return json.load(f)
