import asyncio, websockets


def mark(session, bingo_id, index):
    """
    session is the code for the current card
    bingoid is the code for the generator link
    both of these reffer to the charracters after the /play/ or # in the url
    """

    async def send_message(index, session_key):
        async with websockets.connect(
            f"wss://bingobaker.com/ws?type=handshake&bingo_id={bingo_id}&session_key={session_key}"
        ) as websocket:
            message = f'{"index": {index}, "is_checked": 1, "type": "set_check", "bingo_id": {bingo_id}, "session_key": "{session_key}"}'
            await websocket.send(message)

    asyncio.get_event_loop().run_until_complete(send_message(index, session))


mark("6308504", "64ffd3d32b4cada4", 2)
