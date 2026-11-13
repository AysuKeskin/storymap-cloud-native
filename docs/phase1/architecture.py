"""Draws the Phase 1 GCP architecture diagram (PNG, PDF, SVG).

Layout is set by hand (1 unit = 1 inch) so that the diagram reads top-down:
users -> load balancer -> ingress -> services -> pods -> data / events.
Run:  python3 architecture.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch, Rectangle
from matplotlib.path import Path

plt.rcParams["font.family"] = ["Helvetica", "Arial", "DejaVu Sans"]
plt.rcParams["svg.fonttype"] = "none"

W, H, Y0 = 25.0, 15.85, 0.3
GREY = "#5f6368"
NODE_FS, EDGE_FS, CLUSTER_FS = 15, 13, 16

fig = plt.figure(figsize=(W, H - Y0))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(Y0, H)
ax.axis("off")


# ---------------------------------------------------------------- helpers
def cluster(x0, y0, x1, y1, label, fill="none", edge=GREY, fc=None,
            ls="-", lw=1.3, label_pos="top", label_x=None, z=1):
    ax.add_patch(FancyBboxPatch(
        (x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0,rounding_size=0.15",
        fc=fill, ec=edge, ls=ls, lw=lw, zorder=z))
    lx = label_x if label_x is not None else (x0 + x1) / 2
    ly = y1 - 0.27 if label_pos == "top" else y0 + 0.25
    ax.text(lx, ly, label, ha="center", va="center", fontsize=CLUSTER_FS,
            color=fc or edge, zorder=z + 0.5)


def node(x, y, w, h, text, fill="#ffffff", edge=GREY, lw=1.3, ls="-",
         shape="box", fs=NODE_FS):
    if shape == "ellipse":
        ax.add_patch(Ellipse((x, y), w, h, fc=fill, ec=edge, lw=lw, zorder=5))
    elif shape == "cylinder":
        cap = 0.22
        ax.add_patch(Rectangle((x - w / 2, y - h / 2 + cap / 2), w, h - cap,
                               fc=fill, ec="none", zorder=5))
        ax.add_patch(Ellipse((x, y - h / 2 + cap / 2), w, cap, fc=fill,
                             ec=edge, lw=lw, zorder=5))
        ax.add_patch(Rectangle((x - w / 2, y - h / 2 + cap / 2), w, h - cap,
                               fc=fill, ec="none", zorder=5.1))
        ax.plot([x - w / 2, x - w / 2], [y - h / 2 + cap / 2, y + h / 2 - cap / 2],
                color=edge, lw=lw, zorder=5.2)
        ax.plot([x + w / 2, x + w / 2], [y - h / 2 + cap / 2, y + h / 2 - cap / 2],
                color=edge, lw=lw, zorder=5.2)
        ax.add_patch(Ellipse((x, y + h / 2 - cap / 2), w, cap, fc=fill,
                             ec=edge, lw=lw, zorder=5.3))
        y -= 0.05
    else:
        ax.add_patch(FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0,rounding_size=0.12",
            fc=fill, ec=edge, lw=lw, ls=ls, zorder=5))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            linespacing=1.25, zorder=6)


def edge(points, label=None, at=None, color=GREY, ls="-", ha="center", style="-|>",
         lw=1.3, fc=None):
    path = Path(points, [Path.MOVETO] + [Path.LINETO] * (len(points) - 1))
    ax.add_patch(FancyArrowPatch(
        path=path, arrowstyle=style + ",head_length=0.55,head_width=0.28",
        mutation_scale=14, color=color, lw=lw, ls=ls,
        joinstyle="miter", capstyle="butt", zorder=4))
    if label:
        ax.text(at[0], at[1], label, ha=ha, va="center", fontsize=EDGE_FS,
                color=fc or ("#000000" if color == GREY else color), zorder=7,
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none",
                          alpha=0.9))


# ---------------------------------------------------------------- clusters
cluster(6.2, 13.25, 12.8, 15.15,
        "Load-testing project (account B, separate free trial)",
        edge="#e37400", ls="--")
cluster(0.3, 0.95, 24.7, 12.95,
        "System project (account A, free trial, max 8 vCPU)  -  us-central1  -  Terraform",
        edge="#1a73e8", ls="--", label_x=11.0)
cluster(0.6, 1.3, 18.0, 10.95, "VPC: storymap-vpc (private subnet)",
        fill="#f8f9fa", edge="#9aa0a6", fc=GREY, label_x=9.3)
cluster(0.9, 6.6, 5.9, 8.55, "Kubernetes Services",
        fill="#eef3fd", edge="#8ab4f8", fc="#1a73e8", z=2)
cluster(6.3, 1.9, 14.6, 10.45,
        "GKE Standard zonal cluster  -  private nodes",
        fill="#e6f4ea", edge="#188038", z=2)
cluster(15.1, 2.4, 17.7, 5.1, "Compute Engine VM",
        fill="#fef7e0", edge="#e37400", label_pos="bottom", z=2)
cluster(18.4, 3.2, 24.4, 7.1, "Event-driven / serverless",
        fill="#fce8e6", edge="#c5221f", label_x=21.4, z=2)
cluster(18.4, 7.6, 21.6, 10.95, "Platform services",
        fill="#f1f3f4", edge="#9aa0a6", fc=GREY, z=2)

# ---------------------------------------------------------------- nodes
node(2.6, 14.25, 2.6, 1.0, "End users\n(web browser)", fill="#e8eaed", shape="ellipse")
node(9.5, 14.05, 4.9, 0.8,
     "locust-vm (e2-standard-4, Spot)\nLocust master + workers, only during tests",
     fill="#fef7e0", fs=13)
node(16.4, 14.25, 2.8, 0.8, "Nominatim API", fill="#e8eaed", shape="ellipse")
node(23.2, 14.25, 3.0, 0.8, "Resend email API", fill="#e8eaed", shape="ellipse")

node(3.3, 11.85, 4.4, 0.8, "External HTTP(S) Load Balancer\nstatic public IP", fill="#e8f0fe")
node(3.3, 9.6, 4.2, 0.8, "GKE Ingress\nstorymap-ingress", fill="#e8f0fe")

node(2.15, 7.4, 2.2, 0.8, "api Service\nport 8000")
node(4.65, 7.4, 2.2, 0.8, "frontend Service\nport 80")

node(7.7, 8.9, 2.4, 0.8, "frontend HPA\n1-3 replicas", fill="#fef7e0")
node(10.6, 8.9, 2.8, 0.8, "api HPA\n2-8 replicas @ 60% CPU", fill="#fef7e0")
node(7.7, 6.0, 2.4, 0.9, "frontend Pods\nnginx + React build")
node(10.6, 6.0, 2.8, 0.9, "api Pods\nDjango REST + Gunicorn", lw=2.2)
node(8.3, 4.2, 2.0, 0.8, "redis Pod\nshared cache + lock")
node(12.8, 4.2, 2.0, 0.8, "migrate Job\nmanage.py migrate", ls="--")
node(10.2, 2.6, 7.2, 0.8,
     "Node pool: 2-3 x e2-standard-2 (4-6 vCPU)\ncluster autoscaler, private nodes",
     fill="#ceead6")

node(16.4, 3.9, 2.4, 1.0, "mysql-vm (e2-medium)\nMySQL 8.0, private IP\nscheduled snapshots",
     fs=14)
node(16.4, 9.9, 2.4, 0.8, "Cloud NAT\noutbound egress", fill="#f1f3f4")

node(19.6, 6.1, 2.0, 0.8, "Pub/Sub topic\nemail-events")
node(23.2, 6.1, 2.0, 0.8, "Cloud Function\nsend-email")
node(19.6, 4.4, 2.2, 1.0, "Cloud Storage bucket\nmedia + thumbnails", shape="cylinder")
node(23.2, 4.4, 2.0, 0.8, "Cloud Function\nmake-thumbnail")

node(20.0, 9.85, 2.6, 0.8, "Artifact Registry\ncontainer images")
node(20.0, 8.45, 2.6, 0.8, "Cloud Monitoring\n+ Logging")

# ---------------------------------------------------------------- edges
ORANGE = "#e37400"
edge([(2.6, 13.75), (2.6, 12.25)], "HTTPS", at=(2.5, 13.05), ha="right")
edge([(7.05, 14.05), (4.4, 14.05), (4.4, 12.25)], "load test via public IP",
     at=(4.55, 13.05), ha="left", color=ORANGE, ls="--")
edge([(3.3, 11.45), (3.3, 10.0)], "routes", at=(3.45, 10.72), ha="left")

edge([(2.15, 9.2), (2.15, 7.8)], "/api/*", at=(2.15, 8.65))
edge([(4.65, 9.2), (4.65, 7.8)], "/*", at=(4.65, 8.65))

edge([(4.65, 7.0), (4.65, 6.0), (6.5, 6.0)])
edge([(2.15, 7.0), (2.15, 5.1), (9.45, 5.1), (9.45, 5.55)])

edge([(7.7, 8.5), (7.7, 6.45)], "monitor & scale", at=(7.7, 7.45), ls=":")
edge([(10.6, 8.5), (10.6, 6.45)], "monitor & scale", at=(10.6, 7.45), ls=":")

edge([(9.9, 5.55), (9.9, 4.2), (9.3, 4.2)], "cache", at=(10.0, 4.75), ha="left")

# every Pod runs on the node pool
edge([(6.75, 5.55), (6.75, 3.0)], "run on", at=(6.75, 3.55), ls=":")
edge([(8.3, 3.8), (8.3, 3.0)], "run on", at=(8.3, 3.4), ls=":")
edge([(11.0, 5.55), (11.0, 3.0)], "run on", at=(11.0, 3.55), ls=":")
edge([(12.8, 3.8), (12.8, 3.0)], "run once per deploy", at=(12.8, 3.4), ls=":")

edge([(13.8, 4.2), (15.2, 4.2)], "migrations", at=(14.5, 4.38), ls="--")
edge([(12.0, 5.6), (16.4, 5.6), (16.4, 4.4)], "SQL :3306", at=(16.5, 4.8), ha="left")
edge([(12.0, 6.35), (14.85, 6.35), (14.85, 9.9), (15.2, 9.9)],
     "egress", at=(14.95, 8.0), ha="left", ls=":")
edge([(16.4, 10.3), (16.4, 13.85)], "geocoding (HTTPS)", at=(16.55, 11.9),
     ha="left", ls=":")

edge([(12.0, 6.1), (18.6, 6.1)], "publish email event", at=(16.4, 6.1))
edge([(12.0, 5.85), (18.2, 5.85), (18.2, 4.4), (18.5, 4.4)],
     "upload media", at=(13.4, 5.85))

edge([(20.6, 6.1), (22.2, 6.1)], "trigger", at=(21.4, 6.1))
edge([(20.7, 4.6), (22.2, 4.6)], "object finalize", at=(21.45, 4.8))
edge([(22.2, 4.15), (20.7, 4.15)], "write thumbnail", at=(21.45, 3.9))
edge([(23.2, 6.5), (23.2, 13.85)], "send e-mail (HTTPS)", at=(23.05, 11.9),
     ha="right", ls=":")

# lanes drawn outside every box
edge([(23.2, 14.65), (23.2, 15.55), (2.6, 15.55), (2.6, 14.75)],
     "e-mail notification", at=(17.0, 15.55), ls="--")
edge([(1.3, 14.25), (0.12, 14.25), (0.12, 0.62), (19.6, 0.62), (19.6, 3.9)],
     "media download (public or signed URL), direct from the bucket",
     at=(9.5, 0.62), ls="--", style="<|-|>")

for ext in ("png", "pdf", "svg"):
    fig.savefig(f"architecture.{ext}", dpi=170 if ext == "png" else None,
                facecolor="white")
print("Wrote architecture.png / .pdf / .svg")
