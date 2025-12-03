"""
Environment Validator Script
Check version of Python.
Check if Git is installed (and version).
Check if Docker is installed (and version) and if it's running.
Check if minimum required disk space is available.
"""

import click
import subprocess
import sys
import shutil
from datetime import datetime

def log_result(res, verbose):
    timestamp = datetime.now().replace(microsecond=0)
    if verbose:
        with open("validation.log", "a") as file:
            if res:
                file.write((str(timestamp)) + " " + res)
    else:
        with open("validation.log", "a") as file:
            if res:
                file.write(res)

def validate_python(log=None, verbose=None):
    res = sys.version_info.major, sys.version_info.minor, sys.version_info.micro
    formated_res = f"Python version {res[0]}.{res[1]}.{res[2]} (required: 3.9+)\n"
    
    if res >= (3,9):
        click.echo(click.style("✓ " + formated_res.strip(), fg="green"))
        if log:
            log_result("Passed: " + str(formated_res), verbose)
        return 1
    else:
        click.echo(click.style(f"X Python version {res[0]}.{res[1]}.{res[2]} (required: 3.9+)", fg="red"))
        if log:
            log_result("Failed: " + str(formated_res), verbose)
        return 0

def validate_git(log=None, verbose=None):
    try:
        res = subprocess.run(["git", "--version"], capture_output=True, text=True).stdout
        formated_res = f"{res.capitalize()}"
        click.echo(click.style(f"✓ {formated_res.strip()}", fg="green"))
        if log:
            log_result("Passed: " + str(formated_res), verbose)
        return 1
    except FileNotFoundError:
        click.echo(click.style("X Git not found", fg="red"))
        if log:
            log_result("Failed: " + str(formated_res), verbose)
        return 0

def validate_docker_installed(log=None, verbose=None):
    try:
        res_installed = subprocess.run(["docker", "--version"], capture_output=True, text=True).stdout        
        formated_installed = res_installed.capitalize()
        
        click.echo(click.style(f"✓ {formated_installed.strip()}", fg="green"))
        if log:
            log_result("Passed: " + str(formated_installed), verbose)
        return 1
        
    except FileNotFoundError:
        click.echo(click.style("X Docker not found.", fg="red"))
        if log:
            log_result("Failed: Docker not found.\n", verbose)
        return 0
    
def validate_docker_running(log=None, verbose=None):
    res_running = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    
    if res_running.returncode == 0:
        click.echo(click.style("✓ Docker is running.", fg="green"))
        if log:
            log_result("Passed: Docker is running.\n", verbose)
        return 1
    else:
        click.echo(click.style("X Docker is not running.", fg="red"))
        if log:
            log_result("Failed: Docker is not running.\n", verbose)
        return 0

def validate_disk_space(log=None, verbose=None):
    res = shutil.disk_usage("./").free
    converted = res/1024**3
    formated_res = f"Disk space: {int(converted)}GB (required: >10GB)\n"
    
    if converted >= 10:
        click.echo(click.style(f"✓ Disk space: {int(converted)}GB (required: >10GB)", fg="green"))
        if log:
            log_result("Passed: " + str(formated_res), verbose)
        return 1
    else:
        click.echo(click.style(f"X Disk space: {int(converted)}GB (required: >10GB)", fg="red"))
        if log:
            log_result("Failed: " + str(formated_res), verbose)
        return 0

@click.command()
@click.option('--log', default=None, is_flag=True, help='Create a log file.')
@click.option('--verbose', default=None, is_flag=True, help='Includes timestamps in log file.')
def main(log, verbose):
    """Validate development environment setup"""
    
    if log:
        click.echo("Starting validation...\n")
        with open("validation.log", "w") as f:
            f.write("Environment Validation Log\n\n")
    else:
        click.echo("Starting validation...\n")
    
    validators = [
        validate_python(log, verbose),
        validate_git(log, verbose),
        validate_docker_installed(log, verbose),
        validate_docker_running(log, verbose), 
        validate_disk_space(log, verbose)]
    
    passed = 0
    for validator in validators:
        passed+=validator
    
    click.echo(f"\n{passed}/{len(validators)} points passed.")

if __name__ == '__main__':
    main()