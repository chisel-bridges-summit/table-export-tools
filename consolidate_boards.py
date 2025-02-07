import http.client
import json

conn = http.client.HTTPSConnection("api.miro.com")

headers = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'Authorization': 'Bearer '
}


def create_target_board(target_board_name):
    payload = json.dumps({
        "description": target_board_name,
        "name": target_board_name,
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

    conn.request("POST", "/v2/boards", payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data)

    print('Creating board ' + target_board_name)
    print('Status: ' + str(res.status))
    if res.status == 201:
        print('Link:' + json_data['viewLink'])
    else:
        quit('Failed to create target board')

    return json_data['id']


def copy_stickies(target_board_id, source_board_ids):

    x_offset = 0
    payload = ''

    for source_board_id in source_board_ids:

        max_x_pos = 0
        more_data = True
        cursor = ''

        while more_data:

            print('Getting list of stickies from board ' + source_board_id)

            if cursor == '':
                conn.request("GET", "/v2/boards/" + source_board_id + "/items?type=sticky_note", payload, headers)
            else:
                conn.request("GET", "/v2/boards/" + source_board_id + "/items?type=sticky_note&cursor=" + cursor, payload, headers)
                print('  Cursor found, retrieving more stickies')
            res = conn.getresponse()
            data = res.read()
            json_data = json.loads(data)

            print('Status: ' + str(res.status))
            if res.status == 200:
                if cursor == '':
                    print('Number of stickies found: ' + str(json_data['total']))
            else:
                quit('Failed to retrieve list of stickies from board ' + source_board_id)

            data = json_data['data']
            for sticky_data in data:
                max_x_pos = max(max_x_pos, sticky_data['position']['x'])
                copy_sticky(sticky_data['id'], x_offset, source_board_id, target_board_id)

            x_offset += max_x_pos

            if 'cursor' in json_data:
                cursor = json_data['cursor']
            else:
                more_data = False


def copy_sticky(sticky_id, x_offset, source_board_id, target_board_id):

    print('Getting details for sticky: ' + sticky_id + ' from board: ' + source_board_id)

    payload = ''

    conn.request("GET", "/v2/boards/" + source_board_id + "/sticky_notes/" + sticky_id, payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data)

    print('Status: ' + str(res.status))

    if res.status == 200:
        print('Success')
    else:
        quit('Failed to retrieve details for sticky: ' + sticky_id)

    x_pos = json_data['position']['x'] + x_offset

    payload = json.dumps({
        "data": {
            "content": json_data['data']['content'],
            "shape": json_data['data']['shape']
        },
        "style": {
            "fillColor": json_data['style']['fillColor'],
            "textAlign": json_data['style']['textAlign'],
            "textAlignVertical": json_data['style']['textAlignVertical']
        },
        "position": {
            "x": x_pos,
            "y": json_data['position']['y']
        },
        "geometry": {
            "height": json_data['geometry']['height']
        }
    }
    )

    print('Payload: ' + payload)

    if json_data['data']['content'] == '':
        print('Skipping blank sticky: ' + sticky_id)
    else:
        print('Creating copy of sticky: ' + sticky_id)

        conn.request("POST", "/v2/boards/" + target_board_id + "/sticky_notes", payload, headers)
        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data)

        print('Status: ' + str(res.status))

        if res.status == 201:
            print('Success')
        else:
            quit('Failed to create copy of sticky: ' + sticky_id)


source_boards = {'uXjVKtEW5iI=', 'uXjVKtEW5jg=', 'uXjVKtEdZ0I=', 'uXjVKtEQ20M=', 'uXjVKtEQ2pw=', 'uXjVKtEQ2rU=', 'uXjVKtEdZ2Q='}

target_board = create_target_board("All Problems and Constraints Ideas")
copy_stickies(target_board, source_boards)
