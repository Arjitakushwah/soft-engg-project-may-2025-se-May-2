from crewai import Agent, Task, Crew
from crewai.tools import tool
from dotenv import load_dotenv
import os
from datetime import datetime
from exa_py import Exa

load_dotenv("agents/exaa.env")
exa_api_key = os.getenv("exa_api_key")

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
        role="Child Infotainment Writer",
        goal="Create engaging, factual, and age-appropriate infotainment stories for children using real-time web search results",
        backstory="""
       Create engaging, factual, and age-appropriate infotainment stories for children using real-time web search results.
        """,
        llm=llm,
        tools=[search_and_get_contents_tool],
        allow_delegation=False
    )

    # Create task
    news_task = Task(
        description=f"""
You are an expert children's content writer with a flair for turning real-world information into fascinating infotainment. 
Your job is to take a child’s query or interest (like 'space', 'dinosaurs', 'robots', 'oceans') and find interesting, real, safe facts about it through web search.

SO FOR THIS TOPIC: {prompt}. WRITE NEWS STORIES FOR CHILDREN OF AGE 8-14 YEARS.
Then write **4 simple, fascinating news stories**, each in the following format and style:

---

Title (1 line):
Make it exciting, clear, and informative for a young audience.

**Summary (2–3 lines):**
Write in simple, engaging language. Explain the topic so that a curious child can understand and feel amazed. Avoid any scary, violent, or age-inappropriate content.

**Read more:**
Include a relevant URL where the child can read more, starting with `[Read more](...)`.

---

### Rules:
- Use only **Markdown**
- Include exactly **4** clearly separated stories.
- Each story must follow the same format (Title, Summary, Link).
- Use **facts from the web search tool**
- Content should be age-appropriate, light, inspiring, and curious in tone.
- Avoid any complex political, medical, or mature topics.

Expected Output:
Markdown text with 4 infotainment stories in the structure above.
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
