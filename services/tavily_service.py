import os

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()


class TavilyService:

    def __init__(self):

        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY not found in environment variables."
            )

        self.client = TavilyClient(
            api_key=api_key
        )


    def search(self, query):

        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )

        return response