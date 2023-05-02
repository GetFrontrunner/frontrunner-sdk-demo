import logging
from datetime import datetime, timezone

from frontrunner_sdk import FrontrunnerSDK

# https://stackoverflow.com/questions/55523588/how-to-suppress-these-fake-warnings-coming-from-aiohttp
logging.getLogger('asyncio').setLevel(logging.CRITICAL)
logging.getLogger('frontrunner_sdk').setLevel(logging.WARNING)


def main():
    sdk = FrontrunnerSDK()

    sports_response = sdk.frontrunner.get_sports()
    print("sports:\n", sports_response.sports)

    leagues_response = sdk.frontrunner.get_leagues()
    print("leagues:\n", leagues_response.leagues)

    sport = "basketball"
    leagues_response = sdk.frontrunner.get_leagues(sport=sport)
    league = leagues_response.leagues[0]
    league_id = league.id

    sport_events_response = sdk.frontrunner.get_sport_events(league_id=league_id, starts_since=datetime.now(tz=timezone.utc))
    print(f"{sport} sport events:\n", sport_events_response.sport_events)

    sport_entities_response = sdk.frontrunner.get_sport_entities(league_id=league_id)
    print(f"first 5 {sport} sport entities:\n", sport_entities_response.sport_entities[:5])

    props_response = sdk.frontrunner.get_props(league_id=league_id)
    print(f"first 5 {sport} props:\n", props_response.props[:5])


if __name__ == "__main__":
    main()
