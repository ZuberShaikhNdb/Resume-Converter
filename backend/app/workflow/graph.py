from langgraph.graph import StateGraph, END
from .state import ResumeState

from app.agents.parser_agent import parser_agent
from app.agents.extraction_agent import extraction_agent
from app.agents.validation_agent import validation_agent
from app.agents.template_agent import template_agent




def build_graph():
    workflow = StateGraph(ResumeState)

    workflow.add_node("parser", parser_agent)
    workflow.add_node("extractor", extraction_agent)
    workflow.add_node("validator", validation_agent)

    workflow.set_entry_point("parser")

    workflow.add_edge("parser", "extractor")
    workflow.add_edge("extractor", "validator")
    workflow.add_edge("validator", END)

    workflow.add_node("template", template_agent)

    workflow.add_edge("validator", "template")
    workflow.add_edge("template", END)

    

    return workflow.compile()

