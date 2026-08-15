from services.repository_service import RepositoryService
from services.tavily_service import TavilyService



class KnowledgeAgent:


    def __init__(self):

        self.repository = RepositoryService()

        self.tavily = TavilyService()



    def find_process(self, query):


        # First search internal repository

        process = self.repository.search_process(
            query
        )


        if process:

            return {

                "source": "internal_repository",

                "data": process

            }



        # If not found, search Tavily

        web_results = self.tavily.search(
            query
        )


        return {

            "source": "tavily",

            "data": web_results

        }




    def explain_process(self, process):


        # Internal repository response

        if process.get("source") == "internal_repository":


            return self.format_process_response(

                process.get("data")

            )



        # Tavily response

        elif process.get("source") == "tavily":


            return self.format_tavily_response(

                process.get("data")

            )



        else:


            return {

                "status": "failed",

                "message": "Unknown source"

            }




    def format_process_response(self, process):


        return {


            "status": "completed",


            "source": "internal_repository",


            "process_name":

            process.get(
                "name"
            ),


            "owner":

            process.get(
                "owner"
            ),


            "department":

            process.get(
                "department"
            ),


            "overview": {


                "purpose":

                process.get(
                    "purpose"
                ),


                "description":

                process.get(
                    "description"
                )

            },


            "process_flow":

            process.get(
                "activities",
                []
            ),


            "inputs":

            process.get(
                "inputs",
                []
            ),


            "outputs":

            process.get(
                "outputs",
                []
            ),


            "key_metrics":

            process.get(
                "kpis",
                []
            ),


            "automation_opportunities":

            process.get(
                "automation_candidates",
                []
            ),


            "related_processes":

            process.get(
                "related_processes",
                []
            )

        }




    def format_tavily_response(self, results):


        formatted_results = []


        for result in results.get(
            "results",
            []
        ):


            formatted_results.append(

                {

                    "title":
                    result.get(
                        "title"
                    ),

                    "url":
                    result.get(
                        "url"
                    ),

                    "content":
                    result.get(
                        "content"
                    )

                }

            )



        return {


            "status": "completed",


            "source": "tavily",


            "search_results":

            formatted_results

        }