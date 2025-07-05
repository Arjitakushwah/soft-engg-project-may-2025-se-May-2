# from crewai_tools import tool
from crewai.tools import BaseTool
from crewai.tools import tool

from exa_py import Exa
import os
from crewai import Task, Crew, Agent , LLM

from dotenv import load_dotenv
load_dotenv("exaa.env")

exa_api_key = os.getenv("exa_api_key")


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

    parsedResult = ''.join([
      f'<Title id={idx}>{eachResult.title}</Title>'
      f'<URL id={idx}>{eachResult.url}</URL>'
      f'<Highlight id={idx}>{"".join(eachResult.highlights)}</Highlight>'
      for (idx, eachResult) in enumerate(response.results)
    ])

    return parsedResult

def generate_news(prompt , llm ):
    news_agent = Agent(
    role="Child-Focused News Journalist and Researcher",
    goal="Provide accurate, simplified, and age-appropriate news for children aged 8 to 14 in an engaging markdown format.",
    backstory="""
        You are an experienced journalist and researcher who specializes in crafting child-appropriate news. 
        Your mission is to inform and educate children aged 8 to 14 about current events, science, culture,inovation and important topics in a way that is age-appropriate, safe, and easy to understand.
        You follow journalistic ethics, avoid sensationalism, and aim to inspire curiosity, empathy, and awareness in young readers.
    """,
    llm=llm,
    tools=[search_and_get_contents_tool ],
    allow_delegation=False,
)

    news_task = Task(
    description=f"""
    Generate a child-friendly news article based on this topic or interest using the tool on this topic: {prompt}.

    Return the outpiut in a well-structured markdown format.
    
    => Guidelines for Writing:
    a. The content must be factual, age-appropriate for 8–14-year-old readers, and avoid disturbing or complex details.
    b. Provide short explain the topic clearly, using simple but engaging language.
    c. Use markdown formatting for structure (headings, bullet points, etc.).
    d. Include 5 news highlights with titles, URLs, and brief summaries.
    
    The output must be a well-structured markdwon text.
    
    """,
    expected_output="A well-structured markdown text",
    agent=news_agent,
)

    crew = Crew(
        agents=[news_agent],
        tasks=[news_task],
        verbose=True,
    )

    crew_inputs={"prompt":prompt}
    result = crew.kickoff(inputs=crew_inputs)
    first_output_obj = result.tasks_output[0]
    first_output = first_output_obj.raw
    if first_output.startswith("```markdown"):
        first_output = first_output.removeprefix("```markdown")
    if first_output.endswith("```"):
        first_output = first_output.removesuffix("```")

    first_output = first_output.strip()

    print("cleaned output:")
    print(first_output)

    try:
        # story_json = json.loads(first_output)
        return first_output
    except Exception as e:
        print("some error came", e)
        return "no news"

