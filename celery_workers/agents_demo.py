from celery_workers.controller import celery_app
import random
import time

# celery_app = celery_app
# Simulate agent decision
AGENT_SEQUENCE = {
    "start_agent": "research_agent",
    "research_agent": "scrape_agent",
    "scrape_agent": "analyze_agent",
    "analyze_agent": "final_agent",
    "final_agent": None
}

def decide_next_agent(current_agent):
    return AGENT_SEQUENCE.get(current_agent)

# Base agent task that routes to next dynamically
@celery_app.task(bind=True)
def agent_entry(self, current_agent, context):
    print(f"{current_agent} received context: {context}")
    time.sleep(1)  # Simulate work

    # Simulate output update
    context["history"].append(current_agent)

    # Decide next agent
    next_agent_name = decide_next_agent(current_agent)
    if next_agent_name:
        print(f"{current_agent} -> Calling next agent: {next_agent_name}")
        next_func = globals()[next_agent_name]
        next_func.apply_async(args=[context])
    else:
        print(f"Final agent reached. Final context: {context}")
        return context

# Define each agent as a Celery task

@celery_app.task(name="start_agent")
def start_agent(context):
    agent_entry.apply_async(args=["start_agent", context])

@celery_app.task(name="research_agent")
def research_agent(context):
    agent_entry.apply_async(args=["research_agent", context])

@celery_app.task(name="scrape_agent")
def scrape_agent(context):
    agent_entry.apply_async(args=["scrape_agent", context])

@celery_app.task(name="analyze_agent")
def analyze_agent(context):
    agent_entry.apply_async(args=["analyze_agent", context])

@celery_app.task(name="final_agent")
def final_agent(context):
    print(f"Final agent processing context: {context}")
    return context