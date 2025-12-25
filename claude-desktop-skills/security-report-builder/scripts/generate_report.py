#!/usr/bin/env python3
"""
Main CLI for generating security reports in multiple formats.
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from parsers.scan_result_parser import ScanResultParser
from parsers.framework_mapper import FrameworkMapper
from analyzers.context_analyzer import ContextAnalyzer
from analyzers.risk_calculator import RiskCalculator
from analyzers.false_positive_filter import FalsePositiveFilter
from generators.html_generator import HTMLReportGenerator

# Optional generators (may need system dependencies)
try:
    from generators.pdf_generator import PDFReportGenerator
except ImportError as e:
    logger.warning(f"PDF generator unavailable: {e}")
    PDFReportGenerator = None

try:
    from generators.docx_generator import DOCXReportGenerator
except ImportError as e:
    logger.warning(f"DOCX generator unavailable: {e}")
    DOCXReportGenerator = None

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReportOrchestrator:
    """Orchestrate the complete report generation pipeline."""

    def __init__(self, config_dir: Path):
        """
        Initialize report orchestrator.

        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = config_dir

        # Load configurations
        self.severity_rules = self._load_json(config_dir / 'severity_rules.json')
        self.report_config = self._load_json(config_dir / 'report_config.json')
        self.branding = self._load_json(config_dir / 'branding.json')

        # Initialize components
        self.parser = ScanResultParser()
        self.framework_mapper = FrameworkMapper()
        self.context_analyzer = ContextAnalyzer(config_dir / 'severity_rules.json')
        self.risk_calculator = RiskCalculator(
            self.severity_rules.get('severity_levels', {})
        )
        self.fp_filter = FalsePositiveFilter()

        # Generators
        self.html_generator = HTMLReportGenerator()
        self.pdf_generator = PDFReportGenerator() if PDFReportGenerator else None
        self.docx_generator = DOCXReportGenerator() if DOCXReportGenerator else None

        # Try to load framework mappings
        references_dir = config_dir.parent / 'references'
        mappings_file = references_dir / 'framework_mappings.json'
        if mappings_file.exists():
            self.framework_mapper.load_mappings(mappings_file)
        else:
            # Try plugin-security-checker references
            alt_mappings = Path('../plugin-security-checker/references/threat_mappings.json')
            if alt_mappings.exists():
                self.framework_mapper.load_mappings(alt_mappings)

    def _load_json(self, path: Path) -> Dict[str, Any]:
        """Load JSON file with error handling."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load {path}: {e}")
            return {}

    def generate_reports(self,
                        input_path: Path,
                        output_dir: Path,
                        formats: List[str],
                        min_severity: str = 'INFO',
                        exclude_false_positives: bool = True,
                        template: str = 'technical') -> Dict[str, Path]:
        """
        Generate security reports in specified formats.

        Args:
            input_path: Path to scan results (file or directory)
            output_dir: Output directory for reports
            formats: List of formats ('html', 'pdf', 'docx')
            min_severity: Minimum severity to include
            exclude_false_positives: Whether to filter false positives
            template: Report template to use

        Returns:
            Dictionary mapping format to output file path
        """
        logger.info(f"Starting report generation pipeline")
        logger.info(f"Input: {input_path}")
        logger.info(f"Output: {output_dir}")
        logger.info(f"Formats: {', '.join(formats)}")

        # Step 1: Parse scan results
        logger.info("Step 1: Parsing scan results...")
        if input_path.is_file():
            self.parser.parse_file(input_path)
        elif input_path.is_dir():
            self.parser.parse_directory(input_path)
        else:
            raise ValueError(f"Invalid input path: {input_path}")

        statistics = self.parser.get_statistics()
        logger.info(f"Parsed {statistics['total_plugins']} plugins with {statistics['total_findings']} findings")

        # Step 2: Get all findings
        logger.info("Step 2: Extracting findings...")
        findings = self.parser.get_all_findings()

        # Step 3: Enrich with framework mappings
        logger.info("Step 3: Mapping to security frameworks...")
        enriched_findings = [self.framework_mapper.map_finding(f) for f in findings]

        # Step 4: Apply context-aware analysis
        logger.info("Step 4: Applying context-aware analysis...")
        analysis_result = self.context_analyzer.analyze_batch(enriched_findings)
        analyzed_findings = analysis_result['analyzed_findings']
        analysis_stats = analysis_result['statistics']

        logger.info(f"Adjusted {analysis_stats['adjusted_count']} findings")
        logger.info(f"False positive rate: {analysis_stats['false_positive_rate']}%")

        # Step 5: Filter findings
        logger.info("Step 5: Filtering findings...")
        if exclude_false_positives:
            filtered_findings = self.fp_filter.filter_findings(
                analyzed_findings,
                exclude_info=(min_severity != 'INFO'),
                exclude_low=(min_severity in ['MEDIUM', 'HIGH', 'CRITICAL']),
                min_confidence=0.7
            )
            filter_stats = self.fp_filter.get_statistics()
            logger.info(f"Filtered {filter_stats['filtered_out']} findings ({filter_stats['filter_rate']}%)")
        else:
            filtered_findings = analyzed_findings
            logger.info("False positive filtering disabled")

        # Step 6: Calculate risk scores
        logger.info("Step 6: Calculating risk scores...")

        # Group findings by plugin
        plugins = {}
        for finding in filtered_findings:
            plugin = finding.get('plugin_name', 'unknown')
            if plugin not in plugins:
                plugins[plugin] = []
            plugins[plugin].append(finding)

        # Calculate per-plugin scores
        plugin_scores = []
        for plugin_name, plugin_findings in plugins.items():
            score = self.risk_calculator.calculate_plugin_score(plugin_findings)
            score['plugin_name'] = plugin_name
            plugin_scores.append(score)

        # Calculate overall risk
        overall_risk = self.risk_calculator.calculate_overall_risk(plugin_scores)
        logger.info(f"Overall risk score: {overall_risk['overall_risk_score']} ({overall_risk['overall_risk_level']})")

        # Step 7: Generate framework summary
        logger.info("Step 7: Generating framework summary...")
        framework_summary = self.framework_mapper.generate_framework_summary(filtered_findings)

        # Step 8: Generate reports
        logger.info("Step 8: Generating reports...")
        output_dir.mkdir(parents=True, exist_ok=True)

        generated_files = {}

        # Prepare data for generators
        report_data = {
            'findings': filtered_findings,
            'statistics': {
                'total_plugins': statistics['total_plugins'],
                'total_findings': len(filtered_findings),
                'by_severity': {},
                'by_category': {}
            },
            'framework_summary': framework_summary,
            'plugin_scores': sorted(plugin_scores, key=lambda x: x['risk_score'], reverse=True),
            'overall_risk': overall_risk,
            'config': self.report_config,
            'branding': self.branding
        }

        # Recalculate severity distribution for filtered findings
        for finding in filtered_findings:
            sev = finding.get('severity', 'UNKNOWN')
            report_data['statistics']['by_severity'][sev] = \
                report_data['statistics']['by_severity'].get(sev, 0) + 1

            cat = finding.get('category', 'UNKNOWN')
            report_data['statistics']['by_category'][cat] = \
                report_data['statistics']['by_category'].get(cat, 0) + 1

        # Generate HTML
        if 'html' in formats:
            logger.info("Generating HTML report...")
            html_path = output_dir / 'security_report.html'
            self.html_generator.generate_report(
                **report_data,
                output_path=html_path
            )
            generated_files['html'] = html_path

        # Generate PDF
        if 'pdf' in formats:
            if self.pdf_generator:
                logger.info("Generating PDF report...")
                pdf_path = output_dir / 'security_report.pdf'
                self.pdf_generator.generate_report(
                    **report_data,
                    output_path=pdf_path
                )
                generated_files['pdf'] = pdf_path
            else:
                logger.error("PDF generator not available. Install weasyprint: pip install weasyprint")

        # Generate DOCX
        if 'docx' in formats:
            if self.docx_generator:
                logger.info("Generating DOCX report...")
                docx_path = output_dir / 'security_report.docx'
                self.docx_generator.generate_report(
                    **report_data,
                    output_path=docx_path
                )
                generated_files['docx'] = docx_path
            else:
                logger.error("DOCX generator not available. Install python-docx: pip install python-docx")

        logger.info(f"Report generation complete!")
        return generated_files


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate professional security reports from scan results',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all formats with default settings
  %(prog)s --input results/ --output reports/ --formats html,pdf,docx

  # Generate HTML report with minimum severity HIGH
  %(prog)s --input scan.json --output report.html --format html --min-severity HIGH

  # Generate PDF report without false positive filtering
  %(prog)s --input results/ --output report.pdf --format pdf --no-filter

  # Generate DOCX with custom branding
  %(prog)s --input results/ --output report.docx --format docx --branding custom.json
        """
    )

    parser.add_argument('--input', '-i', required=True,
                       help='Input scan results (JSON file or directory)')
    parser.add_argument('--output', '-o', required=True,
                       help='Output directory or file path')
    parser.add_argument('--formats', '-f', default='html,pdf,docx',
                       help='Output formats (comma-separated: html,pdf,docx)')
    parser.add_argument('--template', '-t', default='technical',
                       choices=['executive', 'technical', 'compliance'],
                       help='Report template to use')
    parser.add_argument('--min-severity', '-s', default='INFO',
                       choices=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'],
                       help='Minimum severity level to include')
    parser.add_argument('--no-filter', action='store_true',
                       help='Disable false positive filtering')
    parser.add_argument('--config-dir', default=None,
                       help='Configuration directory (default: ../config)')
    parser.add_argument('--branding', help='Custom branding JSON file')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Determine config directory
    if args.config_dir:
        config_dir = Path(args.config_dir)
    else:
        config_dir = Path(__file__).parent.parent / 'config'

    if not config_dir.exists():
        logger.error(f"Configuration directory not found: {config_dir}")
        return 1

    # Parse input/output paths
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input path not found: {input_path}")
        return 1

    # Determine output directory
    output_arg = Path(args.output)
    if output_arg.suffix in ['.html', '.pdf', '.docx']:
        # Single file output
        output_dir = output_arg.parent
        # Override format based on file extension
        formats = [output_arg.suffix[1:]]
    else:
        # Directory output
        output_dir = output_arg
        formats = [f.strip() for f in args.formats.split(',')]

    # Validate formats
    valid_formats = {'html', 'pdf', 'docx'}
    formats = [f for f in formats if f in valid_formats]

    if not formats:
        logger.error("No valid output formats specified")
        return 1

    # Initialize orchestrator
    orchestrator = ReportOrchestrator(config_dir)

    # Load custom branding if provided
    if args.branding:
        with open(args.branding, 'r') as f:
            orchestrator.branding = json.load(f)

    # Generate reports
    try:
        generated = orchestrator.generate_reports(
            input_path=input_path,
            output_dir=output_dir,
            formats=formats,
            min_severity=args.min_severity,
            exclude_false_positives=not args.no_filter,
            template=args.template
        )

        # Print summary
        print("\n" + "="*60)
        print("✓ Report Generation Complete")
        print("="*60)
        print(f"\nGenerated {len(generated)} report(s):")
        for format_type, file_path in generated.items():
            if file_path.exists():
                size = file_path.stat().st_size / 1024
                print(f"  • {format_type.upper()}: {file_path} ({size:.1f} KB)")
            else:
                print(f"  • {format_type.upper()}: {file_path} (FAILED)")
        print()

        return 0

    except Exception as e:
        logger.exception(f"Error generating reports: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
