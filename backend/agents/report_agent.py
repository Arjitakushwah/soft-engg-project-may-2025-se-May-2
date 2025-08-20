import json
from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv
load_dotenv("prod.env")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 

llm = LLM(model='gemini/gemini-2.5-flash', api_key=('your api key'))


def analyze_child_data(json_input, llm):
    analysis_agent = Agent(
        role="Child Behavioral Analyst",
        goal="Understand child well-being through data and return engaging markdown analysis",
        backstory="""
            You are a compassionate behavioral data analyst.
            You receive weekly activity summaries for children aged 8–14.
            The summaries include number of completed and pending tasks (todo, journal, story, infotainment)
            for each day, along with mood values.
            Your job is to analyze the child's behavior patterns, productivity, and emotional health.
            Present your insights in a parent-friendly markdown format.
        """,
        llm=llm,
        allow_delegation=False
    )

    data_analysis_task = Task(
        description=f"""
        Analyze the following JSON data showing a child's weekly learning and emotional activity:

        ```json
        {json.dumps(json_input, indent=2)}
        ```

        Please provide a clear **markdown report** with the following structure:

        1. **Mood Overview**
           - Count of each mood.
           - Most common mood.
        
        2. **Task Completion Insight**
           - Count of completed tasks by category (todo, journal, story, infotainment).
           - Days with full completion vs incomplete days.
        
        3. **Behavior Pattern Summary**
           - Are there signs of consistency, burnout, or disinterest?
           - Any links between mood and task completion?

        4. **Well-being Rating**
           - Your rating of the child’s overall weekly well-being: (Excellent / Good / Moderate / Needs Attention).
        
        5. **Recommendations**
           - 2–3 simple, encouraging tips to help improve emotional or task performance next week.

        Output should be clean **markdown** (no code blocks).
        """,
        expected_output="Markdown-formatted report with all sections clearly structured",
        agent=analysis_agent
    )

    crew = Crew(
        agents=[analysis_agent],
        tasks=[data_analysis_task],
        verbose=True
    )

    result = crew.kickoff(inputs={})
    output = result.tasks_output[0].raw.strip()

    # Clean up markdown formatting if wrapped in ```markdown blocks
    if output.startswith("```markdown"):
        output = output.removeprefix("```markdown").strip()
    if output.endswith("```"):
        output = output.removesuffix("```").strip()

    return output




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

