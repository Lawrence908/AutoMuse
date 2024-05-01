from automator import Automator

def main():
    automator = Automator("config.json")
    automator.automate()


if __name__ == "__main__":
    main()



from quote_fetcher import QuoteFetcher

def main():
    quote_fetcher = QuoteFetcher()

    # Fetch a random quote from a file
    quote = quote_fetcher.fetch_quote('quotes.json')
    print(quote)

    # Fetch a random quote from the API with a specific topic
    quote = quote_fetcher.fetch_quote_from_api('inspiration')
    print(quote)

    # Fetch the tags
    tags = quote_fetcher.fetch_tags()
    print(tags)

    # Here you can continue with setting up your GUI, using the fetched quotes and tags

if __name__ == "__main__":
    main()