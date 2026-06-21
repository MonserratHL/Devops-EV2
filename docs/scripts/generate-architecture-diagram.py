#!/usr/bin/env python3
"""Genera diagrama de arquitectura AWS EP3 (ECS Fargate) en SVG y PNG."""

from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent
SVG_PATH = OUTPUT_DIR / "arquitectura-aws.svg"
PNG_PATH = OUTPUT_DIR / "arquitectura-aws.png"

# Colores estilo AWS
AWS_ORANGE = "#FF9900"
AWS_DARK = "#232F3E"
AWS_LIGHT = "#F2F3F3"
PUBLIC_BG = "#E9F3E6"
PRIVATE_BG = "#E8F4FA"
WHITE = "#FFFFFF"
TEXT_DARK = "#16191F"
TEXT_MUTED = "#545B64"
ARROW_BLUE = "#0073BB"
ARROW_GREEN = "#1D8102"
ARROW_ORANGE = "#C45500"
ARROW_RED = "#D13212"

W, H = 1800, 1200


def svg_header() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <marker id="arrow-blue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="{ARROW_BLUE}"/>
    </marker>
    <marker id="arrow-green" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="{ARROW_GREEN}"/>
    </marker>
    <marker id="arrow-orange" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="{ARROW_ORANGE}"/>
    </marker>
    <marker id="arrow-red" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="{ARROW_RED}"/>
    </marker>
    <filter id="shadow" x="-4%" y="-4%" width="108%" height="108%">
      <feDropShadow dx="1" dy="2" stdDeviation="3" flood-opacity="0.15"/>
    </filter>
  </defs>
  <rect width="{W}" height="{H}" fill="{AWS_LIGHT}"/>
