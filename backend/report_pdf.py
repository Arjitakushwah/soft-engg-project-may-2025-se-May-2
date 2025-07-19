import markdown2
from weasyprint import HTML
import tempfile

def generate_pdf(markdown_text):
    raw_html = markdown2.markdown(markdown_text)

    styled_html = f"""
    <html>
<head>
    <style>
        body {{
            font-family: Arial, Helvetica, sans-serif;
            padding: 30px;
            background-color: #ffffff;
            color: #333;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
            border-bottom: 2px solid #ccc;
            padding-bottom: 5px;
        }}
        p {{
            font-size: 16px;
            line-height: 1.6;
        }}
        ul {{
            list-style-type: square;
            margin-left: 20px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            font-family: monospace;
            color: #d63384;
        }}
        blockquote {{
            background-color: #fff3cd;
            border-left: 5px solid #ffc107;
            margin: 20px;
            padding: 10px 20px;
            font-style: italic;
            color: #856404;
        }}
        .task-complete {{
            color: #28a745;
            font-weight: bold;
        }}
        .task-incomplete {{
            color: #dc3545;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    {raw_html}
</body>
</html>
"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as pdf_file:
        pdf_path = pdf_file.name

    HTML(string=styled_html).write_pdf(pdf_path)
    return pdf_path
