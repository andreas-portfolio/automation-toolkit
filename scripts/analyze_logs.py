"""
Log Analyzer
A tool used to parse application log files to extract useful information such as which errors have occured and how many.
"""

import click
import re
from collections import Counter
import json
import csv
from pathlib import Path

LEVELS = ['INFO', 'WARNING', 'ERROR', 'CRITICAL', 'DEBUG']

def save_report(input_file, result, output_format):
    """Save report to file"""
    
    # Generate output filename
    input_path = Path(input_file)
    base_name = input_path.stem + "_report"
    
    # If json: build dict and json.dump()
    if output_format == 'json':
        output_file = base_name + '.json'
        
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
            
    # if csv: csv.DictWriter and writerows()
    elif output_format == 'csv':
        output_file  = base_name + '.csv'
        
        with open(output_file , 'w', newline='') as f:
            fieldnames = ['message', 'count', 'first_seen']
            writer = csv.DictWriter(f, fieldnames)
            
            writer.writeheader()
            for message, values in result.items():
                # Because we are providing writerow() with a nested dict instead of a flat structure
                # we have to apply the 'message' header to the error message here.
                writer.writerow({
                'message': message,
                'count': values['count'],
                'first_seen': values['first_seen']
                })
                
    else:
        click.echo(f"Unknown format: {output_format}")
        return
        
    click.echo(f"Report saved to: {output_file}")
    
    

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
    
    return result


@click.command()
@click.option('--input', '-i', 'input_file', required=True, help='Path to log file.')
@click.option('--format', '-f', 'output_format', default='json', help='Output format: json or csv')
def main(input_file, output_format):
    """Analyze log file and generate report"""
    
    click.echo(f"Analyzing log file: {input_file}\n")
    
    result = analyze_file(input_file)
    save_report(input_file, result, output_format)

if __name__ == '__main__':
    main()