from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os


def generate_resume(data, output_path="app/uploads/output.pdf"):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    template_path = os.path.abspath("app/template")   # ⭐ ADD THIS

    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("apexon_template.html")

    html_content = template.render(**data)

    HTML(string=html_content, base_url=template_path).write_pdf(output_path)   # ⭐ ADD base_url

    return output_path