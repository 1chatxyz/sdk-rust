from pathlib import Path


def test_plugin_yaml_exists():
    path = Path(__file__).resolve().parents[1] / "plugin.yaml"
    assert path.is_file()
    assert "myconversation" in path.read_text()
