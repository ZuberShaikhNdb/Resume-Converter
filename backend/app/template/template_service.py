from jinja2 import Environment, FileSystemLoader
import pdfkit
import os


def generate_resume(data, output_path="app/uploads/output.pdf"):

    env = Environment(loader=FileSystemLoader("app/template"))
    template = env.get_template("apexon_template.html")

    html_content = template.render(**data)

    wk_path = os.getenv("WKHTMLTOPDF_PATH")
    config = pdfkit.configuration(wkhtmltopdf=wk_path)

    pdfkit.from_string(html_content, output_path, configuration=config)

    return output_path
