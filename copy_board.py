import http.client
import json
from dotenv import load_dotenv
import os
import re

# Load environment variables from the .env file
load_dotenv()

API_TOKEN = os.getenv('MIRO_API_TOKEN')

conn = http.client.HTTPSConnection("api.miro.com")

headers = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'Authorization': API_TOKEN
}

for board_number in range(2, 33):

    board_name = "Thought Leader Talk: Rose " + str(board_number)

    payload = json.dumps({
        "name": board_name,
        "policy": {
            "permissionsPolicy": {
                "copyAccess": "team_members",
                "sharingAccess": "team_members_with_editing_rights"
            },
            "sharingPolicy": {
                "access": "edit",
                "inviteToAccountAndBoardLinkAccess": "editor",
                "teamAccess": "edit"
            }
        }
    }
    )

    conn.request("PUT", "/v2/boards?copy_from=uXjVKtatbPo=", payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data)

    #   print(data.decode("utf-8"))
    print('\"' + board_name + '\",\"' + json_data['viewLink'] + '\"')


