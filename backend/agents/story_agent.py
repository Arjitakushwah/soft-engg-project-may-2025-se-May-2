import os
# from dotenv import load_dotenv
from crewai import  Agent, Task, Process, LLM , Crew
import json
import os


def generate_story(prompt , llm ):
    
    
    story_agent = Agent(
        role="English Lecturer At Oxford University",
        goal="Generate an age-appropriate story for 8–14-year-old children that is entertaining, imaginative, and includes a quiz to reinforce comprehension.",
        backstory="""
            You are a passionate English literature lecturer at Oxford University who believes in nurturing imagination and critical thinking in young minds. 
            You have experience in storytelling, children's literature, and education psychology. 
            Your stories are crafted to engage children between the ages of 8 and 14 with age-appropriate language, themes like friendship, courage, curiosity, and learning, and they always include a short quiz to help children reflect on the story.
        """,
        llm=llm,
        allow_delegation=False,
    )

    story_task = Task(
        description=f"""
        Create a short 100 words story suitable for children aged 8 to 14. The story should be imaginative, engaging, and convey a positive theme or moral.
        It should be original, written in simple yet rich language, and contain at least one central character, a clear plot, and a resolution.


        => Important Story Rules:
        a. Story must be child friendly and should be based on childs wish: {prompt}
        b. Choose one of the following theme: ["Kindness","Courage","Friendship","Bravery","Honesty", "Perseverance", "Imagination","Empathy","Respect",
                 "Curiosity","Teamwork","Sharing","Forgiveness", "Belonging","Hope","Trust","Unity","Patience","Tolerance","Joy"]
        c. Json should be well-structured with the given keys.
        d. Quiz question should be apt.
        d. Quiz option should be exactly 4.
        

        The output must be a well-structured JSON object with the following keys no other explations , just a json:
        - title: Title of the story (str)
        - theme: Central idea or moral of the story (str)
        - content: The full story text in a marked-down format (str)
        - quiz:
            question: A simple comprehension question based on the story (str),
            options: A list of 4 possible answers (List[str]),
            answer: The correct option (str)
        """,
        expected_output="A well-structured json object",
        agent=story_agent,
    )

    crew = Crew(
        agents=[story_agent],
        tasks=[story_task],
        verbose=True,
    )

    crew_inputs={"prompt":prompt}

    result = crew.kickoff(inputs=crew_inputs)
    first_output_obj = result.tasks_output[0]
    first_output = first_output_obj.raw
   

    if first_output.startswith("```json"):
        first_output = first_output.removeprefix("```json")
    if first_output.endswith("```"):
        first_output = first_output.removesuffix("```")

    first_output = first_output.strip()

    print("cleaned output:")
    print(first_output)

    try:
        story_json = json.loads(first_output)
        return story_json
    except Exception as e:
        print("failed to parse json:", e)
        return "no story"
