from app.template.template_service import generate_resume


def template_agent(state):
    data = state["validated_data"]

    path = generate_resume(data)

    state["output_path"] = path

    return state
