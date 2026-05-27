import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()


def build_llm() -> LLM:
    return LLM(
        model="gemini/gemini-2.0-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.7,
    )


def run_discovery(industry: str) -> str:
    llm = build_llm()
    search = SerperDevTool()

    researcher = Agent(
        role="B2B Industry Researcher",
        goal=(
            f"Uncover the most painful workflow inefficiencies in the {industry} industry "
            "by finding what real workers and businesses complain about"
        ),
        backstory=(
            "You are an expert at finding real-world pain points by digging into Reddit threads, "
            "Hacker News discussions, LinkedIn posts, and G2/Capterra reviews. "
            "You focus on recurring operational problems that waste significant time or money for businesses."
        ),
        tools=[search],
        llm=llm,
        verbose=True,
    )

    competitor_scanner = Agent(
        role="Competitive Intelligence Analyst",
        goal=(
            f"Map every existing AI and software tool targeting the {industry} industry, "
            "then pinpoint the gaps where users are still underserved"
        ),
        backstory=(
            "You are a sharp analyst who reads between the lines of product reviews and forum complaints. "
            "You find what tools exist, what they promise, and — more importantly — "
            "what frustrated users say is still broken or missing."
        ),
        tools=[search],
        llm=llm,
        verbose=True,
    )

    scorer = Agent(
        role="AI Product Strategist",
        goal=(
            "Synthesize all research findings and rank the top 3 AI automation opportunities "
            "by scoring them on market size, feasibility, and competitive whitespace"
        ),
        backstory=(
            "You have evaluated hundreds of AI use cases for enterprise clients. "
            "You score each opportunity ruthlessly on: Market Size, Automation Feasibility with today's LLMs, "
            "and Competitive Whitespace. You think in terms of ROI and time saved for the buyer."
        ),
        llm=llm,
        verbose=True,
    )

    brief_writer = Agent(
        role="Product Brief Writer",
        goal=(
            "Write tight, compelling one-page product briefs for each top opportunity "
            "that a founder could hand to an investor or an enterprise client today"
        ),
        backstory=(
            "You write crisp, insight-packed product briefs used by venture studios. "
            "You know how to frame a problem so a non-technical buyer immediately feels the pain, "
            "and how to describe an AI solution so a technical founder knows exactly what to build."
        ),
        llm=llm,
        verbose=True,
    )

    research_task = Task(
        description=(
            f"Research the {industry} industry to find its top workflow inefficiencies and daily pain points. "
            "Search Reddit, LinkedIn, Hacker News, and software review sites. "
            "Focus on: what tasks consume the most time, what causes the most errors, "
            "what do front-line workers and managers complain about most. "
            "Find at least 6 distinct pain points with a real source or quote for each."
        ),
        expected_output=(
            "A structured list of 6+ pain points. For each: the pain point name, "
            "who experiences it (job title), how much time or money it wastes, "
            "and one evidence quote or source."
        ),
        agent=researcher,
    )

    competitor_task = Task(
        description=(
            f"Scan the existing software and AI tools targeting the {industry} industry. "
            "For each major tool note: what it does, its pricing tier, and its top 3 user complaints from reviews. "
            "Then identify at least 3 clear gaps — problems the research found that no existing tool solves well."
        ),
        expected_output=(
            "A competitive landscape with: 5+ tools and their weaknesses, "
            "followed by 3 clearly identified market gaps with reasoning."
        ),
        agent=competitor_scanner,
        context=[research_task],
    )

    scoring_task = Task(
        description=(
            "Using the pain points and competitive gaps identified, score and rank the top 3 AI automation opportunities. "
            "For each opportunity score out of 10: Market Size, Automation Feasibility with current LLMs, "
            "Competitive Whitespace. Show the total score and a 2-3 sentence justification."
        ),
        expected_output=(
            "Top 3 ranked opportunities formatted as a scoring table with total scores and justification paragraphs."
        ),
        agent=scorer,
        context=[research_task, competitor_task],
    )

    brief_task = Task(
        description=(
            "Write a product brief for each of the top 3 ranked opportunities. "
            "Each brief must include exactly these 6 sections: "
            "1. Problem Statement (2 sentences, make the pain visceral), "
            "2. AI-Powered Solution (3 sentences, describe the agent workflow), "
            "3. Target Buyer (job title + company size + industry segment), "
            "4. Quantified ROI (specific hours saved or cost reduced per week per user), "
            "5. Why Now (1 sentence — what changed in AI that makes this possible today), "
            "6. Suggested MVP (what to build in 2 weeks to validate). "
            "Separate each brief with a clear divider."
        ),
        expected_output=(
            "Three complete, formatted product briefs each with all 6 sections clearly labeled."
        ),
        agent=brief_writer,
        context=[scoring_task],
    )

    crew = Crew(
        agents=[researcher, competitor_scanner, scorer, brief_writer],
        tasks=[research_task, competitor_task, scoring_task, brief_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(inputs={"industry": industry})
    return str(result)
