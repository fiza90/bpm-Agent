import os

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


class ResponseAgent:


    def __init__(self):

        self.client = OpenAI(
    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    ),
    base_url="https://openrouter.ai/api/v1"
)



    def generate_response(self, data):


        prompt = f"""

You are a Business Process Management expert.

Convert the following information into a structured BPM response.

Include:

- Process Name
- Overview
- Key Activities
- Inputs
- Outputs
- KPIs
- Automation Opportunities
- Sources (if available)

Information:

{data}

"""


        response = self.client.chat.completions.create(

            model="openai/gpt-4o-mini",

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ]

        )


        return response.choices[0].message.content