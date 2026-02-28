from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os


def generate_resume(data, template_name="template1.html", output_path="app/uploads/output.pdf"):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    template_path = os.path.abspath("app/template")

    env = Environment(loader=FileSystemLoader(template_path))

    # 🔥 THIS LINE IS IMPORTANT
    template = env.get_template(template_name)

    html_content = template.render(**data)

    HTML(string=html_content, base_url=template_path).write_pdf(output_path)

    return output_path