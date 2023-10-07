import os
import openai

# pull from environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]
