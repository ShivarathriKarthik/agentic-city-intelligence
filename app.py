from dotenv import load_dotenv
load_dotenv()

import os
import requests
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_core.runnables import RunnableLambda
from langchain.agents import create_agent
from tavily import TavilyClient


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="City Intelligence Agent",
    page_icon="🌆",
    layout="wide"
)


# ============================================================
# UI
# ============================================================

st.title("🌆 City Intelligence Agent")

st.caption(
    "AI-powered weather and latest news assistant"
)


# ============================================================
# WEATHER TOOL
# ============================================================

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""

    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(
        url,
        timeout=10
    )

    data = response.json()

    if str(data.get("cod")) != "200":
        return (
            f"Could not get weather for {city}. "
            f"Reason: {data.get('message', 'Unknown error')}"
        )

    temp = data["main"]["temp"]

    desc = data["weather"][0]["description"]

    humidity = data["main"]["humidity"]

    wind_speed = data["wind"]["speed"]

    return (
        f"Weather in {city}:\n"
        f"Condition: {desc}\n"
        f"Temperature: {temp}°C\n"
        f"Humidity: {humidity}%\n"
        f"Wind Speed: {wind_speed} m/s"
    )


# ============================================================
# NEWS TOOL
# ============================================================

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def get_news(city: str) -> str:
    """Get the latest news about a city."""

    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    results = response.get(
        "results",
        []
    )

    if not results:
        return f"No latest news found for {city}."

    news_list = []

    for r in results:

        title = r.get(
            "title",
            "No title"
        )

        url = r.get(
            "url",
            ""
        )

        content = r.get(
            "content",
            ""
        )

        news_list.append(
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Summary: {content[:1000]}"
        )

    return (
        f"Latest news in {city}:\n\n"
        + "\n\n".join(news_list)
    )


# ============================================================
# LLM
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0
)


# ============================================================
# AGENT
# ============================================================

agent = create_agent(

    model=llm,

    tools=[
        get_weather,
        get_news
    ],

    system_prompt=(
        "You are a City Intelligence Assistant. "
        "You can provide current weather and latest news "
        "for cities. "
        "When the user asks about weather, use the weather tool. "
        "When the user asks about news, use the news tool. "
        "When the user asks for both, use both tools. "
        "Do not ask the user for permission before using tools. "
        "Automatically execute the required tools and provide "
        "a clear final answer."
    )
)


# ============================================================
# RUNNABLE
# ============================================================

def prepare_input(user_input: str) -> str:
    """
    Clean and prepare the user query.
    """

    return user_input.strip()


input_runnable = RunnableLambda(
    prepare_input
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Ask about weather or news..."
)


if user_input:

    # ========================================================
    # RUNNABLE
    # ========================================================

    cleaned_input = input_runnable.invoke(
        user_input
    )


    # ========================================================
    # USER MESSAGE
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": cleaned_input
        }
    )


    with st.chat_message("user"):

        st.markdown(
            cleaned_input
        )


    # ========================================================
    # AGENT
    # ========================================================

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Agent is working..."
        ):

            try:

                result = agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": cleaned_input
                            }
                        ]
                    }
                )


                # ====================================================
                # FINAL MESSAGE
                # ====================================================

                final_message = (
                    result["messages"][-1]
                )

                content = final_message.content


                # ====================================================
                # HANDLE GEMINI STRUCTURED CONTENT
                # ====================================================

                if isinstance(
                    content,
                    list
                ):

                    text_parts = []

                    for block in content:

                        if (
                            isinstance(block, dict)
                            and block.get("type") == "text"
                        ):

                            text_parts.append(
                                block.get(
                                    "text",
                                    ""
                                )
                            )

                    content = "\n".join(
                        text_parts
                    )


                # ====================================================
                # DISPLAY
                # ====================================================

                st.markdown(
                    content
                )


                # ====================================================
                # SAVE ASSISTANT RESPONSE
                # ====================================================

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": content
                    }
                )


            except Exception as e:

                st.error(
                    f"Agent error: {str(e)}"
                )