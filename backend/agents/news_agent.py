from crewai import Agent, Task, Crew
from crewai.tools import tool
from dotenv import load_dotenv
import os
from datetime import datetime
from exa_py import Exa
from crewai import LLM
import json

load_dotenv("exaa.env")


# load_dotenv("prod.env") 
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# llm = LLM(model='gemini/gemini-2.0-flash', api_key=GOOGLE_API_KEY)  # Replace with your actual LLM API key


load_dotenv("exaa.env")
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

def generate_news(prompt, llm):

    

    # Create agent
    news_agent = Agent(
        role="Child Infotainment Writer",
        goal="Create engaging, factual, and age-appropriate infotainment stories for children using real-time web search results",
        backstory="""
        You are an expert children's content writer with a flair for turning real-world information into fascinating infotainment.
        """,
        llm=llm,
        tools=[search_and_get_contents_tool],
        allow_delegation=False
    )

    # Create task
    news_task = Task(
        description=f"""
You are an expert children's content writer with a flair for turning real-world information into fascinating infotainment.

Your job is to take a child’s query or interest (like 'space', 'dinosaurs', 'robots', 'oceans') and find interesting, real, safe facts about it using a web search tool.

SO FOR THIS TOPIC: {prompt}. WRITE NEWS STORIES FOR CHILDREN AGED 8–14 YEARS.

### Output format:
Return a list of **4 JSON objects**. Each story should follow this structure:
{{
  "title": "string, exciting and age-appropriate",
  "summary": "2–3 line simple explanation that amazes children",
  "read_more": "URL as a string"
}}

### Rules:
- Use **real facts** from the web search tool.
- Make each story fun, creative, and safe for kids.
- Content should be age-appropriate, light, inspiring, and curious in tone.
- Avoid violence, politics, scary or adult topics.
- Each story must follow the same format (Title, Summary, Link).
- Don't include extra text, Markdown, or formatting.
- Return only a valid list of JSON objects, no explanations.
        """,
        expected_output="A JSON array of 4 child-friendly news story objects",
        agent=news_agent,
    )

    crew = Crew(
        agents=[news_agent],
        tasks=[news_task],
        verbose=True,
    )

    crew_inputs = {"prompt": prompt}
    result = crew.kickoff(inputs=crew_inputs)

    output = result.tasks_output[0].raw.strip()

    if output.startswith("```json"):
        output = output.removeprefix("```json")
    if output.endswith("```"):
        output = output.removesuffix("```")

    output = output.strip()
    output=json.dumps(json.loads(output), indent=2)


    # print("inside")

    # print(output)
    return output



# json_output = generate_news("space robots",llm)
# print(json.dumps(json.loads(json_output), indent=2))
















# # --------------------------- AI News Generator ---------------------------
# def generate_news(prompt, llm):
#     # Create agent
#     news_agent = Agent(
#         role="Child Infotainment Writer",
#         goal="Create engaging, factual, and age-appropriate infotainment stories for children using real-time web search results",
#         backstory="""
#        Create engaging, factual, and age-appropriate infotainment stories for children using real-time web search results.
#         """,
#         llm=llm,
#         tools=[search_and_get_contents_tool],
#         allow_delegation=False
#     )

#     # Create task
#     news_task = Task(
#         description=f"""
# You are an expert children's content writer with a flair for turning real-world information into fascinating infotainment. 
# Your job is to take a child’s query or interest (like 'space', 'dinosaurs', 'robots', 'oceans') and find interesting, real, safe facts about it through web search.

# SO FOR THIS TOPIC: {prompt}. WRITE NEWS STORIES FOR CHILDREN OF AGE 8-14 YEARS.
# Then write **4 simple, fascinating news stories**, each in the following format and style:

# ---

# Title (1 line):
# Make it exciting, clear, and informative for a young audience.

# **Summary (2–3 lines):**
# Write in simple, engaging language. Explain the topic so that a curious child can understand and feel amazed. Avoid any scary, violent, or age-inappropriate content.

# **Read more:**
# Include a relevant URL where the child can read more, starting with `[Read more](...)`.

# ---

# ### Rules:
# - Use only **Markdown**
# - Include exactly **4** clearly separated stories.
# - Each story must follow the same format (Title, Summary, Link).
# - Use **facts from the web search tool**
# - Content should be age-appropriate, light, inspiring, and curious in tone.
# - Avoid any complex political, medical, or mature topics.

# Expected Output:
# Markdown text with 4 infotainment stories in the structure above.
#         """,
#         expected_output="Markdown with 4 clearly separated child-friendly stories",
#         agent=news_agent,
#     )

#     # Create and run Crew
#     crew = Crew(
#         agents=[news_agent],
#         tasks=[news_task],
#         verbose=True,
#     )

#     crew_inputs = {"prompt": prompt}
#     result = crew.kickoff(inputs=crew_inputs)

#     # Extract and clean output
#     output = result.tasks_output[0].raw
#     if output.startswith("```markdown"):
#         output = output.removeprefix("```markdown")
#     if output.endswith("```"):
#         output = output.removesuffix("```")
#     return output.strip()

# --------------------------- AI News Generator ---------------------------