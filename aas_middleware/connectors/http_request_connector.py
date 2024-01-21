import aiohttp


class HttpRequestConnector:
    def __init__(self, url: str):
        self.url = url

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def send(self, body: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, data=body) as response:
                return await response.text()

    async def receive(self) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                return await response.text()
