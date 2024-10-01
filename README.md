# SQLThat - SQL Injection Testing Tool

SQLThat is a Python-based tool designed for testing web applications against SQL injection vulnerabilities. Use this tool to identify potential weaknesses in your web applications and improve their security posture. **Use at your own risk!**

## Features

- Comprehensive list of SQL injection payloads
- Random User-Agent generation to avoid detection
- Evasion techniques for payloads
- Multithreaded attack functionality for increased efficiency
- Logging of potential vulnerabilities found

## Requirements

To run this tool, you need Python 3.x and the following packages:

- `requests`
- `fake-useragent`

You can install the required packages by running:

```bash
pip install -r requirements.txt
```

# Usage
Clone this repository
```bash 
git clone https://github.com/SleepTheGod/SQLThat
```
# Install the required packages
```bash
pip install -r requirements.txt
```
# Run the main script
```bash
python main.py
```
Follow the prompts to enter the target URL and parameters for the attack.

# Example
Enter target URL (without parameters): http://example.com/vulnerable.php
Enter vulnerable parameter: id
Enter max number of concurrent threads (default 10): 10

# Logging
The tool logs the results of each SQL injection attempt in a file named sql_injection_report.log. Check this file for details on potential vulnerabilities found during the testing.

# Disclaimer
This tool is intended for educational purposes only. Do not use it against any system without explicit permission. The author is not responsible for any misuse or damage caused by this tool.
