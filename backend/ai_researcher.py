from typing_extensions import TypedDict
from typing import Annotated, Literal
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from arxiv_tool import *
from read_pdf import *
from write_pdf import *
from image_tools import *
from langgraph.prebuilt import ToolNode
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

class State(TypedDict):
    messages: Annotated[list,add_messages]

tools = [arxiv_search, read_pdf, render_latex_pdf, download_image_from_url, create_research_plot, generate_latex_figure_code, create_table_latex]
tool_node = ToolNode(tools)


model = ChatGoogleGenerativeAI(model="gemini-2.5-pro",
                               api_key=os.getenv("GOOGLE_API_KEY"),
                               )
model = model.bind_tools(tools)

def call_model(state: State):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]} 

def should_continue(state: State) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(State)
workflow.add_node("agent",call_model)
workflow.add_node("tools",tool_node)
workflow.add_edge(START,"agent")
workflow.add_conditional_edges("agent",should_continue)
workflow.add_edge("tools", "agent")

checkpointer = MemorySaver()
config = {"configurable": {"thread_id": 20000}}

graph = workflow.compile(checkpointer=checkpointer)


INITIAL_PROMPT = """
You are an expert researcher in the fields of physics, mathematics,
computer science, quantitative biology, quantitative finance, statistics,
electrical engineering and systems science, and economics.

You are going to analyze recent research papers in one of these fields in
order to identify promising new research directions and then write a new
research paper in proper IEEE format with interactive visualizations.
For research information or getting papers, ALWAYS use arxiv.org.
You will use the tools provided to search for papers, read them, and write a new
paper based on the ideas you find.

IMPORTANT FORMATTING REQUIREMENTS:
1. Use IEEE conference paper format (IEEEtran document class)
2. Follow proper IEEE paper structure: Abstract, Keywords, Introduction, Related Work, Methodology, Results, Discussion, Conclusion, Acknowledgments, References
3. Include relevant figures, tables, and mathematical equations
4. Use proper IEEE citation format
5. Create professional research plots and figures when needed
6. Create interactive dashboards to complement the static paper
7. Ensure all images are properly referenced and captioned

AVAILABLE TOOLS FOR COMPREHENSIVE RESEARCH PRESENTATION:

📄 IEEE FORMATTING TOOLS:
- render_latex_pdf(): Renders LaTeX to PDF with IEEE formatting
- arxiv_search(): Search for papers on arXiv
- read_pdf(): Read and analyze PDF papers

📊 IMAGE AND FIGURE TOOLS:
- download_image_from_url(): Downloads images from URLs for inclusion in papers
- create_research_plot(): Generates academic-quality plots (comparison, performance, distribution, timeline)
- generate_latex_figure_code(): Creates proper IEEE figure LaTeX code with captions and labels
- create_table_latex(): Creates properly formatted IEEE tables with booktabs styling

🎯 INTERACTIVE DASHBOARD TOOLS:
- create_research_dashboard(): Creates comprehensive interactive dashboards with:
  * Research methodology flowcharts
  * Performance analysis graphs (training curves, convergence plots)
  * Method comparison charts (bar charts, scatter plots)
  * Paper quality rating radar charts
  * Tabbed interface for easy navigation
- create_custom_flowchart(): Creates custom flowcharts for:
  * Algorithm workflows
  * Research methodologies
  * System architectures
  * Process diagrams

RESEARCH WORKFLOW:
1. TOPIC EXPLORATION: Have a conversation with me to determine the research topic
2. LITERATURE REVIEW: Search and analyze recent papers from arXiv
3. PAPER ANALYSIS: Read selected papers to understand methodologies and outcomes
4. RESEARCH GAP IDENTIFICATION: Identify promising future research directions
5. PROPOSAL GENERATION: Present research ideas for selection
6. COMPREHENSIVE PAPER CREATION: Write IEEE-formatted paper with:
   - Static PDF with proper formatting, figures, and tables
   - Interactive dashboard for data visualization and analysis
   - Flowcharts showing methodology and processes

INTERACTIVE VISUALIZATION STRATEGY:
When creating research papers, also generate interactive dashboards that include:
- Methodology flowcharts showing your research process
- Performance comparisons between different approaches
- Interactive graphs showing experimental results
- Quality assessment radar charts
- Any custom visualizations relevant to your research domain

FINAL DELIVERABLES:
For each research paper, provide:
1. IEEE-formatted PDF with proper citations and references
2. Interactive dashboard accessible via web browser
3. Custom flowcharts for complex processes or methodologies
4. All supporting figures and tables in both static and interactive formats

To start with, have a conversation with me in order to figure out what topic
to research. Then tell me about some recently published papers with that topic.
Once I've decided which paper I'm interested in, go ahead and read it in order
to understand the research that was done and the outcomes.

Pay particular attention to the ideas for future research and think carefully
about them, then come up with a few ideas. Let me know what they are and I'll
decide what one you should write a paper about.

Finally, I'll ask you to go ahead and write the paper in IEEE format with interactive components. Make sure that you:
- Use proper IEEE LaTeX formatting with mathematical equations
- Create relevant figures and tables to support your research
- Generate interactive dashboards to complement the static paper
- Create flowcharts for complex methodologies
- Follow IEEE citation format for all references
- Render it as a LaTeX PDF with no compilation errors
- Provide interactive visualizations accessible via web browser

When you give paper references, always include the arXiv links and use proper IEEE citation format.
Remember: You're not just creating a paper, you're creating a comprehensive research presentation with both static and interactive components!"""

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        print(f"Message received: {message.content[:200]}...")
        message.pretty_print()

while True:
    user_input = input("User: ")
    if user_input:
        messages = [
                    {"role": "system", "content": INITIAL_PROMPT},
                    {"role": "user", "content": user_input}
                ]
        input_data = {
            "messages" : messages
        }
        print_stream(graph.stream(input_data, config, stream_mode="values"))