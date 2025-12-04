"""
Log Analyzer
A tool used to parse application log files to extract useful information such as which errors have occured and how many.
"""

import click
import re
from collections import Counter

LEVELS = ['INFO', 'WARNING', 'ERROR', 'CRITICAL', 'DEBUG']

def extract_error_details(line):
    """Extract timestamp, level, and message from ERROR/CRITICAL lines"""
    pattern = r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (ERROR|CRITICAL) (.+)'
    match = re.search(pattern, line)
    
    if match:
        return {
            'timestamp': f"{match.group(1)} {match.group(2)}",
            'level': match.group(3),
            'message': match.group(4).strip()
        }
    return None


def match_level(line):
    """Extract log level from a line"""
    pattern = r'INFO|WARNING|ERROR|CRITICAL|DEBUG'
    match = re.search(pattern, line)
    if match:
        return match.group(0)
    return None


def analyze_file(filepath):
    """Read file and count log levels"""
    levels = []
    errors = [] 
    
    try:
        with open(filepath, 'r') as file:
            for line in file:
                level = match_level(line)
                if level:
                    levels.append(level)
                    
                    # If ERROR/CRITICAL, extract details
                    if level in ['ERROR', 'CRITICAL']:
                        error_info = extract_error_details(line)
                        if error_info:
                            errors.append(error_info)
    
    except FileNotFoundError:
        click.echo(f"Error: File '{filepath}' not found!")
        return None, None
    
    counts = Counter(levels)
    
    # Print summary
    click.echo(f"Found {len(levels)} total log entries\n")
    for level in LEVELS:
        count = counts.get(level, 0)
        click.echo(f"- {level}: {count}")
    
    # Print errors found
    click.echo(f"\nFound {len(errors)} error/critical entries")
    
    return counts, errors  # Return both


@click.command()
@click.option('--input', '-i', 'input_file', required=True, help='Path to log file.')
@click.option('--format', '-f', 'output_format', default='json', help='Output format: json or csv')
def main(input_file, output_format):
    """Analyze log file and generate report"""
    click.echo(f"Analyzing log file: {input_file}\n")
    
    analyze_file(input_file)
    

if __name__ == '__main__':
    main()