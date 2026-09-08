from crewai import Agent, Crew, LLM, Process, Task

from config import GEMINI_API_KEY, GEMINI_MODEL


def create_llm() -> LLM:
    """Create the Gemini LLM used by CrewAI."""
    return LLM(
        model=f"gemini/{GEMINI_MODEL}",
        api_key=GEMINI_API_KEY,
    )


def create_demo_agent() -> Agent:
    """Create a simple agent for validating CrewAI + Gemini integration."""
    llm = create_llm()

    return Agent(
        role="Software Project Planning Assistant",
        goal="Understand a software project idea and summarize its main purpose.",
        backstory=(
            "You are an experienced software project planning assistant "
            "helping developers transform project ideas into structured plans."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_demo_task(agent: Agent) -> Task:
    """Create a simple task for the demo agent."""
    return Task(
        description=(
            "Analyze the following software project idea and provide a "
            "short summary of its purpose:\n\n"
            "A Hospital Management System that manages patients, doctors, "
            "appointments, and medical records."
        ),
        expected_output=(
            "A clear 3 to 5 sentence summary explaining the purpose of "
            "the Hospital Management System."
        ),
        agent=agent,
    )


def run_demo() -> str:
    """Run a minimal CrewAI workflow."""
    agent = create_demo_agent()
    task = create_demo_task(agent)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    return str(result)


if __name__ == "__main__":
    result = run_demo()

    print("\n" + "=" * 60)
    print("CREWAI DEMO RESULT")
    print("=" * 60)
    print(result)