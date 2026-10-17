import aiohttp

class Client:
    def __init__(self, base_url: str):  
        self.base_url = base_url

    async def fetch(self, endpoint: str, params):
        url = f"{self.base_url}{endpoint}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 "
            "YaBrowser/26.8.0.0 Safari/537.36"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:     
                return await response.json()
                

