from openai import OpenAI

from config import (
    OPENROUTER_API_KEY,
    MODEL_NAME
)


client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


def ask_gpt(system_prompt, user_prompt):

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": user_prompt
            }

        ]

    )

    return response.choices[0].message.content