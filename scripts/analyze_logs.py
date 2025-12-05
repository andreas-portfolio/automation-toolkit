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
    
    grouped_errors = {}
    
    # Extract and group errors and their timestamps
    for error in errors:
        message = error['message']
        timestamp = error['timestamp']
        
        if message not in grouped_errors:
            grouped_errors[message] = []
            
        grouped_errors[message].append(timestamp)
    
    result = {}
    
    # Count errors and save when they were first seen
    for message, timestamps in grouped_errors.items():
        result[message] = {
            'count': len(timestamps),
            'first_seen': min(timestamps)
        }
    
    sorted_results = sorted(result.items(), key=lambda result: result[1]['count'], reverse=True)
    
    counts = Counter(levels)
        
    # Print summary
    click.echo(f"Found {len(levels)} total log entries\n")
    for level in LEVELS:
        count = counts.get(level, 0)
        click.echo(f"- {level}: {count}")
    
    # Print amount of errors found
    click.echo(f"\nFound {len(errors)} error/critical entries\n")
    
    # Print which errors and when they were first seen, up to 5 to prevent clutter
    for message, info in sorted_results[:5]:
        click.echo(f"{message}: {info['count']} times, first seen {info['first_seen']}")
    
    # If the number of error messages > 5, let the user know how many without printing them all out
    if len(sorted_results) > 5:
        click.echo(f" ... and {len(sorted_results) - 5} more")
    
    return counts, result


@click.command()
@click.option('--input', '-i', 'input_file', required=True, help='Path to log file.')
@click.option('--format', '-f', 'output_format', default='json', help='Output format: json or csv')
def main(input_file, output_format):
    """Analyze log file and generate report"""
    click.echo(f"Analyzing log file: {input_file}\n")
    
    analyze_file(input_file)
    

if __name__ == '__main__':
    main()