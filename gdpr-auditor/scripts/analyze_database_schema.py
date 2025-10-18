#!/usr/bin/env python3
"""
GDPR Database Schema Analyzer - Static File Analysis Tool

Analyzes database schema files (SQL DDL, migration scripts, ORM models, JSON schemas)
for personal data fields and sensitive information.

IMPORTANT - STATIC ANALYSIS ONLY:
This script analyzes static database schema files. It does NOT:
- Connect to running databases or database servers
- Execute queries or access live data
- Require database credentials or connection strings
- Monitor database activity or transactions
- Modify any database or data
- Access production or development database instances

Analyzes: .sql files (DDL/migrations), .json schema files, ORM model definitions
Purpose: Identify personal data fields in database schemas for GDPR compliance review
"""

import re
import json
import sys
from typing import List, Dict, Any

# Common personal data field patterns
PERSONAL_DATA_PATTERNS = {
    "identifiers": [
        r'\b(user_?id|customer_?id|person_?id|account_?id|uuid)\b',
        r'\b(username|login|handle)\b',
    ],
    "contact_info": [
        r'\b(email|e_?mail|mail_?address)\b',
        r'\b(phone|telephone|mobile|cell|fax)\b',
        r'\b(address|street|city|state|zip|postal|country)\b',
    ],
    "personal_identifiers": [
        r'\b(first_?name|last_?name|full_?name|given_?name|surname)\b',
        r'\b(ssn|social_?security|passport|license|id_?number)\b',
        r'\b(dob|date_?of_?birth|birth_?date|birthday)\b',
    ],
    "financial": [
        r'\b(credit_?card|card_?number|cvv|account_?number)\b',
        r'\b(bank|iban|swift|routing_?number)\b',
        r'\b(salary|income|payment)\b',
    ],
    "health": [
        r'\b(medical|health|diagnosis|prescription|treatment)\b',
        r'\b(blood_?type|allergy|condition)\b',
    ],
    "sensitive": [
        r'\b(race|ethnicity|religion|political|union)\b',
        r'\b(sexual|genetic|biometric)\b',
    ],
    "location": [
        r'\b(ip_?address|geo|location|latitude|longitude|gps)\b',
    ],
    "authentication": [
        r'\b(password|passwd|pwd|hash|salt|token|api_?key)\b',
        r'\b(secret|credential|auth)\b',
    ]
}

def analyze_field_name(field_name: str) -> List[Dict[str, str]]:
    """Analyze a field name for personal data patterns."""
    findings = []

    for category, patterns in PERSONAL_DATA_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, field_name, re.IGNORECASE):
                findings.append({
                    "category": category,
                    "field": field_name,
                    "pattern": pattern,
                    "gdpr_concern": get_gdpr_concern(category)
                })

    return findings

def get_gdpr_concern(category: str) -> str:
    """Get GDPR concern level for a data category."""
    concerns = {
        "identifiers": "Personal identifier - requires legal basis and protection",
        "contact_info": "Contact data - requires consent or legitimate interest",
        "personal_identifiers": "Personal identifier - high protection required",
        "financial": "Financial data - requires heightened security measures",
        "health": "Special category data (Article 9) - explicit consent required",
        "sensitive": "Special category data (Article 9) - explicit consent required",
        "location": "Location data - may be personal data requiring protection",
        "authentication": "Security credentials - must be encrypted and protected"
    }
    return concerns.get(category, "Personal data - requires appropriate protection")

def analyze_sql_schema(sql_content: str) -> Dict[str, Any]:
    """Analyze SQL schema for personal data."""
    findings = {
        "tables": [],
        "summary": {}
    }

    # Extract table definitions
    table_pattern = r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"\[]?(\w+)[`"\]]?\s*\((.*?)\);'
    tables = re.finditer(table_pattern, sql_content, re.IGNORECASE | re.DOTALL)

    for table_match in tables:
        table_name = table_match.group(1)
        table_def = table_match.group(2)

        # Extract column definitions
        column_pattern = r'[`"\[]?(\w+)[`"\]]?\s+(\w+)'
        columns = re.findall(column_pattern, table_def)

        table_findings = {
            "table_name": table_name,
            "fields": []
        }

        for col_name, col_type in columns:
            field_findings = analyze_field_name(col_name)
            if field_findings:
                table_findings["fields"].append({
                    "field_name": col_name,
                    "field_type": col_type,
                    "findings": field_findings
                })

        if table_findings["fields"]:
            findings["tables"].append(table_findings)

    # Generate summary
    total_tables = len(findings["tables"])
    total_personal_fields = sum(len(t["fields"]) for t in findings["tables"])

    findings["summary"] = {
        "total_tables_with_personal_data": total_tables,
        "total_personal_data_fields": total_personal_fields,
        "requires_dpia": total_personal_fields > 10 or any(
            any(f["category"] in ["health", "sensitive"] for f in field["findings"])
            for table in findings["tables"]
            for field in table["fields"]
        )
    }

    return findings

def analyze_json_schema(json_content: str) -> Dict[str, Any]:
    """Analyze JSON schema or model definitions."""
    findings = {"models": [], "summary": {}}

    try:
        # Try to parse as JSON
        data = json.loads(json_content)

        # Handle different schema formats
        if isinstance(data, dict):
            for model_name, model_def in data.items():
                if isinstance(model_def, dict) and "properties" in model_def:
                    # JSON Schema format
                    model_findings = {"model_name": model_name, "fields": []}

                    for field_name, field_def in model_def.get("properties", {}).items():
                        field_findings = analyze_field_name(field_name)
                        if field_findings:
                            model_findings["fields"].append({
                                "field_name": field_name,
                                "field_type": field_def.get("type", "unknown"),
                                "findings": field_findings
                            })

                    if model_findings["fields"]:
                        findings["models"].append(model_findings)

        # Generate summary
        total_models = len(findings["models"])
        total_personal_fields = sum(len(m["fields"]) for m in findings["models"])

        findings["summary"] = {
            "total_models_with_personal_data": total_models,
            "total_personal_data_fields": total_personal_fields
        }

    except json.JSONDecodeError:
        findings["error"] = "Invalid JSON format"

    return findings

def main():
    """Main entry point for the analyzer."""
    if len(sys.argv) < 2:
        print("Usage: python analyze_database_schema.py <schema_file>")
        print("Supports SQL files (.sql) and JSON schema files (.json)")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if file_path.endswith('.sql'):
            findings = analyze_sql_schema(content)
        elif file_path.endswith('.json'):
            findings = analyze_json_schema(content)
        else:
            print("Unsupported file format. Use .sql or .json files.")
            sys.exit(1)

        print(json.dumps(findings, indent=2))

        # Summary
        print(f"\n{'='*60}")
        print("GDPR Schema Analysis Summary")
        print(f"{'='*60}")
        for key, value in findings.get("summary", {}).items():
            print(f"{key}: {value}")

    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
