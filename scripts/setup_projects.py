"""
Project Setup Script
Creates new Python projects with proper structure
"""
# TODO: Validate input variables to prevent crashes, etc.
    
import click
from pathlib import Path


def create_readme_template(project_name, project_type):
    """Generate README content

    Args:
        project_name (str): Name of project
        project_type (str): Type of project

    Returns:
        str: Returns preformated README content
    """

    return f"""# {project_name}
Description of your project here.

## Installation
```bash
pip install -r requirements.txt
```

## Usage

[Add usage instructions]

## Project Type
{project_type}

## Development
```bash
# Run tests
pytest

# Run application
python src/main.py
```
"""


def create_gitignore_template():
    """Generate .gitignore content"""
    
    return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# IDE
.vscode/
.idea/
*.swp

# Testing
.pytest_cache/
.coverage

# OS
.DS_Store
Thumbs.db
"""


def create_requirements_template(project_type):
    """Generate requirements.txt based on project type

    Args:
        project_type (str): Type of project

    Returns:
        str: A string containing the contents of a requirements.txt file
    """
    
    base = "pytest>=7.0.0\n"
    
    if project_type == "api":
        return base + "fastapi>=0.100.0\nuvicorn>=0.23.0\n"
    elif project_type == "cli":
        return base + "click>=8.0.0\n"
    else:
        return base


def create_project_structure(project_name, project_type):
    """Create the directory structure for a new project

    Args:
        project_name (str): Name of project
        project_type (str): Type of project

    Returns:
        bool: Returns True on success, else False
    """
    
    base_path = Path(project_name)
    
    if base_path.exists():
        click.echo(f"Error: Directory '{project_name}' already exists!")
        return False
    
    directories = [
        base_path,
        base_path / "src",
        base_path / "tests",
        base_path / "docs",
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        click.echo(f"Created: {directory}")
        
    files = {
        "README.md": create_readme_template(project_name, project_type),
        ".gitignore": create_gitignore_template(),
        "requirements.txt": create_requirements_template(project_type)
    }
    
    for filename, content in files.items():
        file_path = base_path / filename
        file_path.write_text(content)
        click.echo(f"Created: {file_path}")
        
    return True


@click.command()
@click.option('--name', '-n', prompt='Project name', help='Name of the project.')
@click.option('--type', '-t', default='basic', help='Project type: basic, api, cli')
def main(name, type):
    click.echo(f"Creating project: {name}!")
    click.echo(f"Type: {type}\n")
    
    if create_project_structure(name, type):
        click.echo(f"Project '{name}' created successfully!")
        click.echo(f"Location: ./{name}/")
    else:
        click.echo("Project creation failed!")


if __name__ == '__main__':
    main()