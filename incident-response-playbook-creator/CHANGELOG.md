# Changelog

All notable changes to the Incident Response Playbook Creator plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2025-10-21

### Added

#### New Scenarios (7 Total)
Expanded from 3 to 11 comprehensive incident scenarios:

1. **AI/ML Security Incident** (`ai_ml_attack`)
   - Adversarial attacks on machine learning models
   - Model poisoning, data poisoning, and inference attacks
   - Based on OWASP Top 10 for LLMs v2025

2. **Supply Chain Attack** (`supply_chain_attack`)
   - Compromise through third-party software or services
   - SolarWinds-style attacks and dependency vulnerabilities
   - Based on NIST SP 800-161r1 (Cybersecurity Supply Chain Risk Management)

3. **Container/Kubernetes Security Incident** (`container_kubernetes_security`)
   - Container escape, cluster compromise, and orchestration attacks
   - Based on NIST SP 800-190 (Application Container Security Guide)
   - Kubernetes-specific security controls and detection

4. **IoT/OT Security Incident** (`iot_ot_security`)
   - Industrial Control Systems (ICS) and SCADA security incidents
   - Based on NIST SP 800-82r3 (Guide to Operational Technology Security)
   - Safety-critical considerations for operational technology

5. **Cloud Security Breach** (`cloud_security_breach`)
   - S3 bucket exposure, IAM compromise, cloud misconfigurations
   - Based on AWS Security Incident Response Guide
   - Multi-cloud considerations (AWS, Azure, GCP)

6. **API Security Incident** (`api_security_incident`)
   - API vulnerabilities, authentication bypass, and data exposure
   - Based on OWASP API Security Top 10 and NIST SP 800-218 (Secure SDLC)
   - REST, GraphQL, and microservices security

7. **DDoS Attack** (`ddos_attack`)
   - Distributed Denial of Service attacks
   - Based on CISA Understanding and Responding to DDoS Attacks guide
   - Application-layer and network-layer attack mitigation

#### Enhanced Original Scenarios
Significantly expanded and improved the original 3 scenarios:

- **Ransomware Attack** (`ransomware`)
  - Added double extortion scenarios
  - Enhanced detection indicators
  - Expanded recovery procedures

- **Data Breach / Exfiltration** (`data_breach`)
  - More comprehensive GDPR Article 33/34 guidance
  - Enhanced HIPAA breach notification procedures
  - Additional data exfiltration techniques and detection

- **Phishing / Business Email Compromise** (`phishing`)
  - Expanded BEC attack vectors
  - Enhanced CEO fraud and wire transfer scam procedures
  - Improved credential harvesting detection

#### New Authoritative Sources
Added comprehensive coverage from additional NIST publications:

- **NIST SP 800-161r1** - Cybersecurity Supply Chain Risk Management (Rev 1 Update 1, May 2024)
- **NIST SP 800-190** - Application Container Security Guide (September 2017)
- **NIST SP 800-82r3** - Guide to Operational Technology Security (Revision 3, September 2023)
- **NIST SP 800-218** - Secure Software Development Framework (Version 1.1, February 2022)
- **AWS Security Incident Response Guide** (2024)
- **OWASP Top 10 for LLMs** (Version 2025, January 2025)

### Changed

#### Default Scenarios File
- Changed default from `incident_scenarios_simplified.json` to `incident_scenarios_v2.json`
- Updated in `scripts/browse_scenarios.py` (line 457)
- Updated in `scripts/generate_playbook_markdown.py` (line 535)

#### Documentation Updates
- **plugin.json**: Version bumped to 2.0.0, updated description to mention 11 scenarios
- **README.md**: Complete rewrite of scenario section with detailed descriptions
- **SKILL.md**: Expanded trigger phrases for all 11 scenarios
- All version references updated from 1.0.0 to 2.0.0

#### Keywords
Added new keywords to `plugin.json`:
- `supply-chain`
- `container`
- `kubernetes`
- `iot`
- `ot`
- `cloud`
- `api`
- `insider-threat`
- `ddos`

### Improved

#### Data Quality
- All scenarios now include comprehensive NIST CSF 2.0 mappings
- Enhanced detection indicators (technical and behavioral)
- More detailed response procedures with specific timeframes
- Expanded communication requirements
- Improved compliance guidance (GDPR/HIPAA where applicable)

#### Reference Documentation
- Enhanced source citations
- Added publication dates for all references
- Included version information for all NIST publications
- Comprehensive reference file documentation

### Fixed
- Script version strings updated throughout
- Playbook template footer updated to reflect v2.0.0
- Help text updated to reference new default scenarios file

---

## [1.0.0] - 2025-10-19

### Added
- Initial release of Incident Response Playbook Creator
- 3 core incident scenarios:
  - Ransomware Attack
  - Data Breach / Exfiltration
  - Phishing / Business Email Compromise
- NIST SP 800-61r3 alignment (April 2025 revision)
- NIST Cybersecurity Framework 2.0 integration
- GDPR Article 33/34 compliance guidance
- HIPAA Breach Notification Rule guidance
- Professional Markdown playbook generation
- Organization customization (name, industry, contacts)
- Python scripts for scenario browsing and playbook generation
- Comprehensive documentation (README.md, SKILL.md)
- MIT License

### Data Sources (v1.0.0)
- NIST SP 800-61r3 - Computer Security Incident Handling Guide (April 2025)
- NIST Cybersecurity Framework 2.0 (February 2024)
- CISA Federal Incident Response Playbooks (August 2024)
- GDPR (EU Regulation 2016/679)
- HIPAA Breach Notification Rule (45 CFR 164.400-414)

---

## Release Notes

### v2.0.0 Highlights

This major release represents a **266% increase** in scenario coverage (from 3 to 11 scenarios) and incorporates **175% more authoritative sources** (from 4 to 11 NIST/CISA/OWASP publications).

**What's New:**
- 7 new incident scenarios covering modern attack vectors (AI/ML, supply chain, containers)
- Critical infrastructure scenarios (IoT/OT, cloud, API security)
- Insider threat and DDoS attack scenarios
- Comprehensive NIST publication coverage (800-161r1, 800-190, 800-82r3, 800-218)
- Enhanced original scenarios with more detailed procedures
- All scenarios updated to latest 2024-2025 guidance

**Migration from v1.0.0:**
- Default scenarios file changed from `incident_scenarios_simplified.json` to `incident_scenarios_v2.json`
- All v1.0.0 scenario IDs remain compatible (`ransomware`, `data_breach`, `phishing`)
- No breaking changes to script interfaces or command-line arguments
- Existing playbooks remain valid; regeneration recommended to benefit from enhancements

**Testing:**
- All 11 scenarios validated against authoritative sources
- JSON syntax verified
- Script functionality tested across all scenarios
- Playbook generation confirmed for each scenario type

---

## Future Roadmap

Planned for future releases:
- **v2.1.0**: Multi-format export (Word .docx, PDF)
- **v2.2.0**: Excel contact roster generation
- **v2.3.0**: Tabletop exercise scenario generation
- **v3.0.0**: Custom scenario creation framework
- **v3.1.0**: Integration with ticketing systems (Jira, ServiceNow)

---

**Note**: For complete documentation, see [README.md](README.md) and [SKILL.md](SKILL.md)
