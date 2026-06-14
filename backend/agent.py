import os
import json
from typing import TypedDict, Annotated, Sequence
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from pydantic import ValidationError
from dotenv import load_dotenv
from tavily import TavilyClient

from models import StudentProfile, GuidanceResponse, CareerPath, University, Scholarship, FreeCourse

load_dotenv()

# Check for API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if GROQ_API_KEY:
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)
else:
    llm = None

if TAVILY_API_KEY:
    tavily = TavilyClient(api_key=TAVILY_API_KEY)
else:
    tavily = None

# Define Graph State
class AgentState(TypedDict):
    profile: StudentProfile
    analysis: str
    search_results: str
    final_response: dict

def analyze_profile(state: AgentState) -> AgentState:
    profile = state["profile"]
    sys_msg = SystemMessage(content="You are an expert career counselor for Pakistani students. Analyze the student's FSC background and interests to suggest 3 high-potential career paths in the local and global market.")
    user_msg = HumanMessage(content=f"FSC Group: {profile.fsc_group}, Marks: {profile.fsc_marks}, Interests: {profile.interests}, City: {profile.city}. Give a brief analysis of suitable career paths.")
    
    response = llm.invoke([sys_msg, user_msg]) if llm else HumanMessage(content="LLM not configured.")
    return {"analysis": response.content}

def search_opportunities(state: AgentState) -> AgentState:
    profile = state["profile"]
    analysis = state.get("analysis", "")
    
    # We use Tavily to search for Universities, Scholarships, and Courses in Pakistan
    # To save tokens and time, we do a combined query
    query = f"Top universities for {profile.fsc_group} in {profile.city} Pakistan, scholarships for FSC students with {profile.fsc_marks} marks, and free online courses for {profile.interests}"
    
    try:
        if tavily:
            search_response = tavily.search(query=query, search_depth="basic", max_results=3)
            search_results = json.dumps(search_response.get("results", []))
        else:
            search_results = "Tavily search not configured."
    except Exception as e:
        search_results = f"Search failed: {str(e)}"
        
    return {"search_results": search_results}

def synthesize_response(state: AgentState) -> AgentState:
    profile = state["profile"]
    analysis = state["analysis"]
    search_results = state["search_results"]
    
    sys_msg = SystemMessage(content="""You are a Career Guidance AI. 
Based on the student's profile, the analysis, and the search results, output a structured JSON response EXACTLY matching the GuidanceResponse schema.
Do not include any markdown formatting like ```json, just output the raw JSON object.

Schema:
{
  "career_paths": [{"title": "str", "description": "str", "skills_required": ["str"]}],
  "universities": [{"name": "str", "programs": ["str"], "estimated_fee": "str", "merit_info": "str"}],
  "scholarships": [{"name": "str", "description": "str", "eligibility": "str", "link": "str or null"}],
  "free_courses": [{"title": "str", "platform": "str", "link": "str"}],
  "roadmap_summary": "str"
}
""")
    
    user_msg = HumanMessage(content=f"""
Profile: {profile.json()}
Analysis: {analysis}
Search Results: {search_results}

Generate the JSON response:
""")
    
    if llm:
        response = llm.invoke([sys_msg, user_msg])
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        try:
            final_dict = json.loads(content)
        except json.JSONDecodeError:
            # Fallback
            final_dict = {"error": "Failed to parse LLM output as JSON."}
    else:
        final_dict = {"error": "LLM not configured."}
        
    return {"final_response": final_dict}

# Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("analyze", analyze_profile)
workflow.add_node("search", search_opportunities)
workflow.add_node("synthesize", synthesize_response)

workflow.set_entry_point("analyze")
workflow.add_edge("analyze", "search")
workflow.add_edge("search", "synthesize")
workflow.add_edge("synthesize", END)

app_graph = workflow.compile()

def run_agent(profile: StudentProfile):
    initial_state = {"profile": profile}
    result = app_graph.invoke(initial_state)
    return result.get("final_response", {})
