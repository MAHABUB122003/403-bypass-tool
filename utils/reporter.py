#!/usr/bin/env python3
"""
Report generation utilities
"""

import json
import datetime
import os
from colorama import Fore, Style

class Reporter:
    def __init__(self):
        self.results = []
        self.start_time = datetime.datetime.now()
        
    def add_result(self, result):
        self.results.append(result)
        
    def generate_report(self, format='json', output_file=None):
        """Generate report in specified format"""
        if format == 'json':
            content = self.generate_json()
        elif format == 'html':
            content = self.generate_html()
        elif format == 'csv':
            content = self.generate_csv()
        else:
            content = self.generate_text()
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(content)
            print(f"{Fore.GREEN}[+] Report saved to: {output_file}")
        
        return content
    
    def generate_json(self):
        """Generate JSON report"""
        report = {
            'timestamp': self.start_time.isoformat(),
            'duration': str(datetime.datetime.now() - self.start_time),
            'total_bypasses': len(self.results),
            'results': self.results
        }
        return json.dumps(report, indent=2)
    
    def generate_text(self):
        """Generate text report"""
        report = []
        report.append("=" * 70)
        report.append("403 BYPASS REPORT")
        report.append("=" * 70)
        report.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Duration: {datetime.datetime.now() - self.start_time}")
        report.append(f"Total Bypasses Found: {len(self.results)}")
        report.append("=" * 70)
        report.append("")
        
        if self.results:
            # Group by technique type
            techniques = {}
            for result in self.results:
                tech = result.get('technique', 'Unknown').split(':')[0]
                if tech not in techniques:
                    techniques[tech] = []
                techniques[tech].append(result)
            
            for tech, bypasses in techniques.items():
                report.append(f"\n{tech.upper()} BYPASSES ({len(bypasses)})")
                report.append("-" * 70)
                for i, bypass in enumerate(bypasses, 1):
                    report.append(f"{i}. {bypass.get('technique', 'Unknown')}")
                    report.append(f"   URL: {bypass.get('url', 'N/A')}")
                    report.append(f"   Status: {bypass.get('status_code', 'N/A')}")
                    report.append(f"   Method: {bypass.get('method', 'GET')}")
                    report.append(f"   Content Length: {bypass.get('content_length', 'N/A')}")
                    report.append("")
        else:
            report.append("No bypasses found!")
        
        report.append("=" * 70)
        return "\n".join(report)
    
    def generate_html(self):
        """Generate HTML report"""
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html lang='en'>")
        html.append("<head>")
        html.append("<meta charset='UTF-8'>")
        html.append("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html.append("<title>403 Bypass Report</title>")
        html.append("<style>")
        html.append("""
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 20px;
                background: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
            .summary {
                background: #e8f5e9;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
            .summary span { font-weight: bold; color: #2e7d32; }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            th {
                background: #4CAF50;
                color: white;
                position: sticky;
                top: 0;
            }
            tr:nth-child(even) { background: #f9f9f9; }
            tr:hover { background: #f1f1f1; }
            .status-success { color: #4CAF50; font-weight: bold; }
            .status-partial { color: #FF9800; font-weight: bold; }
            .status-error { color: #f44336; font-weight: bold; }
            .badge {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
            }
            .badge-success { background: #4CAF50; color: white; }
            .badge-partial { background: #FF9800; color: white; }
            .badge-error { background: #f44336; color: white; }
            @media print {
                .no-print { display: none; }
                body { background: white; }
                .container { box-shadow: none; }
            }
        """)
        html.append("</style>")
        html.append("</head>")
        html.append("<body>")
        html.append("<div class='container'>")
        html.append("<h1>🔍 403 Bypass Report</h1>")
        
        # Summary
        html.append("<div class='summary'>")
        html.append(f"<p><strong>Generated:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
        html.append(f"<p><strong>Duration:</strong> {datetime.datetime.now() - self.start_time}</p>")
        html.append(f"<p><strong>Total Bypasses Found:</strong> <span>{len(self.results)}</span></p>")
        html.append("</div>")
        
        if self.results:
            html.append("<table>")
            html.append("<thead>")
            html.append("<tr>")
            html.append("<th>#</th>")
            html.append("<th>Technique</th>")
            html.append("<th>URL</th>")
            html.append("<th>Status</th>")
            html.append("<th>Method</th>")
            html.append("<th>Length</th>")
            html.append("</tr>")
            html.append("</thead>")
            html.append("<tbody>")
            
            for i, result in enumerate(self.results, 1):
                status = result.get('status_code', 'N/A')
                status_class = 'status-success' if status in [200, 201, 202] else 'status-partial'
                badge_class = 'badge-success' if status in [200, 201, 202] else 'badge-partial'
                
                html.append("<tr>")
                html.append(f"<td>{i}</td>")
                html.append(f"<td>{result.get('technique', 'Unknown')}</td>")
                html.append(f"<td style='word-break: break-all;'>{result.get('url', 'N/A')}</td>")
                html.append(f"<td><span class='{status_class}'>{status}</span></td>")
                html.append(f"<td>{result.get('method', 'GET')}</td>")
                html.append(f"<td>{result.get('content_length', 'N/A')}</td>")
                html.append("</tr>")
            
            html.append("</tbody>")
            html.append("</table>")
        else:
            html.append("<p style='color: #f44336; font-size: 18px;'>❌ No bypasses found!</p>")
        
        html.append("</div>")
        html.append("</body>")
        html.append("</html>")
        return "\n".join(html)
    
    def generate_csv(self):
        """Generate CSV report"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['#', 'Technique', 'URL', 'Status', 'Method', 'Content Length', 'Timestamp'])
        
        for i, result in enumerate(self.results, 1):
            writer.writerow([
                i,
                result.get('technique', 'Unknown'),
                result.get('url', 'N/A'),
                result.get('status_code', 'N/A'),
                result.get('method', 'GET'),
                result.get('content_length', 'N/A'),
                datetime.datetime.now().isoformat()
            ])
        
        return output.getvalue()
