import asyncio
import logging

from frontrunner_sdk import FrontrunnerSDKAsync

# https://stackoverflow.com/questions/55523588/how-to-suppress-these-fake-warnings-coming-from-aiohttp
logging.getLogger('asyncio').setLevel(logging.CRITICAL)
logging.getLogger('frontrunner_sdk').setLevel(logging.WARNING)

# Frontrunner markets are in USDC and on Injective, USDC has 6 decimals.
# 1,000,000 from Injective is $1 USDC.
USDC_SCALE_FACTOR = 10 ** 6
INJECTIVE_MARKET_ID = "0xd03091c74e4e76878c2afbeb470b1c825677014afdaa3d315fa534884d2d90e1"


async def stream_trades(sdk: FrontrunnerSDKAsync):
    print("streaming trades: ")
    response = await sdk.injective.stream_trades([INJECTIVE_MARKET_ID], mine=True)

    async for trade in response.trades:
        print("trade:", trade.operation_type, trade.trade.order_hash)

    print("exited stream")


async def main():
    sdk = FrontrunnerSDKAsync()
    await stream_trades(sdk)


if __name__ == "__main__":
    asyncio.run(main())
