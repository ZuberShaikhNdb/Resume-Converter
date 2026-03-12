from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os


def generate_resume(data, template_name, output_path):

    # Ensure output folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Template folder path
    template_path = os.path.abspath("app/template")

    env = Environment(loader=FileSystemLoader(template_path))

    # Load selected template (IND.html or USA.html)
    template = env.get_template(template_name)

    html_content = template.render(**data)

    # Generate PDF
    HTML(string=html_content, base_url=template_path).write_pdf(output_path)

    return output_path