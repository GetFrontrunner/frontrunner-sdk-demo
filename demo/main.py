import logging
import time

from frontrunner_sdk import FrontrunnerSDK
from frontrunner_sdk.commands.injective.get_order_books import GetOrderBooksResponse
from frontrunner_sdk.models import Order

# https://stackoverflow.com/questions/55523588/how-to-suppress-these-fake-warnings-coming-from-aiohttp
logging.getLogger('asyncio').setLevel(logging.CRITICAL)
logging.getLogger('frontrunner_sdk').setLevel(logging.WARNING)

# Frontrunner markets are in USDC and on Injective, USDC has 6 decimals.
# 1,000,000 from Injective is $1 USDC.
USDC_SCALE_FACTOR = 10 ** 6
INJECTIVE_MARKET_ID = "0xd03091c74e4e76878c2afbeb470b1c825677014afdaa3d315fa534884d2d90e1"


def create_wallet(sdk: FrontrunnerSDK):
    print("Creating and funding a wallet ...")
    response = sdk.injective.create_wallet()
    print(f"""
    Put this somewhere safe!
        {response.wallet.mnemonic}
    """)


def find_and_print_markets(sdk: FrontrunnerSDK):
    find_markets_response = sdk.frontrunner.find_markets(
        sports=["basketball"],  # Looking for basketball game markets
        event_types=["game"],  # Looking for game (instead of future) markets
        prop_types=["winner"],  # Looking for winner (instead of other) markets
        market_statuses=["active"],  # Only active markets
    )

    markets = find_markets_response.markets
    for market in markets:
        # print market and sport event info
        print(f"Market: {market.long_entity_name} [{market.prop_name}] vs {market.short_entity_name} (FR: {market.id}; Injective: {market.injective_id})")
        find_events = sdk.frontrunner.get_sport_events(id=market.sport_event_id)
        event = find_events.sport_events[0]
        print(f"Starting at {event.start_time}")

        # get the order book for this market
        response = sdk.injective.get_order_books([market.injective_id])
        print_orderbooks(response)


def submit_orders(sdk: FrontrunnerSDK):
    highest_buy = 0.01

    response = sdk.injective.create_orders([
        Order.buy_long(INJECTIVE_MARKET_ID, 10, highest_buy + 0.01),
        Order.buy_long(INJECTIVE_MARKET_ID, 5, highest_buy + 0.02),
    ])

    # lowest_ask = 0.40
    #
    # response = sdk.injective.create_orders([
    #     Order.buy_long(INJECTIVE_MARKET_ID, 2, lowest_ask),
    # ])

    print(f"""
    Transaction: {response.transaction}
    You can view your transaction at:
      https://testnet.explorer.injective.network/transaction/{response.transaction}
    """)


def print_orders(sdk: FrontrunnerSDK, state: str):
    response = sdk.injective.get_orders(mine=True, execution_types=["limit"], state=state)
    print(f"{state} orders:")
    for order in response.orders:
        print(f"{order.order_hash}: {order.quantity} @ ${int(order.price) / USDC_SCALE_FACTOR}")


def cancel_orders(sdk: FrontrunnerSDK):
    response = sdk.injective.cancel_all_orders()
    print(f"""
    Transaction: {response.transaction}
    You can view your transaction at:
      https://testnet.explorer.injective.network/transaction/{response.transaction}
    """)


def print_orderbooks(response: GetOrderBooksResponse):
    print("order_books:")
    for market_id, order_book in response.order_books.items():
        print("\tmarket:", market_id)

        print("buys:")
        for buy in order_book.buys:
            print(f"  {buy.quantity} @ ${int(buy.price) / USDC_SCALE_FACTOR}")

        print("sells:")
        for sell in order_book.sells:
            print(f"  {sell.quantity} @ ${int(sell.price) / USDC_SCALE_FACTOR}")

        # find the highest buy and lowest sell
        buy_prices = [int(order.price) / USDC_SCALE_FACTOR for order in order_book.buys]
        sell_prices = [int(order.price) / USDC_SCALE_FACTOR for order in order_book.sells]
        highest_buy = max(buy_prices) if buy_prices else "<empty>"
        lowest_sell = min(sell_prices) if sell_prices else "<empty>"
        print(f"bid-ask spread: [${highest_buy}, ${lowest_sell}]")


def get_and_print_orderbook(sdk: FrontrunnerSDK):
    response = sdk.injective.get_order_books([INJECTIVE_MARKET_ID])
    print_orderbooks(response)


def main():
    sdk = FrontrunnerSDK()
    # create_wallet(sdk)

    # find_and_print_markets(sdk)
    get_and_print_orderbook(sdk)
    # submit_orders(sdk)
    # print_orders(sdk, "booked")
    # cancel_orders(sdk)
    # print_orders(sdk, "canceled")
    print_orders(sdk, "booked")
    print_orders(sdk, "filled")
    # get_and_print_orderbook(sdk)


if __name__ == "__main__":
    main()
