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
