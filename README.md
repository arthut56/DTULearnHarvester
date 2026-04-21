# DTULearnHarvester

A tool for downloading course materials from DTU Learn.

## Installation
```bash
git clone https://github.com/username/DTULearnHarvester
cd DTULearnHarvester
pip install -r requirements.txt
```
Create a .env file at the root of the project with your user credentials, e.g:
```
CREDENTIALS_EMAIL=studentnumber@dtu.dk
CREDENTIALS_PASSWORD=password
```

## Usage
```bash
python main.py course_no [format_style]
```

### Format options
| Option    | Description                  |
|-----------|------------------------------|
| `default` | Keeps original filename      |
| `lower`   | Lowercases the filename      |
| `snake`   | Converts to snake_case       |
| `kebab`   | Converts to kebab-case       |

### Example
```bash
python main.py 12345 snake
```