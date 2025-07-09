import asyncio
import aiohttp
import nest_asyncio

# Example list of tickers; populate with many more as needed
TICKERS = ["AAPL", "TSLA", "SPY"]

async def fetch(session, ticker):
    async with session.get(f"https://finance.yahoo.com/quote/{ticker}") as resp:
        await resp.text()

async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(fetch(session, t) for t in TICKERS))

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
