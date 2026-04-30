#!/usr/bin/env python3
"""
Generate comprehensive HTML report from Jupyter notebooks
================================================

This script orchestrates the complete analysis pipeline:
1. Executes all three analysis notebooks in sequence
2. Consolidates outputs into a single HTML report
3. Applies styling and branding
4. Exports to docs/index.html

Usage:
    python Z_generate_report.py

Requirements:
    - nbconvert: jupyter nbconvert
    - All notebooks in the code/ directory
    - Processed data in data/ directory
"""

import os
import sys
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime


class ReportGenerator:
    """Generate consolidated report from notebooks"""
    
    def __init__(self, project_root=None):
        """Initialize paths and configuration"""
        if project_root is None:
            project_root = Path(__file__).parent
        
        self.project_root = Path(project_root)
        self.code_dir = self.project_root / 'code'
        self.data_dir = self.project_root / 'data'
        self.docs_dir = self.project_root / 'docs'
        
        # Ensure directories exist
        self.docs_dir.mkdir(exist_ok=True)
        
        # Define notebooks in execution order
        self.notebooks = [
            '01_data_cleaning.ipynb',
            '02_exploration.ipynb',
            '03_analysis.ipynb'
        ]
        
        self.output_html = self.docs_dir / 'index.html'
        
    def check_dependencies(self):
        """Verify all required tools and files exist"""
        print("📋 Checking dependencies...")
        
        # Check for nbconvert
        try:
            subprocess.run(['jupyter', 'nbconvert', '--version'], 
                          capture_output=True, check=True)
            print("  ✓ jupyter nbconvert found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("  ✗ jupyter nbconvert not found")
            print("    Install with: pip install nbconvert")
            return False
        
        # Check for notebooks
        for nb in self.notebooks:
            nb_path = self.code_dir / nb
            if not nb_path.exists():
                print(f"  ✗ {nb} not found at {nb_path}")
                return False
            print(f"  ✓ {nb} found")
        
        print("  ✓ All dependencies available\\n")
        return True
    
    def execute_notebooks(self):
        """Execute all notebooks to generate outputs"""
        print("⚙️  Executing notebooks...\\n")
        
        for idx, nb_name in enumerate(self.notebooks, 1):
            nb_path = self.code_dir / nb_name
            print(f"[{idx}/{len(self.notebooks)}] Executing {nb_name}...")
            
            try:
                # Execute notebook using nbconvert
                subprocess.run([
                    'jupyter', 'nbconvert',
                    '--to', 'notebook',
                    '--execute',
                    '--inplace',
                    str(nb_path)
                ], capture_output=True, timeout=300)
                print(f"     ✓ {nb_name} executed successfully\\n")
            except subprocess.TimeoutExpired:
                print(f"     ✗ {nb_name} execution timeout\\n")
                return False
            except Exception as e:
                print(f"     ✗ Error executing {nb_name}: {e}\\n")
                return False
        
        return True
    
    def convert_notebooks_to_html(self):
        """Convert each notebook to HTML"""
        print("🔄 Converting notebooks to HTML...\\n")
        
        html_outputs = []
        
        for nb_name in self.notebooks:
            nb_path = self.code_dir / nb_name
            html_path = self.code_dir / nb_name.replace('.ipynb', '.html')
            
            print(f"Converting {nb_name}...")
            
            try:
                subprocess.run([
                    'jupyter', 'nbconvert',
                    '--to', 'html',
                    '--template', 'lab',  # Use lab template for better styling
                    str(nb_path),
                    '--output', str(html_path)
                ], capture_output=True, check=True)
                
                html_outputs.append(html_path)
                print(f"  ✓ Created {html_path.name}\\n")
            except Exception as e:
                print(f"  ✗ Error converting {nb_name}: {e}\\n")
                return None
        
        return html_outputs
    
    def extract_html_content(self, html_path):
        """Extract body content from HTML file"""
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract content between body tags
            match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
            if match:
                return match.group(1)
            return content
        except Exception as e:
            print(f"Error reading {html_path}: {e}")
            return ""
    
    def create_consolidated_report(self, html_outputs):
        \"\"\"Merge all notebook HTML into single report\"\"\"
        print("📝 Creating consolidated report...\\n")
        
        # Build HTML structure
        html_content = f\"\"\"<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Afghanistan Conflict Spillover Analysis Report</title>
    <script src=\"https://cdn.plot.ly/plotly-2.35.2.min.js\"></script>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3 {{ color: #1a1a1a; }}
        h1 {{
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }}
        .notebook-section {{
            margin: 30px 0;
            padding: 20px;
            background: #f9f9f9;
            border-left: 4px solid #007bff;
        }}
        .metadata {{
            font-size: 0.9em;
            color: #666;
            margin: 10px 0;
        }}
        .toc {{
            background: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .toc ul {{ margin: 10px 0; }}
        .toc li {{ margin: 5px 0; }}
        .toc a {{ color: #007bff; text-decoration: none; }}
        .toc a:hover {{ text-decoration: underline; }}
        code {{
            background: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        .cell-output {{
            background: white;
            border: 1px solid #ddd;
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
            overflow-x: auto;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }}
        table th, table td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        table th {{
            background: #007bff;
            color: white;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 0.9em;
            color: #666;
        }}
    </style>
</head>
<body>
<div class=\"container\">
    <h1>🔍 Afghanistan Conflict Spillover Analysis</h1>
    <p><strong>Comprehensive Report</strong> | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class=\"toc\">
        <h3>📚 Report Contents:</h3>
        <ul>
            <li><a href=\"#section-1\">1. Data Cleaning & Preprocessing</a></li>
            <li><a href=\"#section-2\">2. Exploratory Data Analysis</a></li>
            <li><a href=\"#section-3\">3. Statistical Analysis & Findings</a></li>
        </ul>
    </div>
    
    <hr>
\"\"\"
        
        # Add notebook content
        for idx, html_path in enumerate(html_outputs, 1):
            section_id = f\"section-{idx}\"
            nb_name = self.notebooks[idx - 1]
            
            print(f"  Including content from {nb_name}...")
            
            section_title = self._get_notebook_title(nb_name)
            content = self.extract_html_content(html_path)
            
            html_content += f\"\"\"
    <div class=\"notebook-section\" id=\"{section_id}\">
        <h2>Section {idx}: {section_title}</h2>
        <div class=\"metadata\">📄 From: <code>{nb_name}</code></div>
        {content}
    </div>
    <hr>
\"\"\"
        
        # Add footer
        html_content += f\"\"\"
    <div class=\"footer\">
        <p><strong>Report Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Source:</strong> ACLED Political Violence Data (2020-2021)</p>
        <p><strong>Analysis:</strong> Lagged regression examining spillover of Afghanistan conflict to neighboring countries</p>
        <p><em>This report was automatically generated from Jupyter notebooks. For details, see the individual notebook files in the <code>code/</code> directory.</em></p>
    </div>
</div>
</body>
</html>
\"\"\"
        
        return html_content
    
    def _get_notebook_title(self, nb_name):
        \"\"\"Extract title from notebook name\"\"\"
        titles = {
            '01_data_cleaning.ipynb': 'Data Cleaning & Preprocessing',
            '02_exploration.ipynb': 'Exploratory Data Analysis',
            '03_analysis.ipynb': 'Statistical Analysis & Visualization'
        }
        return titles.get(nb_name, nb_name)
    
    def save_report(self, html_content):
        \"\"\"Save HTML report to file\"\"\"
        try:
            with open(self.output_html, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f\"\\n✅ Report saved to: {self.output_html}\")
            return True
        except Exception as e:
            print(f\"❌ Error saving report: {e}\")
            return False
    
    def generate(self):
        \"\"\"Execute full report generation pipeline\"\"\"
        print(\"=\"*70)
        print(\"🚀 AFGHANISTAN SPILLOVER ANALYSIS - REPORT GENERATOR\")
        print(\"=\"*70 + \"\\n\")
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Execute notebooks
        if not self.execute_notebooks():
            print(\"⚠️  Warning: Some notebooks had issues, continuing anyway...\\n\")
        
        # Convert to HTML
        html_outputs = self.convert_notebooks_to_html()
        if not html_outputs:
            print(\"❌ Failed to convert notebooks to HTML\")
            return False
        
        # Create consolidated report
        html_content = self.create_consolidated_report(html_outputs)
        
        # Save report
        if not self.save_report(html_content):
            return False
        
        print(\"\\n\" + \"=\"*70)
        print(\"✨ Report generation completed successfully!\")
        print(\"=\"*70)
        print(f\"\\n📂 Open report at: file://{self.output_html.absolute()}\")
        
        return True


def main():
    \"\"\"Main entry point\"\"\"
    try:
        # Determine project root (parent of this script)
        script_dir = Path(__file__).parent
        generator = ReportGenerator(project_root=script_dir)
        
        # Generate report
        success = generator.generate()
        
        sys.exit(0 if success else 1)
    
    except Exception as e:
        print(f\"\\n❌ Fatal error: {e}\")
        sys.exit(1)


if __name__ == '__main__':
    main()
