from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.tools.job_search import search_jobs
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class AgentState(TypedDict):
    user_query: str
    role: str
    location: str
    experience: str
    jobs: list
    response: str


def query_parser_node(state: AgentState):
    print("QUERY PARSER NODE STARTED")
    prompt = f"""
    Extract the following information from the user query.

    Return ONLY valid JSON.

    Fields:
    - role
    - location
    - experience

    User Query:
    {state["user_query"]}
    """
    print("BEFORE GROQ CALL")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You extract structured job search information."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    print("AFTER GROQ CALL")
    content = response.choices[0].message.content

    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )

    content = content.strip()
     
    print("CLEANED CONTENT:")
    print(content)

    parsed = json.loads(content)
    
    print("PARSED JSON:")
    print(parsed)

    return {
        "role": parsed.get("role", ""),
        "location": parsed.get("location", ""),
        "experience": str(parsed.get("experience", ""))
    }

def job_search_node(state: AgentState):

    jobs = search_jobs(
    state["role"],
    state["location"]
    )
    print(
    f"Searching for: "
    f"{state['role']} "
    f"in {state['location']}"
)

    return {    
        "jobs": jobs
    }


def llm_response_node(state: AgentState):

    return {
        "response": state["jobs"]
    }

graph = StateGraph(AgentState)

graph.add_node(
    "query_parser",
    query_parser_node
)

graph.add_node(
    "job_search",
    job_search_node
)

graph.add_node(
    "llm_response",
    llm_response_node
)

graph.set_entry_point(
    "query_parser"
)

graph.add_edge(
    "query_parser",
    "job_search"
)

graph.add_edge(
    "job_search",
    "llm_response"
)

graph.add_edge(
    "llm_response",
    END
)

job_agent = graph.compile()