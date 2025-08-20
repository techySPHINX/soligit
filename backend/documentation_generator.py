from jinja2 import Environment, FileSystemLoader

def generate_file_tree_graph(file_tree):
    graph = "graph TD;\n"

    for item in file_tree:
        if "/" in item:
            parent_dir, current_dir = item.rsplit("/", 1)
            graph += f"{parent_dir}-->{current_dir}\n"

    return graph

def generate_documentation_html(project_name, documentation, mermaid_graph):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('documentation_template.html')

    return template.render(
        project_name=project_name,
        documentation=documentation,
        mermaid_graph=mermaid_graph
    )

