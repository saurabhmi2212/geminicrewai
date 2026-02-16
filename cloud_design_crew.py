import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

# ==========================================
# 1. Configuration & Setup
# ==========================================
# Replace 'YOUR_API_KEY' with your actual Gemini API key, 
# or set it in your environment variables before running the script.
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "AIzaSyD__qT1sElYgxtfKab8hZUiEjOCYOBn0eg")
os.environ["CREWAI_DEFAULT_LLM"] = "gemini/gemini-2.5-flash"

# Initialize the Gemini model
# Using gemini-2.5-flash for complex reasoning and architecture design
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-latest",
    provider="google",

    temperature=0.4 # Slightly creative, but grounded in technical reality
)

# ==========================================
# 2. Define the Agents
# ==========================================
cloud_architect = Agent(
    role='Principal Cloud Architect',
    goal='Design highly scalable, resilient, and cost-effective cloud infrastructures based on user requirements.',
    backstory=(
        "You are a seasoned cloud architect with 15+ years of experience across AWS, GCP, and Azure. "
        "You excel at designing modern microservices, serverless architectures, and event-driven systems. "
        "Your primary focus is ensuring the system can handle massive scale while keeping latency low."
    ),
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

devsecops_engineer = Agent(
    role='Lead DevSecOps Engineer',
    goal='Rigorously review cloud architectures to identify vulnerabilities, ensure compliance, and enforce zero-trust security.',
    backstory=(
        "You are a paranoid but brilliant cybersecurity veteran. You specialize in cloud security posture management, "
        "IAM least-privilege policies, network isolation, and data encryption. You view every architecture through "
        "the lens of a potential attacker and fix flaws before deployment."
    ),
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

# ==========================================
# 3. Define the Tasks
# ==========================================
# The scenario we want them to work on
project_scenario = (
    "A global e-commerce platform transitioning from a monolith to microservices. "
    "It requires secure user authentication, a high-throughput inventory management system, "
    "and seamless integration with third-party payment gateways. It anticipates massive traffic spikes during holiday sales."
)

design_task = Task(
    description=(
        f"Analyze the following project scenario: '{project_scenario}'.\n"
        "Create a comprehensive cloud architecture design. You must specify the cloud provider (or multi-cloud), "
        "compute resources, databases, caching layers, message queues, and content delivery networks. "
        "Justify why you chose these specific services."
    ),
    expected_output="A detailed Architectural Design Document outlining services, data flow, and scaling strategies.",
    agent=cloud_architect
)

security_review_task = Task(
    description=(
        "Critically review the Architectural Design Document produced by the Principal Cloud Architect. "
        "Identify at least 3 potential security vulnerabilities or single points of failure. "
        "Provide concrete, actionable remediations for each vulnerability (e.g., adding WAF, adjusting VPC peering, enforcing KMS encryption)."
    ),
    expected_output="A Security Audit Report listing vulnerabilities found, risk severity, and mandatory architecture modifications.",
    agent=devsecops_engineer
)

# ==========================================
# 4. Form the Crew and Execute
# ==========================================
cloud_engineering_crew = Crew(
    agents=[cloud_architect, devsecops_engineer],
    tasks=[design_task, security_review_task],
    process=Process.sequential, # The DevSecOps engineer waits for the Architect to finish
    verbose=True
)

if __name__ == "__main__":
    print("🚀 Booting up the Automated Cloud Infrastructure Design Team...")
    print("Initiating CrewAI sequence. Please wait while the agents collaborate...\n")
    
    # Kickoff the process
    result = cloud_engineering_crew.kickoff()
    
    print("\n" + "="*50)
    print("✅ FINAL DEVSECOPS REVIEW & SECURED ARCHITECTURE")
    print("="*50 + "\n")
    print(result)