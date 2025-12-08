# Learning Log

## Week 1 - Planning

### Tuesday Part 1
**Goal**: Portfolio infrastructure and project roadmap

**Completed**: Created github org and added everything I need to begin my projects.

**Questions**: None

**Next**: Tuesday Part 2 - Start building Script #1

### Tuesday Part 2
**Goal**: Build Script #1 MVP

**Completed**:
- Installed Click framework
- Created CLI with --name and --type options
- Implemented directory structure creation
- Added file templates (README, .gitignore, requirements.txt)
- Script #1 is working

**What I learned**:
- Click is a lot easier to use than I thought
- I prefer pathlib to os.path

**Next**: Wednesday - Add git initialization and virtual environment setup

### Wednesday
**Goal**: Build Script #2 MVP

**Completed**:
- Script #2: Environment Validator (checks Python, Git, Docker, disk space)
- Added logging (--log flag)
- Added color using click.style()

**What I learned**:
- subprocess for system commands
- sys.version_info for checking Python version
- shutil.disk_usage for checking disk space

**Next**: Thursday - Log Analyzer

### Thursday
**Goal**: Start Script #3 - Log Analyzer

**Completed**:
- CLI structure and file reading
- Log level parsing and counting using regex
- ERROR/CRITICAL message extraction

**What I learned**:
- Beginning the figure out regex pattrens and capture groups
- Using .group(i) to pick out specific group
- Regex doesn't implicitly skip parts you don't mention (duh)

**Challanges**:
- Regex is a monumental pain in the neck to figure out
- Wrapping my head around groups.

**Next**: Grouping duplicate error messages and count occurrences

### Friday
**Goal**: Complete Steps 2-4 of Log Analyzer

**Completed**:
- Log level parsing with regex (continued from Thursday)
- Error message extraction  
- Group duplicate errors, count occurrences, track first seen timestamp

**What I learned**:
- Grouping data with dictionaries (message as key, list of timestamps as value)
- Lambda functions for sorting (key=lambda x: x[1]['count'])

**Challenges**:
- Got stuck on timestamp comparison logic - overcomplicated it initially
- Needed help understanding simpler grouping approach (collect all, then process)

**Energy**: Started late (13:00), 3/5

**Next**: JSON and CSV output

## Week 2

### Monday
**Goal**: Complete Steps 5-6 of Log Analyzer (file output)

**Completed**:
- Step 5: JSON output with json.dump()
- Step 6: CSV output with csv.DictWriter
- Full log analyzer tool finished

**What I learned**:
- json.dump() for writing dicts to files (indent parameter for readability)
- csv.DictWriter() expects flat dicts, not nested structures
- writerow() takes a dict with keys matching fieldnames
- pathlib.Path.stem for extracting filename without extension
- Transforming nested dict structure for CSV format

**Challenges**:
- CSV writerow() confusion - was passing list instead of dict
- Understanding that message key needed to become a dict value for CSV
- Filename generation (first idea was to slice but wasn't robust, needed .stem)

**Energy**: [3/5]

**Next**: Script #4 - Backup Automation (Days 8-9 in roadmap)