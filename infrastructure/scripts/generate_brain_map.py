"""
AgenticMarketingPro — Brain Map Generator
=========================================
Scans the vault, extracts entities and relationships, and generates a
D3.js force-directed graph showing all clients, websites, keywords,
competitors, agents, content pieces, and their connections.

Usage:
    python scripts/generate_brain_map.py
    python scripts/generate_brain_map.py --client acme
    python scripts/generate_brain_map.py --output brain-map.html
"""

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config

logger = logging.getLogger("amp.brain_map")


@dataclass
class Node:
    id: str
    label: str
    type: str  # client, website, keyword, competitor, agent, content, page, metric
    group: str
    size: int = 10
    metadata: Dict = field(default_factory=dict)


@dataclass
class Edge:
    source: str
    target: str
    type: str  # owns, ranks_for, targets, wrote, monitors, competes_with, links_to, cites
    weight: float = 1.0


class VaultBrainMap:
    """Extracts entities and relationships from the vault for visualization."""

    NODE_COLORS = {
        "client": "#4A90D9",
        "website": "#50C878",
        "keyword": "#FFD700",
        "competitor": "#E74C3C",
        "agent": "#9B59B6",
        "content": "#F39C12",
        "page": "#1ABC9C",
        "metric": "#ECF0F1",
        "campaign": "#E67E22",
        "persona": "#34495E",
    }

    def __init__(self, vault_root: Path = None):
        self.vault_root = vault_root or Config.VAULT_ROOT
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.client_map: Dict[str, str] = {}  # website -> client slug

    def _extract_frontmatter(self, text: str) -> Dict:
        """Extract YAML frontmatter from markdown."""
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

    def _slugify(self, text: str) -> str:
        return re.sub(r'[^a-z0-9]+', '_', text.lower().strip()).strip('_')

    def _add_node(self, node_id: str, label: str, node_type: str, size: int = 10, metadata: Dict = None):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(
                id=node_id,
                label=label,
                type=node_type,
                group=node_type,
                size=size,
                metadata=metadata or {},
            )
        else:
            # Update size for existing nodes (more references = bigger)
            self.nodes[node_id].size += size // 2

    def _add_edge(self, source: str, target: str, edge_type: str, weight: float = 1.0):
        if source and target and source != target:
            self.edges.append(Edge(source, target, edge_type, weight))

    # ── Entity Extraction ─────────────────────────────────────────────────

    def extract_clients(self):
        """Extract clients and their websites."""
        clients_dir = self.vault_root / "01-Clients"
        if not clients_dir.exists():
            return

        for client_dir in clients_dir.iterdir():
            if not client_dir.is_dir() or client_dir.name.startswith("_"):
                continue

            client_slug = client_dir.name
            client_id = f"client:{client_slug}"
            client_name = client_slug.replace("-", " ").title()
            website = ""

            # Read client-profile.md
            profile_file = client_dir / "client-profile.md"
            if profile_file.exists():
                fm = self._extract_frontmatter(profile_file.read_text(encoding="utf-8"))
                client_name = fm.get("client", client_name)
                website = fm.get("website", "")
                mrr = fm.get("mrr", 0)
                tier = fm.get("tier", "")
                self._add_node(
                    client_id, client_name, "client", size=20,
                    metadata={"mrr": mrr, "tier": tier, "website": website}
                )

            # Read website-manifest.md
            manifest_file = client_dir / "website-manifest.md"
            if manifest_file.exists():
                fm = self._extract_frontmatter(manifest_file.read_text(encoding="utf-8"))
                website = fm.get("website", website)

            if website:
                web_id = f"website:{self._slugify(website)}"
                self._add_node(web_id, website, "website", size=15, metadata={"client": client_slug})
                self._add_edge(client_id, web_id, "owns")
                self.client_map[website] = client_slug

    def extract_keywords(self):
        """Extract keywords from keyword-universe.md."""
        kw_file = self.vault_root / "03-SEO-Intelligence" / "keyword-universe.md"
        if not kw_file.exists():
            return

        text = kw_file.read_text(encoding="utf-8")
        # Extract table rows after "Keyword schema" header
        lines = text.split("\n")
        in_table = False
        for line in lines:
            if "Keyword |" in line and "Volume" in line:
                in_table = True
                continue
            if in_table and line.startswith("|") and "Keyword" not in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 2:
                    keyword = parts[1]
                    if keyword and not keyword.startswith("---"):
                        kw_id = f"keyword:{self._slugify(keyword)}"
                        self._add_node(kw_id, keyword, "keyword", size=8)
                        # Link to client if found in row
                        client = parts[5] if len(parts) > 5 else ""
                        if client:
                            self._add_edge(f"client:{self._slugify(client)}", kw_id, "targets")
                        # Link to cluster
                        cluster = parts[4] if len(parts) > 4 else ""
                        if cluster:
                            cluster_id = f"cluster:{self._slugify(cluster)}"
                            self._add_node(cluster_id, cluster, "metric", size=6)
                            self._add_edge(kw_id, cluster_id, "belongs_to")
            elif in_table and not line.startswith("|"):
                in_table = False

    def extract_competitors(self):
        """Extract competitors from competitor-map.md."""
        comp_file = self.vault_root / "02-Competitors" / "competitor-map.md"
        if comp_file.exists():
            text = comp_file.read_text(encoding="utf-8")
            # Simple pattern matching for competitor URLs/names
            for match in re.finditer(r'\*\*([^*]+)\*\*.*?(https?://[^\s\)]+)', text):
                name = match.group(1).strip()
                url = match.group(2).strip()
                comp_id = f"competitor:{self._slugify(name)}"
                self._add_node(comp_id, name, "competitor", size=12)
                if url:
                    web_id = f"website:{self._slugify(url)}"
                    self._add_node(web_id, url, "website", size=10)
                    self._add_edge(comp_id, web_id, "owns")

    def extract_agents(self):
        """Extract agents from agent configs."""
        configs_dir = self.vault_root / "11-Ops" / "agent-configs"
        if not configs_dir.exists():
            return

        for config_file in configs_dir.glob("*.md"):
            agent_name = config_file.stem
            agent_id = f"agent:{agent_name}"
            fm = self._extract_frontmatter(config_file.read_text(encoding="utf-8"))
            role = fm.get("role", agent_name.replace("-", " ").title())
            self._add_node(agent_id, role, "agent", size=10, metadata={"config": str(config_file)})

    def extract_content(self):
        """Extract content pieces from published-index.md and briefs."""
        published_file = self.vault_root / "04-Content-Production" / "published-index.md"
        if published_file.exists():
            text = published_file.read_text(encoding="utf-8")
            for match in re.finditer(r'\| ([^|]+) \| ([^|]+) \|', text):
                title = match.group(1).strip()
                if title and not title.startswith("---"):
                    content_id = f"content:{self._slugify(title)}"
                    self._add_node(content_id, title, "content", size=8)

    def extract_relationships(self):
        """Extract implicit relationships from wiki links [[...]] and URLs."""
        for md_file in self.vault_root.rglob("*.md"):
            text = md_file.read_text(encoding="utf-8", errors="ignore")
            # Find wiki links
            for match in re.finditer(r'\[\[([^\]]+)\]\]', text):
                target = match.group(1).strip()
                # Link from file to target
                file_id = f"page:{self._slugify(md_file.stem)}"
                self._add_node(file_id, md_file.stem, "page", size=5)
                target_id = f"page:{self._slugify(target)}"
                self._add_node(target_id, target, "page", size=5)
                self._add_edge(file_id, target_id, "links_to")

    # ── Visualization ─────────────────────────────────────────────────

    def generate_html(self, center_client: str = None, output_path: Path = None) -> Path:
        """Generate D3.js force-directed graph HTML."""
        self.extract_clients()
        self.extract_keywords()
        self.extract_competitors()
        self.extract_agents()
        self.extract_content()
        self.extract_relationships()

        # Filter to center client if specified
        if center_client:
            # Find all nodes connected to this client
            connected = set([f"client:{center_client}"])
            for edge in self.edges:
                if edge.source in connected or edge.target in connected:
                    connected.add(edge.source)
                    connected.add(edge.target)
            # Filter nodes
            self.nodes = {k: v for k, v in self.nodes.items() if k in connected}
            self.edges = [e for e in self.edges if e.source in self.nodes and e.target in self.nodes]

        nodes_json = json.dumps([
            {
                "id": n.id,
                "label": n.label,
                "group": n.group,
                "size": n.size,
                "color": self.NODE_COLORS.get(n.type, "#95A5A6"),
                "metadata": n.metadata,
            }
            for n in self.nodes.values()
        ])

        edges_json = json.dumps([
            {"source": e.source, "target": e.target, "type": e.type, "weight": e.weight}
            for e in self.edges
        ])

        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AgenticMarketingPro — Brain Map</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #1a1a2e; color: #fff; }}
        #header {{ padding: 20px 30px; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center; }}
        #header h1 {{ margin: 0; font-size: 20px; font-weight: 600; }}
        #header .meta {{ font-size: 13px; color: #888; }}
        #legend {{ padding: 15px 30px; display: flex; gap: 20px; font-size: 12px; flex-wrap: wrap; }}
        #legend .item {{ display: flex; align-items: center; gap: 6px; }}
        #legend .dot {{ width: 10px; height: 10px; border-radius: 50%; }}
        #graph {{ width: 100vw; height: calc(100vh - 100px); }}
        #tooltip {{ position: absolute; padding: 10px 14px; background: rgba(0,0,0,0.9); border: 1px solid #444; border-radius: 6px; font-size: 12px; pointer-events: none; opacity: 0; transition: opacity 0.2s; max-width: 280px; }}
        #tooltip h4 {{ margin: 0 0 6px 0; font-size: 13px; color: #fff; }}
        #tooltip p {{ margin: 0; color: #aaa; line-height: 1.5; }}
        #tooltip .meta {{ color: #888; font-size: 11px; margin-top: 4px; }}
        .controls {{ position: fixed; bottom: 20px; right: 20px; display: flex; gap: 8px; }}
        .controls button {{ padding: 8px 14px; border: none; border-radius: 6px; background: #4A90D9; color: white; font-size: 12px; cursor: pointer; }}
        .controls button:hover {{ background: #357ABD; }}
    </style>
</head>
<body>
    <div id="header">
        <div>
            <h1>🧠 AgenticMarketingPro Brain Map</h1>
            <div class="meta">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Nodes: {len(self.nodes)} | Edges: {len(self.edges)}</div>
        </div>
        <div class="meta">Client: {center_client or 'All'}</div>
    </div>
    <div id="legend">
        <div class="item"><div class="dot" style="background:#4A90D9"></div> Client</div>
        <div class="item"><div class="dot" style="background:#50C878"></div> Website</div>
        <div class="item"><div class="dot" style="background:#FFD700"></div> Keyword</div>
        <div class="item"><div class="dot" style="background:#E74C3C"></div> Competitor</div>
        <div class="item"><div class="dot" style="background:#9B59B6"></div> Agent</div>
        <div class="item"><div class="dot" style="background:#F39C12"></div> Content</div>
        <div class="item"><div class="dot" style="background:#1ABC9C"></div> Page</div>
        <div class="item"><div class="dot" style="background:#E67E22"></div> Campaign</div>
    </div>
    <div id="graph"></div>
    <div id="tooltip"></div>
    <div class="controls">
        <button onclick="resetZoom()">Reset Zoom</button>
        <button onclick="toggleLabels()">Toggle Labels</button>
    </div>
    <script>
        const nodes = {nodes_json};
        const links = {edges_json};

        const width = window.innerWidth;
        const height = window.innerHeight - 100;

        const svg = d3.select("#graph").append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height]);

        const g = svg.append("g");

        const zoom = d3.zoom()
            .scaleExtent([0.1, 4])
            .on("zoom", (event) => g.attr("transform", event.transform));

        svg.call(zoom);

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id).distance(80))
            .force("charge", d3.forceManyBody().strength(-200))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(d => d.size + 5));

        const link = g.append("g").attr("stroke", "#444").attr("stroke-opacity", 0.6)
            .selectAll("line").data(links).join("line")
            .attr("stroke-width", d => Math.sqrt(d.weight));

        const node = g.append("g")
            .selectAll("g").data(nodes).join("g")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        node.append("circle")
            .attr("r", d => d.size)
            .attr("fill", d => d.color)
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .on("mouseover", showTooltip)
            .on("mouseout", hideTooltip)
            .on("click", (event, d) => console.log(d));

        let labelsVisible = true;
        const labels = node.append("text")
            .text(d => d.label.length > 20 ? d.label.slice(0, 20) + "..." : d.label)
            .attr("x", d => d.size + 3)
            .attr("y", 4)
            .attr("font-size", "10px")
            .attr("fill", "#ccc")
            .attr("pointer-events", "none");

        simulation.on("tick", () => {{
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
            node
                .attr("transform", d => `translate(${{d.x}},${{d.y}})`);
        }});

        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x; d.fy = d.y;
        }}
        function dragged(event, d) {{
            d.fx = event.x; d.fy = event.y;
        }}
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null; d.fy = null;
        }}

        function showTooltip(event, d) {{
            const tooltip = document.getElementById("tooltip");
            tooltip.innerHTML = `<h4>${{d.label}}</h4><p>Type: ${{d.group}}</p><p>ID: ${{d.id}}</p>${{d.metadata && Object.keys(d.metadata).length ? '<div class="meta">' + Object.entries(d.metadata).map(([k,v]) => `${{k}}: ${{v}`).join('<br>') + '</div>' : ''}}`;
            tooltip.style.left = (event.pageX + 10) + "px";
            tooltip.style.top = (event.pageY + 10) + "px";
            tooltip.style.opacity = 1;
        }}
        function hideTooltip() {{
            document.getElementById("tooltip").style.opacity = 0;
        }}
        function resetZoom() {{
            svg.transition().duration(750).call(zoom.transform, d3.zoomIdentity);
        }}
        function toggleLabels() {{
            labelsVisible = !labelsVisible;
            labels.style("display", labelsVisible ? "block" : "none");
        }}
    </script>
</body>
</html>'''

        output_path = output_path or self.vault_root / "00-Agency-Core" / "_dashboards" / "brain-map.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        logger.info(f"Brain map generated: {output_path} ({len(self.nodes)} nodes, {len(self.edges)} edges)")
        return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate vault brain map")
    parser.add_argument("--client", "-c", help="Center map on a specific client")
    parser.add_argument("--output", "-o", help="Output HTML file path")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")

    bm = VaultBrainMap()
    output = bm.generate_html(
        center_client=args.client,
        output_path=Path(args.output) if args.output else None,
    )
    print(f"Brain map: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
