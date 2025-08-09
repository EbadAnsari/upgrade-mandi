import os
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from notion_client import Client
from utils.utils import notionObject2DataFrame

load_dotenv()

AUTH_TOKEN = os.getenv("NOTION_AUTH")
DATABASE_SWIGGY_ID = os.getenv("DATABASE_SWIGGY_ID")

notion = Client(auth=AUTH_TOKEN)


responseDf = pd.DataFrame(
    columns=result["properties"].keys(),
)

print("Loaded")

startCursor = None

while True:
    response = notion.databases.query(
        database_id=DATABASE_SWIGGY_ID,
        filter={"property": "Date", "date": {"equals": "2025-05-15"}},
        start_cursor=startCursor,
    )
    print(startCursor)
    for result in response["results"]:
        responseDf = pd.concat(
            [responseDf, notionObject2DataFrame(result)], ignore_index=True
        )
    if response.get("has_more"):
        startCursor = response["next_cursor"]
    else:
        break

print(responseDf)
