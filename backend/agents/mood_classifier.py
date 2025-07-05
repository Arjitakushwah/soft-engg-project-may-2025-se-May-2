from crewai import Agent, Task, Crew
import json

def classify_emotion(user_input, llm):
    sentiment_agent = Agent(
        role="Emotion Classification Psychologist",
        goal="Classify user emotion from short texts and emojis with high accuracy",
        backstory="""
            You are a seasoned psychologist specializing in emotional analysis based on digital communication.
            Your role is to identify whether someone is feeling sad, happy, excited, anxious, or neutral
            based on short messages that may include emojis.
        """,
        llm=llm,
        allow_delegation=False,
    )

    sentiment_task = Task(
        description=f"""
        Given the following message: "{user_input}", determine the user's emotional state.

        => Rules:
        - Take into account both the words and the emojis.
        - Choose the most appropriate label from:
          ["happy", "sad", "feeling good", "angry", "neutral", "anxious", "excited", "bored"]
        - Output must be a JSON with a single key `emotion`.

        Example Output:
        {{ "emotion": "happy" }}
        """,
        expected_output="A JSON object with the detected emotion",
        agent=sentiment_agent,
    )

    crew = Crew(
        agents=[sentiment_agent],
        tasks=[sentiment_task],
        verbose=True,
    )

    result = crew.kickoff(inputs={"user_input": user_input})
    raw_output = result.tasks_output[0].raw.strip()

    # Clean the JSON if wrapped in code block
    if raw_output.startswith("```json"):
        raw_output = raw_output.removeprefix("```json").removesuffix("```").strip()

    try:
        emotion_json = json.loads(raw_output)
        return emotion_json
    except Exception as e:
        print("Failed to parse JSON:", e)
        return {"emotion": "unknown"}
