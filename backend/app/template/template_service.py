from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os


def generate_resume(data, output_path="app/uploads/output.pdf"):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    env = Environment(loader=FileSystemLoader("app/template"))
    template = env.get_template("apexon_template.html")

    html_content = template.render(**data)

    HTML(string=html_content).write_pdf(output_path)

    return output_path