'''


def rect(x, y, w, h, fill, stroke, sw=2, rx=6, dash=None):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash_attr}/>'
    )


def text(x, y, content, size=14, weight="normal", fill=TEXT_DARK, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-family="Amazon Ember, Helvetica Neue, Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{content}</text>'
    )


def line(x1, y1, x2, y2, color, marker="arrow-blue", width=2, dash=None):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" '
        f'marker-end="url(#{marker})"{dash_attr}/>'
    )


def arrow_path(d, color, marker="arrow-blue", width=2):
    return (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
        f'marker-end="url(#{marker})"/>'
    )


def service_box(x, y, w, h, title, subtitle, icon_color, icon_label):
    parts = [
        f'<g filter="url(#shadow)">',
        rect(x, y, w, h, WHITE, "#AAB7B8", 1.5, 8),
        rect(x + 10, y + 12, 36, 36, icon_color, icon_color, 0, 8),
        text(x + 28, y + 36, icon_label, 11, "bold", WHITE, "middle"),
        text(x + 56, y + 28, title, 13, "bold"),
        text(x + 56, y + 46, subtitle, 11, "normal", TEXT_MUTED),
        "</g>",
    ]
    return "\n".join(parts)


def generate_svg() -> str:
    parts = [svg_header()]

    # Título
    parts.append(rect(40, 24, W - 80, 56, AWS_DARK, AWS_DARK, 0, 8))
    parts.append(text(W // 2, 58, "Innovatech Chile — Arquitectura AWS (EP3 — ECS Fargate)", 22, "bold", WHITE, "middle"))

    # Usuario / Internet
    parts.append(service_box(60, 110, 200, 72, "Usuarios", "HTTP :80", "#232F3E", "👤"))
    parts.append(text(160, 200, "Internet", 12, "normal", TEXT_MUTED, "middle"))

    # GitHub Actions
    parts.append(service_box(60, 240, 220, 88, "GitHub Actions", "rama deploy · CI/CD", "#24292F", "GH"))
    parts.append(text(170, 345, "Build → Push → Deploy", 11, "normal", TEXT_MUTED, "middle"))

    # AWS Cloud boundary
    aws_x, aws_y, aws_w, aws_h = 320, 100, 1440, 1020
    parts.append(rect(aws_x, aws_y, aws_w, aws_h, "#FAFAFA", AWS_ORANGE, 3, 10))
    parts.append(text(aws_x + 20, aws_y + 32, "AWS Cloud", 18, "bold", AWS_ORANGE))
    parts.append(rect(aws_x + aws_w - 160, aws_y + 14, 140, 32, AWS_DARK, AWS_DARK, 0, 6))
    parts.append(text(aws_x + aws_w - 90, aws_y + 36, "us-east-1", 13, "bold", WHITE, "middle"))

    # ECR
    ecr_x, ecr_y = aws_x + 980, aws_y + 60
    parts.append(service_box(ecr_x, ecr_y, 380, 100, "Amazon ECR", "3 repositorios Docker", "#C7131F", "ECR"))
    parts.append(text(ecr_x + 30, ecr_y + 78, "frontend · backend-ventas · backend-despachos", 10, "normal", TEXT_MUTED))

    # CloudWatch
    cw_x, cw_y = aws_x + 980, aws_y + 880
    parts.append(service_box(cw_x, cw_y, 380, 100, "Amazon CloudWatch", "Logs + Container Insights", "#759C3E", "CW"))
    parts.append(text(cw_x + 30, cw_y + 78, "/ecs/innovatech/* · metricas CPU/Memoria", 10, "normal", TEXT_MUTED))

    # VPC
    vpc_x, vpc_y, vpc_w, vpc_h = aws_x + 30, aws_y + 190, 920, 780
    parts.append(rect(vpc_x, vpc_y, vpc_w, vpc_h, "#FFFDF8", AWS_ORANGE, 2.5, 8, "10,6"))
    parts.append(text(vpc_x + 16, vpc_y + 28, "Amazon VPC  10.1.0.0/16", 16, "bold", AWS_ORANGE))

    # Public subnets
    pub_x, pub_y, pub_w, pub_h = vpc_x + 20, vpc_y + 50, vpc_w - 40, 200
    parts.append(rect(pub_x, pub_y, pub_w, pub_h, PUBLIC_BG, "#7AA116", 2, 8))
    parts.append(text(pub_x + 14, pub_y + 24, "Subredes publicas (2 AZ)", 14, "bold", "#3F6212"))

    # AZ columns public
    az_w = (pub_w - 30) // 2
    parts.append(rect(pub_x + 10, pub_y + 38, az_w, pub_h - 48, "#F4FAF0", "#7AA116", 1, 6, "4,3"))
    parts.append(text(pub_x + 10 + az_w // 2, pub_y + 58, "AZ-a  ·  10.1.1.0/24", 11, "bold", "#3F6212", "middle"))
    parts.append(rect(pub_x + 20 + az_w, pub_y + 38, az_w, pub_h - 48, "#F4FAF0", "#7AA116", 1, 6, "4,3"))
    parts.append(text(pub_x + 20 + az_w + az_w // 2, pub_y + 58, "AZ-b  ·  10.1.2.0/24", 11, "bold", "#3F6212", "middle"))

    # IGW
    igw_x, igw_y = pub_x + 30, pub_y + 90
    parts.append(service_box(igw_x, igw_y, 170, 72, "Internet Gateway", "Acceso publico", "#8C4FFF", "IGW"))

    # ALB
    alb_x, alb_y = pub_x + pub_w // 2 - 110, pub_y + 80
    parts.append(service_box(alb_x, alb_y, 220, 88, "Application LB", "Publico · HTTP :80", "#8C4FFF", "ALB"))
    parts.append(text(alb_x + 110, alb_y + 108, "/  ·  /api/v1/ventas*  ·  /api/v1/despachos*", 9, "normal", TEXT_MUTED, "middle"))

    # NAT
    nat_x, nat_y = pub_x + pub_w - 210, pub_y + 90
    parts.append(service_box(nat_x, nat_y, 180, 72, "NAT Gateway", "Salida privada", "#8C4FFF", "NAT"))

    # Private subnets
    priv_x, priv_y, priv_w, priv_h = vpc_x + 20, pub_y + pub_h + 20, vpc_w - 40, 490
    parts.append(rect(priv_x, priv_y, priv_w, priv_h, PRIVATE_BG, "#0073BB", 2, 8))
    parts.append(text(priv_x + 14, priv_y + 24, "Subredes privadas (2 AZ) — sin IP publica", 14, "bold", "#0F3D75"))

    parts.append(rect(priv_x + 10, priv_y + 38, az_w, priv_h - 48, "#F0F8FF", "#0073BB", 1, 6, "4,3"))
    parts.append(text(priv_x + 10 + az_w // 2, priv_y + 58, "AZ-a  ·  10.1.11.0/24", 11, "bold", "#0F3D75", "middle"))
    parts.append(rect(priv_x + 20 + az_w, priv_y + 38, az_w, priv_h - 48, "#F0F8FF", "#0073BB", 1, 6, "4,3"))
    parts.append(text(priv_x + 20 + az_w + az_w // 2, priv_y + 58, "AZ-b  ·  10.1.12.0/24", 11, "bold", "#0F3D75", "middle"))

    # ECS Cluster box
    ecs_x, ecs_y, ecs_w, ecs_h = priv_x + 30, priv_y + 80, priv_w - 60, 360
    parts.append(rect(ecs_x, ecs_y, ecs_w, ecs_h, WHITE, "#FF9900", 2, 10))
    parts.append(text(ecs_x + 16, ecs_y + 28, "Amazon ECS Fargate — innovatech-cluster", 15, "bold", AWS_ORANGE))
    parts.append(text(ecs_x + 16, ecs_y + 48, "Capacity Providers: FARGATE · Autoscaling CPU/Mem 50%", 11, "normal", TEXT_MUTED))

    # ECS services (2x2 grid)
    svc_w, svc_h = 190, 78
    gap_x, gap_y = 24, 18
    base_x, base_y = ecs_x + 24, ecs_y + 70
    services = [
        ("Frontend", "nginx + React :8080", "#FF9900", "FE"),
        ("Backend Ventas", "Spring Boot :8080", "#FF9900", "BV"),
        ("Backend Despachos", "Spring Boot :8081", "#FF9900", "BD"),
        ("MySQL 8", "Base de datos :3306", "#FF9900", "DB"),
    ]
    for i, (title, sub, color, icon) in enumerate(services):
        col, row = i % 2, i // 2
        sx = base_x + col * (svc_w + gap_x + 180)
        sy = base_y + row * (svc_h + gap_y)
        parts.append(service_box(sx, sy, svc_w, svc_h, title, sub, color, icon))

    # NLB interno MySQL
    nlb_x, nlb_y = ecs_x + ecs_w - 260, ecs_y + ecs_h - 90
    parts.append(service_box(nlb_x, nlb_y, 230, 72, "NLB interno MySQL", "TCP :3306 · DNS estable", "#8C4FFF", "NLB"))

    # Autoscaling badge
    parts.append(rect(ecs_x + ecs_w - 200, ecs_y + 12, 180, 28, "#FFF3E0", AWS_ORANGE, 1.5, 6))
    parts.append(text(ecs_x + ecs_w - 110, ecs_y + 31, "Autoscaling 1-3 tareas", 11, "bold", AWS_ORANGE, "middle"))

    # Flechas — Usuario → ALB
    parts.append(line(260, 146, igw_x - 10, 146, ARROW_BLUE))
    parts.append(line(igw_x + 85, 162, alb_x, 162, ARROW_BLUE))
    parts.append(text(300, 130, "HTTP :80", 10, "bold", ARROW_BLUE))

    # GitHub → ECR
    parts.append(line(280, 280, ecr_x, 310, ARROW_RED, "arrow-red"))
    parts.append(text(420, 268, "push imagenes", 10, "bold", ARROW_RED))

    # GitHub → ECS
    parts.append(arrow_path("M 280 300 Q 600 420 700 520", ARROW_RED, "arrow-red"))
    parts.append(text(480, 400, "force-new-deployment", 10, "bold", ARROW_RED))

    # ECR → ECS (pull via NAT)
    parts.append(arrow_path(f"M {ecr_x} 380 Q {ecr_x - 80} 520 {nat_x + 90} 520", ARROW_ORANGE, "arrow-orange"))
    parts.append(text(ecr_x - 60, 500, "pull imagenes :443", 10, "bold", ARROW_ORANGE))
    parts.append(line(nat_x + 90, 162, nat_x + 90, 480, ARROW_ORANGE, "arrow-orange", 2, "6,4"))

    # ALB → ECS services
    parts.append(line(alb_x + 50, alb_y + 88, base_x + 95, base_y, ARROW_BLUE))
    parts.append(text(alb_x - 30, alb_y + 130, " / ", 10, "bold", ARROW_BLUE))
    parts.append(line(alb_x + 110, alb_y + 88, base_x + svc_w + gap_x + 95, base_y, ARROW_BLUE))
    parts.append(text(alb_x + 130, alb_y + 130, "/api/v1/ventas*", 10, "bold", ARROW_BLUE))
    parts.append(line(alb_x + 170, alb_y + 88, base_x + 95, base_y + svc_h + gap_y, ARROW_BLUE))
    parts.append(text(alb_x + 200, alb_y + 130, "/api/v1/despachos*", 10, "bold", ARROW_BLUE))

    # Backends → NLB → MySQL
    mysql_cx = base_x + svc_w + gap_x + 180 + svc_w // 2
    mysql_cy = base_y + svc_h + gap_y + svc_h // 2
    nlb_cx = nlb_x + 115
    nlb_cy = nlb_y + 36
    bv_cx = base_x + svc_w // 2
    bv_cy = base_y + svc_h // 2
    bd_cx = base_x + svc_w + gap_x + 180 + svc_w // 2
    bd_cy = base_y + svc_h // 2
    parts.append(line(bv_cx, bv_cy + 39, nlb_cx - 40, nlb_cy, ARROW_GREEN, "arrow-green"))
    parts.append(line(bd_cx, bd_cy + 39, nlb_cx + 40, nlb_cy, ARROW_GREEN, "arrow-green"))
    parts.append(line(nlb_cx, nlb_cy + 36, mysql_cx, mysql_cy - 39, ARROW_GREEN, "arrow-green"))
    parts.append(text(nlb_x - 10, nlb_y - 8, "MySQL :3306", 10, "bold", ARROW_GREEN))

    # ECS → CloudWatch
    parts.append(line(ecs_x + ecs_w - 40, ecs_y + ecs_h, cw_x, cw_y + 20, "#759C3E", "arrow-green", 1.5, "5,4"))
    parts.append(text(960, 820, "logs y metricas", 10, "bold", "#759C3E"))

    # Leyenda
    leg_x, leg_y = aws_x + 30, aws_y + 920
    parts.append(rect(leg_x, leg_y, 880, 70, WHITE, "#AAB7B8", 1, 8))
    parts.append(text(leg_x + 16, leg_y + 24, "Leyenda de flujos", 13, "bold"))
    legend_items = [
        (ARROW_BLUE, "Trafico HTTP usuario / ALB → ECS"),
        (ARROW_GREEN, "Backends → NLB interno → MySQL"),
        (ARROW_ORANGE, "Pull de imagenes ECR via NAT Gateway"),
        (ARROW_RED, "CI/CD: GitHub Actions → ECR + ECS"),
    ]
    for i, (color, label) in enumerate(legend_items):
        lx = leg_x + 16 + (i % 2) * 430
        ly = leg_y + 44 + (i // 2) * 22
        parts.append(f'<rect x="{lx}" y="{ly - 10}" width="24" height="4" fill="{color}" rx="2"/>')
        parts.append(text(lx + 32, ly, label, 11, "normal", TEXT_MUTED))

    # Footer
    parts.append(text(
        W // 2, H - 24,
        "Flujo: push deploy → build → ECR → ECS update → ALB → usuario  |  "
        "Backends → NLB MySQL :3306  |  Observabilidad: CloudWatch Logs + Container Insights",
        12, "normal", TEXT_MUTED, "middle",
    ))

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    svg_content = generate_svg()
    SVG_PATH.write_text(svg_content, encoding="utf-8")
    print(f"SVG generado: {SVG_PATH}")

    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), write_to=str(PNG_PATH), scale=2.0)
        print(f"PNG generado: {PNG_PATH}")
    except Exception as exc:
        print(f"Advertencia: no se pudo generar PNG ({exc}). Solo SVG disponible.")


if __name__ == "__main__":
    main()
