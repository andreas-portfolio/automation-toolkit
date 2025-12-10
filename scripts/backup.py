"""
Backup Automation
Creates timestamped compressed backups of directories
"""

import click
import tarfile
from datetime import datetime
from pathlib import Path


def should_exclude(tarinfo):
    """Filter out unwanted files/directories

    Args:
        tarinfo (TarInfo): TarInfo object containing details of what is about to be archived

    Returns:
        TarInfo: The tarinfo object if file should be included, None if excluded
    """    
    
    exclude_patterns = ['__pycache__', '.git', 'venv', '.pyc', '.pytest_cache']
    
    for pattern in exclude_patterns:
        if pattern in tarinfo.name:
            return None # Exclude file
    return tarinfo # Include file


def prune_backups(destination, keep):
    """Prune number of backups (default: 5)

    Args:
        destination (str): Path to backup directory
        keep (int): Number of backup files to keep
    
    Returns:
        None
    """
    
    backup_dir = Path(destination)
    backup_files = list(backup_dir.glob('*tar.gz'))
    
    # Sort backups by age
    sorted_files = sorted(backup_files, key=lambda f: f.stat().st_mtime)
    
    # Prune amount of files until they are as many as 'keep' specifies
    to_delete = sorted_files[:-keep]
    
    for f in to_delete:
        f.unlink()
    

def create_archive(source, destination):
    """Create archive and backup directory

    Args:
        source (str): Directory user wishes to backup
        destination (str): Directory where the user wishes the backup to be stored
        
    Returns:
        None
    """
    
    source_path = Path(source)
    dest_dir = Path(destination)

    dest_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    archive_name = f"{source_path.name}_{timestamp}.tar.gz"
    archive_path = dest_dir / archive_name    
    
    with tarfile.open(archive_path, 'w:gz') as f:
        f.add(source_path, arcname=source_path.name, filter=should_exclude)
        
    click.echo(f"Backup created: {archive_path}")

        
@click.command()
@click.option('--source', '-s', required=True, help='Directory to backup')
@click.option('--destination', '-d', required=True, help='Where to save backup')
@click.option('--keep', '-k', default=5, help='Number of backups to save (default: 5)')
def main(source, destination, keep):
    """Create compressed backup of directory"""

    create_archive(source, destination)
    prune_backups(destination, keep)


if __name__ == '__main__':
    main()