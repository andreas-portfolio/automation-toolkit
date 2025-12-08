"""
Backup Automation
Creates timestamped compressed backups of directories
"""

import click
import tarfile
from datetime import datetime
from pathlib import Path
    

def create_archive(source, destination, *keep):
    source_path = Path(source)
    dest_dir = Path(destination)

    dest_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    archive_name = f"{source_path}_{timestamp}.tar.gz"
    archive_path = dest_dir / archive_name    
    
    with tarfile.open(archive_path, 'w:gz') as f:
        f.add(source_path, arcname=source_path.name)
        f.close()
        
    click.echo(f"Backup created: {archive_path}")

        
@click.command()
@click.option('--source', '-s', required=True, help='Directory to backup')
@click.option('--destination', '-d', required=True, help='Where to save backup')
@click.option('--keep', '-k', default=5, help='Number of backups to save (default: 5)')
def main(source, destination, keep):
    """Create compressed backup of directory"""

    create_archive(source, destination, keep)


if __name__ == '__main__':
    main()