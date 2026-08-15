import json
import re


class RepositoryService:


    def __init__(self):

        with open(
            "data/processes.json",
            "r"
        ) as file:

            self.processes = json.load(file)



    def normalize_text(self, text):

        if not text:
            return ""

        text = text.lower()

        # replace hyphens with spaces
        text = text.replace("-", " ")

        # remove special characters
        text = re.sub(
            r"[^a-z0-9\s]",
            "",
            text
        )

        # remove extra spaces
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()



    def search_process(self, query):


        query = self.normalize_text(
            query
        )


        best_match = None

        best_score = 0



        for process in self.processes:


            # Support both possible JSON keys

            process_name = self.normalize_text(

                process.get(
                    "process_name",
                    process.get(
                        "name",
                        ""
                    )
                )

            )


            if not process_name:

                continue



            score = 0



            # Exact match gets highest priority

            if query == process_name:

                score = 100



            # Query contains process name

            elif process_name in query:

                score = 80



            # Process name contains query

            elif query in process_name:

                score = 60



            else:

                # Word matching

                query_words = set(
                    query.split()
                )

                process_words = set(
                    process_name.split()
                )


                common_words = (
                    query_words &
                    process_words
                )


                if common_words:

                    score = len(common_words) * 10



            # Keep highest scoring match

            if score > best_score:

                best_score = score

                best_match = process



        return best_match