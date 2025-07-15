import json
from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv
load_dotenv("prod.env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 

llm = LLM(model='gemini/gemini-2.0-flash', api_key=('your api key'))


def analyze_child_data(json_input, llm):
    analysis_agent = Agent(
        role="Child Behavioral Analyst",
        goal="Understand child well-being through data and return engaging markdown analysis",
        backstory="""
            You are a compassionate behavioral data analyst. 
            You receive weekly activity logs from children aged 8–14. Your job is to extract key patterns from their journaling, mood ratings, and time/activity logs to generate useful insights about their mental well-being.
            Present your analysis in a markdown format that’s suitable for parents, guardians, or educators.
        """,
        llm=llm,
        allow_delegation=False
    )

    data_analysis_task = Task(
        description=f"""
        Given the following JSON data of a child's weekly activity:

        ```json
        {json.dumps(json_input, indent=2)}
        ```

        Perform a structured analysis that includes:

        - Mood summary (count of each mood, most common mood)
        - Sentiment analysis from journal entries (positive, negative, neutral)
        - Time management trends (days completed vs skipped)
        - Stories read (total, average, trend)

         Format your analysis in **markdown** and include:

        1. **Mood Overview** – breakdown with bullet points
        2. **Journal Sentiment Insight** – what kind of mood/thoughts are expressed
        3. **Time Management & Activity Summary** – engagement level
        4. **Well-being Rating** – overall mental health impression (happy/stressed/sad)
        5.  Recommendations – 2-3 tips to improve emotional or activity balance

        The markdown should be clean, structured, and simple to read.
        """,
        expected_output="Structured markdown with sections and bullet points",
        agent=analysis_agent
    )

    crew = Crew(
        agents=[analysis_agent],
        tasks=[data_analysis_task],
        verbose=True,
    )

    result = crew.kickoff(inputs={})
    first_output_obj = result.tasks_output[0]
    first_output = first_output_obj.raw

    if first_output.startswith("```markdown"):
        first_output = first_output.removeprefix("```markdown")
    if first_output.endswith("```"):
        first_output = first_output.removesuffix("```")

    return first_output.strip()



# json_input = {
#     "name": "Aryan",
#     "age": 11,
#     "entries": [
#         {"day": "Monday", "journal": "I felt good after yoga and helped mom", "mood": "happy", "stories_read": 1, "time_management_done": 1},
#         {"day": "Tuesday", "journal": "I got scolded and felt bad", "mood": "sad", "stories_read": 0, "time_management_done": 0},
#         {"day": "Wednesday", "journal": "I learned new words and played chess", "mood": "happy", "stories_read": 2, "time_management_done": 1},
#         {"day": "Thursday", "journal": "Too much homework made me tired", "mood": "stressed", "stories_read": 1, "time_management_done": 1},
#         {"day": "Friday", "journal": "I watched a cartoon and laughed", "mood": "happy", "stories_read": 3, "time_management_done": 1}
#     ]
# }



# markdown_output = analyze_child_data(json_input, llm)

# with open("child_analysis_report.md", "w") as f:
#     f.write(markdown_output)

