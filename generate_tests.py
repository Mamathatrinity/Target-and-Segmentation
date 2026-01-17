import yaml
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

def load_spec():
    with open(BASE / "specs/application_spec.yaml") as f:
        return yaml.safe_load(f)

def write_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)

def generate():
    spec = load_spec()
    for module in spec["modules"]:
        for api in module["apis"]:
            api_test = f'''
from mcp.api_tools import call_api

def test_{api["name"]}_positive():
    response = call_api("{api["endpoint"]}", valid=True)
    assert response.status_code == {api["success_status"]}
'''
            write_file(BASE / f"tests/api/test_{api['name']}.py", api_test)

            if api["db_validation"]["enabled"]:
                db_test = f'''
from mcp.db_tools import fetch_record

def test_{api["name"]}_db():
    record = fetch_record("{api["db_validation"]["table"]}")
    assert record is not None
'''
                write_file(BASE / f"tests/db/test_{api['name']}_db.py", db_test)

            if api["ui_validation"]["enabled"]:
                ui_test = f'''
def test_{api["name"]}_ui(page):
    page.goto("{module["base_ui_path"]}")
    assert page.locator("text={module["name"]}").is_visible()
'''
                write_file(BASE / f"tests/ui/test_{api['name']}_ui.py", ui_test)

if __name__ == "__main__":
    generate()
