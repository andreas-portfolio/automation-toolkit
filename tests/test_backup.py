"""
Tests for backup script
"""
from click.testing import CliRunner
from scripts.backup import main, create_archive, prune_backups


def test_prune_backups(tmp_path):
    dest = tmp_path / "backup"
    dest.mkdir()

    for i in range(10):
        f = dest / f"test_{i}.tar.gz"
        f.write_text("x")

    prune_backups(dest, keep=5)

    files = list(dest.glob("*.tar.gz"))
    assert len(files) == 5


def test_create_archive(tmp_path):
    source_dir = tmp_path / "my-project"
    source_dir.mkdir()
    dest_dir = tmp_path / "dest"

    create_archive(str(source_dir), str(dest_dir))
    
    backups = list(dest_dir.glob("*.tar.gz"))
    assert len(backups) == 1
    

def test_main(tmp_path):
    runner = CliRunner()
    
    source_dir = tmp_path / "test-source"
    source_dir.mkdir()
    
    dest_dir = tmp_path / "backups"
    
    result = runner.invoke(main, ["-s", str(source_dir), "-d", str(dest_dir), "-k", 2])
    
    assert result.exit_code == 0
    assert "Backup created" in result.output
