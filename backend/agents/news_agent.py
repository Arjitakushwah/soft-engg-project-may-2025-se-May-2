from crewai import Agent, Task, Crew
from crewai.tools import tool
from dotenv import load_dotenv
import os
from datetime import datetime
from exa_py import Exa

load_dotenv("exaa.env") 
exa_api_key = os.getenv("your api key")

# --------------------------- Tool Setup ---------------------------
@tool('Exa search and get contents')
def search_and_get_contents_tool(question: str) -> str:
    """
    Tool using Exa's Python SDK to run semantic search and return result highlights.
    """
    exa = Exa(exa_api_key)

    response = exa.search_and_contents(
        question,
        type="neural",
        num_results=5,
        highlights=True
    )

    parsed_result = ''.join([
        f'<Title id={idx}>{eachResult.title}</Title>\n'
        f'<URL id={idx}>{eachResult.url}</URL>\n'
        f'<Highlight id={idx}>{"".join(eachResult.highlights)}</Highlight>\n\n'
        for (idx, eachResult) in enumerate(response.results)
    ])
    return parsed_result


# --------------------------- AI News Generator ---------------------------
def generate_news(prompt, llm):
    # Create agent
    news_agent = Agent(
        role="Child-Friendly News Creator",
        goal="Generate four clear and fun stories for kids aged 8–14 based on a given topic or prompt",
        backstory="""
        You are a kind and fun journalist who explains things in a way that kids aged 8–14 will love and understand.
        You tell true, positive, and exciting stories — not scary or hard things. You explain clearly, like a good storyteller.
        Each story must feel like a short, separate paragraph with a title, a few lines of text, and a helpful link.
        """,
        llm=llm,
        tools=[search_and_get_contents_tool],
        allow_delegation=False
    )

    # Create task
    news_task = Task(
        description=f"""
Use the tool to gather information about: "{prompt}". Then write **4 simple and clear stories**, each as a **paragraph** with:

1. A fun and clear **title** (`##` heading).
2. A **short summary** in 2–3 simple lines that a child aged 8–14 can easily understand.
3. A `Read more` link below.

✅ Each story should be in this format (repeat 4 times):

---

## Story Title ✨  
This is the summary of the story. It should be short, fun, and simple to read.  
Even complicated topics should be explained using easy words.  

**[Read more here](https://example.com)**  

---

Use only `Markdown`. Make sure there are **four full stories**, clearly separated. Avoid complex or scary info.
        """,
        expected_output="Markdown with 4 clearly separated child-friendly stories",
        agent=news_agent,
    )

    # Create and run Crew
    crew = Crew(
        agents=[news_agent],
        tasks=[news_task],
        verbose=True,
    )

    crew_inputs = {"prompt": prompt}
    result = crew.kickoff(inputs=crew_inputs)

    # Extract and clean output
    output = result.tasks_output[0].raw
    if output.startswith("```markdown"):
        output = output.removeprefix("```markdown")
    if output.endswith("```"):
        output = output.removesuffix("```")
    return output.strip()
