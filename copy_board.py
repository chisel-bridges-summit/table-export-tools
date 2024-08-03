import http.client
import json

conn = http.client.HTTPSConnection("api.miro.com")

headers = {
  'accept': 'application/json',
  'content-type': 'application/json',
  'Authorization': 'Bearer INSERT SECRET CODE HERE',
  'Cookie': 'AWSALBTG=p23cs0hhA9pdrd2TusjyKTZ7R9ZHMe6gKDCAGBS/Pg6JhCuWAh/0/rPg9SPpHh5mWo5ePNrt7EPdy9nPyR7vLcKeRocy18Z/7wGADvpJ7q/Tw4bvQ9nPGD+i8X6eya8hFJ1Fq8Mgty+EcmIo+M3spP8muh2M8Uux+CWrQ14AJJ92; AWSALBTGCORS=p23cs0hhA9pdrd2TusjyKTZ7R9ZHMe6gKDCAGBS/Pg6JhCuWAh/0/rPg9SPpHh5mWo5ePNrt7EPdy9nPyR7vLcKeRocy18Z/7wGADvpJ7q/Tw4bvQ9nPGD+i8X6eya8hFJ1Fq8Mgty+EcmIo+M3spP8muh2M8Uux+CWrQ14AJJ92'
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


