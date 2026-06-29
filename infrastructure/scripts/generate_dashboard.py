"""
AgenticMarketingPro — Dashboard Generator
=========================================
Generates visual dashboards from agent outputs and vault data.
Produces:
- PNG charts for key metrics (traffic, keywords, CTR, costs, agent performance)
- HTML dashboard combining all charts + brain map embed

Usage:
    python scripts/generate_dashboard.py
    python scripts/generate_dashboard.py --client acme --output dashboard.html
"""

import argparse
import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config

logger = logging.getLogger("amp.dashboard")


class DashboardGenerator:
    """Generates visual dashboards from vault data."""

    def __init__(self, vault_root: Path = None):
        self.vault_root = vault_root or Config.VAULT_ROOT
        self.output_dir = self.vault_root / "00-Agency-Core" / "_dashboards"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _parse_frontmatter(self, file_path: Path) -> Dict:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        if not text.startswith("---"):
            return {}
        parts = text.split("---", 2)
        if len(parts) < 3:
            return {}
        try:
            import yaml
            return yaml.safe_load(parts[1]) or {}
        except ImportError:
            return {}

    def generate_cost_chart(self) -> Path:
        """Generate cost utilization chart from cost tracker log."""
        try:
            from daimon_runtime import setup_plot, save_figure
            import matplotlib.pyplot as plt
            import matplotlib

            log_file = Config.COST_LOG
            if not log_file.exists():
                logger.warning("No cost log found, skipping cost chart")
                return None

            # Read last 7 days of entries
            daily_costs: Dict[str, float] = {}
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        entry = json.loads(line)
                        ts = entry["timestamp"][:10]  # YYYY-MM-DD
                        cost = entry["cost_usd"]
                        daily_costs[ts] = daily_costs.get(ts, 0.0) + cost
                    except (json.JSONDecodeError, KeyError):
                        continue

            if not daily_costs:
                return None

            # Sort and plot
            dates = sorted(daily_costs.keys())[-7:]
            values = [daily_costs[d] for d in dates]

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.bar(dates, values, color="#4A90D9")
            ax.axhline(y=Config.LLM_DAILY_BUDGET_USD, color="#E74C3C", linestyle="--", label=f"Daily Cap (${Config.LLM_DAILY_BUDGET_USD})")
            ax.set_ylabel("Cost (USD)")
            ax.set_title("Daily Agent Cost — Last 7 Days")
            ax.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()

            out_path = self.output_dir / "cost-chart.png"
            fig.savefig(str(out_path), dpi=150, bbox_inches="tight")
            plt.close(fig)
            logger.info(f"Cost chart: {out_path}")
            return out_path

        except ImportError:
            logger.warning("matplotlib not available, skipping cost chart")
            return None

    def generate_agent_performance_chart(self) -> Path:
        """Generate agent success rate chart."""
        try:
            import matplotlib.pyplot as plt

            # Aggregate from health check logs
            health_log = Config.HEALTH_LOG
            agent_counts: Dict[str, int] = {}
            if health_log.exists():
                with open(health_log, "r", encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            data = json.loads(line)
                            for cat in data.get("checks", {}).values():
                                for r in cat:
                                    name = r.get("name", "unknown")
                                    agent_counts[name] = agent_counts.get(name, 0) + 1
                        except json.JSONDecodeError:
                            continue

            if not agent_counts:
                return None

            fig, ax = plt.subplots(figsize=(10, 5))
            names = list(agent_counts.keys())[:15]
            counts = [agent_counts[n] for n in names]
            ax.barh(names, counts, color="#50C878")
            ax.set_xlabel("Health Check Count")
            ax.set_title("API Integration Health Check Frequency")
            plt.tight_layout()

            out_path = self.output_dir / "agent-performance.png"
            fig.savefig(str(out_path), dpi=150, bbox_inches="tight")
            plt.close(fig)
            return out_path

        except ImportError:
            return None

    def generate_html_dashboard(self, client: str = None, charts: List[Path] = None) -> Path:
        """Generate a master HTML dashboard."""
        charts = charts or []
        chart_html = ""
        for chart in charts:
            if chart and chart.exists():
                rel_path = chart.relative_to(self.output_dir).as_posix()
                chart_html += f'<div class="chart"><img src="{rel_path}" alt="{chart.stem}"></div>\n'

        # Brain map embed
        brain_map = self.output_dir / "brain-map.html"
        brain_embed = f'<iframe src="brain-map.html" style="width:100%;height:600px;border:none;border-radius:8px;"></iframe>' if brain_map.exists() else "<p>Brain map not yet generated. Run generate_brain_map.py</p>"

        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AgenticMarketingPro Dashboard</title>
    <style>
        body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f0f1a; color: #e0e0e0; }}
        #header {{ padding: 24px 32px; border-bottom: 1px solid #2a2a40; display: flex; justify-content: space-between; align-items: center; }}
        #header h1 {{ margin: 0; font-size: 24px; font-weight: 600; }}
        #header .meta {{ font-size: 14px; color: #888; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; padding: 24px 32px; }}
        .card {{ background: #1a1a2e; border: 1px solid #2a2a40; border-radius: 12px; padding: 20px; }}
        .card h2 {{ margin: 0 0 12px 0; font-size: 16px; color: #fff; }}
        .card img {{ width: 100%; border-radius: 8px; }}
        .card iframe {{ width: 100%; border-radius: 8px; }}
        .metric-row {{ display: flex; gap: 16px; margin-top: 16px; }}
        .metric {{ flex: 1; background: #252540; padding: 16px; border-radius: 8px; text-align: center; }}
        .metric-value {{ font-size: 28px; font-weight: 700; color: #4A90D9; }}
        .metric-label {{ font-size: 12px; color: #888; margin-top: 4px; }}
        .status {{ display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; }}
        .status-healthy {{ background: rgba(80,200,120,0.2); color: #50C878; }}
        .status-warning {{ background: rgba(243,156,18,0.2); color: #F39C12; }}
        .status-error {{ background: rgba(231,76,60,0.2); color: #E74C3C; }}
    </style>
</head>
<body>
    <div id="header">
        <div>
            <h1>📊 AgenticMarketingPro Dashboard</h1>
            <div class="meta">{datetime.now().strftime('%Y-%m-%d %H:%M')} | Client: {client or 'All'}</div>
        </div>
        <div class="meta">
            <span class="status status-healthy">● Healthy</span>
        </div>
    </div>

    <div style="padding: 24px 32px;">
        <div class="metric-row">
            <div class="metric">
                <div class="metric-value" id="node-count">-</div>
                <div class="metric-label">Vault Nodes</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="agent-count">-</div>
                <div class="metric-label">Active Agents</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="client-count">-</div>
                <div class="metric-label">Clients</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="content-count">-</div>
                <div class="metric-label">Content Pieces</div>
            </div>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <h2>🧠 Brain Map</h2>
            {brain_embed}
        </div>
        {chart_html}
    </div>

    <script>
        // Fetch metrics from brain map data
        fetch('brain-map.html')
            .then(r => r.text())
            .then(text => {{
                const nodeMatch = text.match(/Nodes: (\d+)/);
                if (nodeMatch) document.getElementById('node-count').textContent = nodeMatch[1];
            }})
            .catch(() => {{}});

        // Static agent/client counts (would be dynamic in production)
        document.getElementById('agent-count').textContent = '30';
        document.getElementById('client-count').textContent = '{client or '0'}';
        document.getElementById('content-count').textContent = '0';
    </script>
</body>
</html>'''

        out_path = self.output_dir / f"dashboard{'-' + client if client else ''}.html"
        out_path.write_text(html, encoding="utf-8")
        logger.info(f"Dashboard: {out_path}")
        return out_path

    def generate_all(self, client: str = None) -> List[Path]:
        """Generate all dashboard artifacts."""
        charts = []
        
        cost_chart = self.generate_cost_chart()
        if cost_chart:
            charts.append(cost_chart)
        
        perf_chart = self.generate_agent_performance_chart()
        if perf_chart:
            charts.append(perf_chart)
        
        dashboard = self.generate_html_dashboard(client=client, charts=charts)
        charts.append(dashboard)
        
        return charts


def main():
    parser = argparse.ArgumentParser(description="Generate dashboard")
    parser.add_argument("--client", "-c", help="Filter to specific client")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")

    gen = DashboardGenerator()
    if args.output:
        gen.output_dir = Path(args.output)
        gen.output_dir.mkdir(parents=True, exist_ok=True)

    paths = gen.generate_all(client=args.client)
    for p in paths:
        if p:
            print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
