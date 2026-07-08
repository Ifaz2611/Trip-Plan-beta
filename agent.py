import os
import json
import gradio as gr
from google import genai
from google.genai import types
from dotenv import load_dotenv
from duckduckgo_search import DDGS

# Load environment variables
load_dotenv()
client = genai.Client()


# ==========================================
# 1. DEFINE THE REAL TOOL (Web Search)
# ==========================================

def search_accessibility_info(location: str) -> str:
    """REAL TOOL: Searches the web for wheelchair accessibility info."""
    log_msg = f"[Tool Executed] Searching web for: {location} accessibility...\n"
    query = f"wheelchair accessibility {location} entrance restrooms ramps"
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if not results:
                return log_msg, f"No specific accessibility information found for {location}."
            
            summary = f"Web search results for '{location}':\n"
            for i, r in enumerate(results, 1):
                summary += f"{i}. {r['body']}\n"
            return log_msg, summary
            
    except Exception as e:
        return log_msg, f"Error performing search: {str(e)}"

available_tools = {"search_accessibility_info": search_accessibility_info}
tool_config = [search_accessibility_info]

# ==========================================
# 2. THE UI AGENT CONROLLER
# ==========================================

def ui_agent_runner(user_goal: str):
    """
    This function handles the Agent loop and yields updates 
    directly to the Gradio interface in real-time.
    """
    if not user_goal.strip():
        return "Please enter a valid travel goal.", "No activity."

    system_instruction = (
        "You are an expert Accessibility Trip Planner AI. Your goal is to help wheelchair users plan safe and accessible trips. "
        "Use the search tool to gather real information about locations. Think step-by-step. "
        "Once you have enough information, provide a final, encouraging, and detailed itinerary."
    )
    
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=tool_config,
            temperature=0.2
        )
    )
    
    current_prompt = user_goal
    max_steps = 5 
    agent_logs = "Starting Agentic Loop...\n"
    
    yield "Thinking and searching...", agent_logs

    for step in range(max_steps):
        agent_logs += f"\n--- Step {step + 1} ---\n"
        yield "Thinking...", agent_logs
        

        response = chat.send_message(current_prompt)
        

        if response.function_calls:
            agent_logs += "Agent decided to call a search tool.\n"
            yield "Searching the web...", agent_logs
            
            tool_responses = []
            for call in response.function_calls:
                if call.name in available_tools:
                    location = call.args.get("location")
                    
                    tool_log, observation = available_tools[call.name](location)
                    
                    agent_logs += tool_log
                    agent_logs += f"[Observation] Found data snippet ({len(observation)} chars).\n"
                    yield "Processing search results...", agent_logs
                    
                    tool_responses.append(
                        types.Part.from_function_response(
                            name=call.name,
                            response={"result": observation}
                        )
                    )
            
            current_prompt = tool_responses
            
        else:
            # Final Answer reached!
            agent_logs += "\nFinal itinerary generated successfully!"
            yield response.text, agent_logs
            break
    else:
        agent_logs += "\nHit maximum execution steps."
        yield "Failed to generate complete itinerary within step limits.", agent_logs

# ==========================================
# 3. GRADIO UI INTERFACE LAYOUT
# ==========================================


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Accessible Trip Planner Agent")
    gr.Markdown("Enter your destination goals below. The AI Agent will dynamically research accessibility details using live web search tools.")
    
    with gr.Row():
        with gr.Column(scale=2):
            user_input = gr.Textbox(
                label="Where do you want to go?", 
                placeholder="e.g., Plan a half-day trip to downtown Chicago. I want to visit Millennium Park and the Art Institute.",
                lines=3
            )
            submit_btn = gr.Button("Generate Accessible Itinerary", variant="primary")
            
            final_output = gr.Markdown(label="Your Itinerary", value="*Your itinerary will appear here...*")
            
        with gr.Column(scale=1):
            log_output = gr.Textbox(
                label="Agent Execution Logs (Reasoning & Tools)", 
                interactive=False, 
                lines=20
            )
            
    submit_btn.click(
        fn=ui_agent_runner,
        inputs=[user_input],
        outputs=[final_output, log_output]
    )

if __name__ == "__main__":
    demo.launch()