from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

# Get API key from Render environment variable
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)


def travel_planner(destination, days, budget, interests):

    prompt = f"""
You are an expert travel planning assistant.

Create a practical travel plan for:

Destination: {destination}
Number of days: {days}
Budget: {budget}
Interests: {interests}

Give the answer in this structure:

1. Trip Overview

2. Day-by-Day Itinerary

3. Places to Visit

4. Food Suggestions

5. Approximate Budget Breakdown

6. Travel Tips

Make the plan realistic, simple and easy to understand.

Do not invent exact prices or claim information is current
unless you are certain.
"""

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful travel planning assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        destination = request.form["destination"]
        days = request.form["days"]
        budget = request.form["budget"]
        interests = request.form["interests"]

        result = travel_planner(
            destination,
            days,
            budget,
            interests
        )

    return render_template(
        "index.html",
        result=result
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
