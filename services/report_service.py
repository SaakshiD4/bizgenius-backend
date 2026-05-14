# import sys
# import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from io import BytesIO
# from datetime import datetime
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
# from reportlab.lib import colors
# from reportlab.platypus import (
#     SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
#     HRFlowable, PageBreak
# )
# from reportlab.lib.enums import TA_LEFT, TA_CENTER


# # ── Color palette ──
# PURPLE     = colors.HexColor("#7c6bff")
# DARK_BG    = colors.HexColor("#0d0d24")
# LIGHT_BG   = colors.HexColor("#f8f7ff")
# GREEN      = colors.HexColor("#34d399")
# RED        = colors.HexColor("#f87171")
# YELLOW     = colors.HexColor("#fbbf24")
# GRAY       = colors.HexColor("#64748b")
# WHITE      = colors.white
# BLACK      = colors.HexColor("#1e1b4b")


# def _styles():
#     s = getSampleStyleSheet()
#     base = dict(fontName="Helvetica", textColor=BLACK)

#     h1 = ParagraphStyle("H1", **base, fontSize=22, fontName="Helvetica-Bold",
#                          textColor=PURPLE, spaceAfter=6)
#     h2 = ParagraphStyle("H2", **base, fontSize=15, fontName="Helvetica-Bold",
#                          textColor=BLACK, spaceBefore=14, spaceAfter=4)
#     h3 = ParagraphStyle("H3", **base, fontSize=12, fontName="Helvetica-Bold",
#                          textColor=PURPLE, spaceBefore=8, spaceAfter=3)
#     body = ParagraphStyle("Body", **base, fontSize=10, leading=15, spaceAfter=4)
#     small = ParagraphStyle("Small", **base, fontSize=9, textColor=GRAY, leading=13)
#     center = ParagraphStyle("Center", **base, fontSize=10, alignment=TA_CENTER)
#     tag_green  = ParagraphStyle("TagG",  **base, fontSize=10, textColor=GREEN,  fontName="Helvetica-Bold")
#     tag_red    = ParagraphStyle("TagR",  **base, fontSize=10, textColor=RED,    fontName="Helvetica-Bold")
#     tag_yellow = ParagraphStyle("TagY",  **base, fontSize=10, textColor=YELLOW, fontName="Helvetica-Bold")

#     return dict(h1=h1, h2=h2, h3=h3, body=body, small=small,
#                 center=center, tag_green=tag_green, tag_red=tag_red, tag_yellow=tag_yellow)


# def _divider():
#     return HRFlowable(width="100%", thickness=1, color=PURPLE, spaceAfter=8, spaceBefore=8)


# def generate_pdf_report(data: dict) -> BytesIO:
#     ui   = data["user_input"]
#     ml   = data["ml_results"]
#     analysis   = data.get("analysis", "")
#     competitors = data.get("competitors", [])
#     hierarchy   = data.get("hierarchy", {})
#     risks       = data.get("probable_risks", [])

#     buf = BytesIO()
#     doc = SimpleDocTemplate(buf, pagesize=letter,
#                              leftMargin=0.75*inch, rightMargin=0.75*inch,
#                              topMargin=0.75*inch,  bottomMargin=0.75*inch)
#     st  = _styles()
#     story = []

#     # ── Cover ──
#     story.append(Spacer(1, 0.3*inch))
#     story.append(Paragraph("BizGenius Startup Report", st["h1"]))
#     story.append(Paragraph(
#         f"<b>Domain:</b> {ui.get('domain')}  •  "
#         f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y %H:%M')}",
#         st["small"]
#     ))
#     story.append(_divider())

#     # ── Startup Snapshot ──
#     story.append(Paragraph("1. Startup Snapshot", st["h2"]))
#     snap = [
#         ["Field", "Value"],
#         ["Domain",            ui.get("domain","—")],
#         ["Idea",              ui.get("description","—")[:120]],
#         ["Company Age",       f"{ui.get('company_age','—')} years"],
#         ["Founders",          str(ui.get("founder_count","—"))],
#         ["Employees",         str(ui.get("employees","—"))],
#         ["Funding Rounds",    str(ui.get("funding_rounds","—"))],
#         ["Avg Funding/Round", f"${ui.get('funding_per_round',0):,.0f}"],
#         ["Investors",         str(ui.get("investor_count","—"))],
#     ]
#     t = Table(snap, colWidths=[2.2*inch, 4.8*inch])
#     t.setStyle(TableStyle([
#         ("BACKGROUND",   (0,0), (-1,0),  PURPLE),
#         ("TEXTCOLOR",    (0,0), (-1,0),  WHITE),
#         ("FONTNAME",     (0,0), (-1,0),  "Helvetica-Bold"),
#         ("FONTSIZE",     (0,0), (-1,-1), 9),
#         ("ROWBACKGROUNDS",(0,1),(-1,-1), [LIGHT_BG, WHITE]),
#         ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#e2e8f0")),
#         ("LEFTPADDING",  (0,0), (-1,-1), 8),
#         ("RIGHTPADDING", (0,0), (-1,-1), 8),
#         ("TOPPADDING",   (0,0), (-1,-1), 5),
#         ("BOTTOMPADDING",(0,0), (-1,-1), 5),
#     ]))
#     story.append(t)
#     story.append(Spacer(1, 0.15*inch))

#     # ── ML Results ──
#     story.append(Paragraph("2. ML Prediction Results", st["h2"]))
#     classification = ml.get("classification", "—")
#     sp = ml.get("success_probability", 0) * 100
#     risk = ml.get("risk_level", "—")
#     pred_fund = ml.get("predicted_funding_usd", 0)

#     tag_style = st["tag_green"] if classification == "Success" else (
#                 st["tag_red"] if classification == "Failure" else st["tag_yellow"])
#     story.append(Paragraph(f"Classification: {classification}", tag_style))

#     ml_data = [
#         ["Metric", "Value"],
#         ["Success Probability",      f"{sp:.1f}%"],
#         ["Risk Level",               risk],
#         ["Predicted Next Funding",   f"${pred_fund:,.2f}"],
#     ]
#     mt = Table(ml_data, colWidths=[3*inch, 4*inch])
#     mt.setStyle(TableStyle([
#         ("BACKGROUND",  (0,0), (-1,0), PURPLE),
#         ("TEXTCOLOR",   (0,0), (-1,0), WHITE),
#         ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
#         ("FONTSIZE",    (0,0), (-1,-1), 9),
#         ("ROWBACKGROUNDS",(0,1),(-1,-1),[LIGHT_BG, WHITE]),
#         ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#e2e8f0")),
#         ("LEFTPADDING", (0,0), (-1,-1), 8),
#         ("TOPPADDING",  (0,0), (-1,-1), 5),
#         ("BOTTOMPADDING",(0,0),(-1,-1), 5),
#     ]))
#     story.append(mt)
#     story.append(Spacer(1, 0.15*inch))

#     # ── Risk Management ──
#     story.append(Paragraph("3. Risk Management", st["h2"]))
#     for r in risks:
#         story.append(Paragraph(f"⚠  {r}", st["body"]))
#     story.append(Spacer(1, 0.1*inch))

#     # ── Competitors ──
#     story.append(Paragraph("4. Competitor Analysis", st["h2"]))
#     if competitors:
#         for i, c in enumerate(competitors, 1):
#             doc_text = c.get("document", c.get("summary", str(c)))
#             story.append(Paragraph(f"{i}. {doc_text}", st["body"]))
#     else:
#         story.append(Paragraph("No competitor data available.", st["small"]))
#     story.append(Spacer(1, 0.1*inch))

#     # ── Team Hierarchy ──
#     story.append(Paragraph("5. Team Hierarchy & Skills", st["h2"]))
#     story.append(Paragraph(
#         f"<b>CEO:</b> {hierarchy.get('ceo_title','CEO')}  •  "
#         f"<b>Total Employees:</b> {hierarchy.get('total_employees','—')}",
#         st["body"]
#     ))

#     depts = hierarchy.get("departments", [])
#     if depts:
#         dept_data = [["Department", "Headcount", "Key Roles", "Skills Needed"]]
#         for d in depts:
#             dept_data.append([
#                 d.get("name",""),
#                 str(d.get("headcount","")),
#                 ", ".join(d.get("roles",[])),
#                 ", ".join(d.get("skills_needed",[])),
#             ])
#         dt = Table(dept_data, colWidths=[1.5*inch, 1*inch, 2.5*inch, 2*inch])
#         dt.setStyle(TableStyle([
#             ("BACKGROUND",  (0,0),(-1,0), PURPLE),
#             ("TEXTCOLOR",   (0,0),(-1,0), WHITE),
#             ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
#             ("FONTSIZE",    (0,0),(-1,-1), 8),
#             ("ROWBACKGROUNDS",(0,1),(-1,-1),[LIGHT_BG, WHITE]),
#             ("GRID",        (0,0),(-1,-1), 0.4, colors.HexColor("#e2e8f0")),
#             ("LEFTPADDING", (0,0),(-1,-1), 6),
#             ("TOPPADDING",  (0,0),(-1,-1), 4),
#             ("BOTTOMPADDING",(0,0),(-1,-1), 4),
#             ("WORDWRAP",    (0,0),(-1,-1), True),
#         ]))
#         story.append(dt)

#     gaps = hierarchy.get("hiring_gaps", [])
#     if gaps:
#         story.append(Spacer(1, 0.1*inch))
#         story.append(Paragraph("<b>Hiring Gaps:</b> " + ", ".join(gaps), st["body"]))

#     next_hires = hierarchy.get("recommended_next_hires", [])
#     if next_hires:
#         story.append(Paragraph("Recommended Next Hires:", st["h3"]))
#         for h in next_hires:
#             story.append(Paragraph(
#                 f"• <b>{h.get('role')}</b> [{h.get('priority')}] — {h.get('reason')}",
#                 st["body"]
#             ))

#     insight = hierarchy.get("org_insight", "")
#     if insight:
#         story.append(Spacer(1, 0.1*inch))
#         story.append(Paragraph(insight, st["small"]))

#     story.append(Spacer(1, 0.15*inch))

#     # ── LLM Strategic Analysis ──
#     story.append(PageBreak())
#     story.append(Paragraph("6. Strategic Analysis & 30-Day Action Plan", st["h2"]))
#     story.append(_divider())

#     if analysis:
#         for line in analysis.split("\n"):
#             line = line.strip()
#             if not line:
#                 story.append(Spacer(1, 0.05*inch))
#             elif line.startswith("**") and line.endswith("**"):
#                 story.append(Paragraph(line.replace("**",""), st["h3"]))
#             elif line.startswith("##"):
#                 story.append(Paragraph(line.replace("#","").strip(), st["h2"]))
#             elif line.startswith("#"):
#                 story.append(Paragraph(line.replace("#","").strip(), st["h1"]))
#             else:
#                 safe = line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
#                 story.append(Paragraph(safe, st["body"]))
#     else:
#         story.append(Paragraph("Analysis not available.", st["small"]))

#     # ── Footer ──
#     story.append(Spacer(1, 0.3*inch))
#     story.append(_divider())
#     story.append(Paragraph(
#         f"Generated by BizGenius  •  {datetime.now().strftime('%Y-%m-%d %H:%M')}  •  Confidential",
#         st["small"]
#     ))

#     doc.build(story)
#     buf.seek(0)
#     return buf

# """
# BizGenius FastAPI Backend - Report Service
# Fully corrected version:
#   - Fixed IndentationError in competitors block
#   - Removed invalid WORDWRAP TableStyle command
#   - Added VALIGN TOP everywhere
#   - Wrapped long cell text in Paragraph() for auto-wrap
#   - Safe HTML escaping throughout analysis section
# """

# import sys
# import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from io import BytesIO
# from datetime import datetime
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
# from reportlab.lib import colors
# from reportlab.platypus import (
#     SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
#     HRFlowable, PageBreak
# )
# from reportlab.lib.enums import TA_LEFT, TA_CENTER


# # ── Color palette ──────────────────────────────────────────────
# PURPLE  = colors.HexColor("#7c6bff")
# DARK_BG = colors.HexColor("#0d0d24")
# LIGHT_BG= colors.HexColor("#f8f7ff")
# GREEN   = colors.HexColor("#34d399")
# RED     = colors.HexColor("#f87171")
# YELLOW  = colors.HexColor("#fbbf24")
# GRAY    = colors.HexColor("#64748b")
# WHITE   = colors.white
# BLACK   = colors.HexColor("#1e1b4b")
# ORANGE  = colors.HexColor("#fb923c")


# def _styles():
#     s = getSampleStyleSheet()

#     h1 = ParagraphStyle("H1", fontSize=22, fontName="Helvetica-Bold",
#                          textColor=PURPLE, spaceAfter=6)
#     h2 = ParagraphStyle("H2", fontSize=15, fontName="Helvetica-Bold",
#                          textColor=BLACK, spaceBefore=14, spaceAfter=4)
#     h3 = ParagraphStyle("H3", fontSize=12, fontName="Helvetica-Bold",
#                          textColor=PURPLE, spaceBefore=8, spaceAfter=3)
#     h4 = ParagraphStyle("H4", fontSize=11, fontName="Helvetica-Bold",
#                          textColor=BLACK, spaceBefore=6, spaceAfter=2)
#     body   = ParagraphStyle("Body",   fontName="Helvetica", fontSize=10,
#                              textColor=BLACK, leading=15, spaceAfter=4)
#     small  = ParagraphStyle("Small",  fontName="Helvetica", fontSize=9,
#                              textColor=GRAY, leading=13)
#     center = ParagraphStyle("Center", fontName="Helvetica", fontSize=10,
#                              textColor=BLACK, alignment=TA_CENTER)
#     tag_green  = ParagraphStyle("TagG", fontName="Helvetica-Bold", fontSize=10, textColor=GREEN)
#     tag_red    = ParagraphStyle("TagR", fontName="Helvetica-Bold", fontSize=10, textColor=RED)
#     tag_yellow = ParagraphStyle("TagY", fontName="Helvetica-Bold", fontSize=10, textColor=YELLOW)
#     tag_orange = ParagraphStyle("TagO", fontName="Helvetica-Bold", fontSize=10, textColor=ORANGE)

#     return dict(h1=h1, h2=h2, h3=h3, h4=h4, body=body, small=small,
#                 center=center, tag_green=tag_green, tag_red=tag_red,
#                 tag_yellow=tag_yellow, tag_orange=tag_orange)


# def _divider():
#     return HRFlowable(width="100%", thickness=1,   color=PURPLE, spaceAfter=8, spaceBefore=8)

# def _section_divider():
#     return HRFlowable(width="100%", thickness=0.5, color=GRAY,   spaceAfter=6, spaceBefore=6)

# def _safe(text: str) -> str:
#     """Escape HTML special chars so ReportLab Paragraph doesn't choke."""
#     return (str(text)
#             .replace("&", "&amp;")
#             .replace("<", "&lt;")
#             .replace(">", "&gt;"))

# # ── Shared TableStyle helper ────────────────────────────────────
# def _base_table_style(header_color=PURPLE, row_colors=None, grid_color="#e2e8f0"):
#     if row_colors is None:
#         row_colors = [LIGHT_BG, WHITE]
#     return TableStyle([
#         ("BACKGROUND",    (0, 0), (-1, 0),  header_color),
#         ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
#         ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
#         ("FONTSIZE",      (0, 0), (-1, -1), 9),
#         ("ROWBACKGROUNDS",(0, 1), (-1, -1), row_colors),
#         ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor(grid_color)),
#         ("LEFTPADDING",   (0, 0), (-1, -1), 8),
#         ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
#         ("TOPPADDING",    (0, 0), (-1, -1), 5),
#         ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
#         ("VALIGN",        (0, 0), (-1, -1), "TOP"),
#     ])


# # ════════════════════════════════════════════════════════════════
# # MAIN ENTRY POINT
# # ════════════════════════════════════════════════════════════════
# def generate_pdf_report(data: dict) -> BytesIO:
#     ui           = data["user_input"]
#     ml           = data["ml_results"]
#     analysis     = data.get("analysis", "")
#     competitors  = data.get("competitors", [])
#     hierarchy    = data.get("hierarchy", {})
#     risks        = data.get("probable_risks", [])
#     hiring_guide = data.get("hiring_guide", {})

#     buf = BytesIO()
#     doc = SimpleDocTemplate(
#         buf, pagesize=letter,
#         leftMargin=0.75*inch, rightMargin=0.75*inch,
#         topMargin=0.75*inch,  bottomMargin=0.75*inch,
#     )
#     st    = _styles()
#     story = []

#     # ────────────────────────────────────────
#     # COVER
#     # ────────────────────────────────────────
#     story.append(Spacer(1, 0.3*inch))
#     story.append(Paragraph("BizGenius Startup Intelligence Report", st["h1"]))
#     story.append(Paragraph(
#         f"<b>Domain:</b> {_safe(ui.get('domain', ''))}  •  "
#         f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y %H:%M')}",
#         st["small"],
#     ))
#     story.append(_divider())

#     # ────────────────────────────────────────
#     # 1. STARTUP SNAPSHOT
#     # ────────────────────────────────────────
#     story.append(Paragraph("1. Startup Snapshot", st["h2"]))
#     snap = [
#         ["Field", "Value"],
#         ["Domain",            _safe(ui.get("domain", "—"))],
#         ["Idea",              _safe((ui.get("description", "—") or "")[:200])],
#         ["Company Age",       f"{ui.get('company_age', '—')} years"],
#         ["Founders",          str(ui.get("founder_count", "—"))],
#         ["Employees",         str(ui.get("employees", "—"))],
#         ["Funding Rounds",    str(ui.get("funding_rounds", "—"))],
#         ["Avg Funding/Round", f"${ui.get('funding_per_round', 0):,.0f}"],
#         ["Investors",         str(ui.get("investor_count", "—"))],
#     ]
#     t = Table(snap, colWidths=[2.2*inch, 4.8*inch])
#     t.setStyle(_base_table_style())
#     story.append(t)
#     story.append(Spacer(1, 0.15*inch))

#     # ────────────────────────────────────────
#     # 2. ML PREDICTION RESULTS
#     # ────────────────────────────────────────
#     story.append(Paragraph("2. ML Prediction Results", st["h2"]))
#     classification = ml.get("classification", "—")
#     sp        = ml.get("success_probability", 0) * 100
#     risk_lvl  = ml.get("risk_level", "—")
#     pred_fund = ml.get("predicted_funding_usd", 0) or 0
#     probs     = ml.get("probabilities", {})

#     tag_style = (
#         st["tag_green"]  if classification == "Success" else
#         st["tag_red"]    if classification == "Failure" else
#         st["tag_yellow"]
#     )
#     story.append(Paragraph(f"Classification: {classification}", tag_style))
#     story.append(Spacer(1, 0.05*inch))

#     ml_data = [
#         ["Metric", "Value"],
#         ["Success Probability",    f"{sp:.1f}%"],
#         ["Failure Probability",    f"{probs.get('failure', 0)*100:.1f}%"],
#         ["Uncertain Probability",  f"{probs.get('uncertain', 0)*100:.1f}%"],
#         ["Risk Level",             str(risk_lvl)],
#         ["Predicted Next Funding", f"${pred_fund:,.2f}" if pred_fund else "N/A"],
#     ]
#     mt = Table(ml_data, colWidths=[3*inch, 4*inch])
#     mt.setStyle(_base_table_style())
#     story.append(mt)
#     story.append(Spacer(1, 0.15*inch))

#     # ────────────────────────────────────────
#     # 3. RISK FACTORS
#     # ────────────────────────────────────────
#     story.append(Paragraph("3. Risk Factors", st["h2"]))
#     if risks:
#         risk_data = [["#", "Risk Factor"]]
#         for i, r in enumerate(risks, 1):
#             risk_data.append([str(i), _safe(str(r))])
#         rt = Table(risk_data, colWidths=[0.5*inch, 6.5*inch])
#         rt.setStyle(_base_table_style(
#             header_color=RED,
#             row_colors=[colors.HexColor("#fff5f5"), WHITE],
#             grid_color="#fecaca",
#         ))
#         story.append(rt)
#     else:
#         story.append(Paragraph("No specific risk factors identified.", st["small"]))
#     story.append(Spacer(1, 0.15*inch))

#     # ────────────────────────────────────────
#     # 4. COMPETITOR ANALYSIS
#     # ────────────────────────────────────────
#     story.append(Paragraph("4. Competitor Analysis", st["h2"]))
#     if competitors:
#         # Use Paragraph() in cells so long text wraps properly
#         comp_data = [["#", Paragraph("<b>Competitor / Intelligence</b>", st["body"])]]
#         for i, c in enumerate(competitors, 1):
#             doc_text = c.get("document", c.get("name", c.get("summary", str(c))))
#             comp_data.append([
#                 str(i),
#                 Paragraph(_safe(str(doc_text)[:400]), st["body"]),
#             ])
#         ct = Table(comp_data, colWidths=[0.5*inch, 6.5*inch])
#         ct.setStyle(_base_table_style())
#         story.append(ct)
#     else:
#         story.append(Paragraph("No competitor data available.", st["small"]))
#     story.append(Spacer(1, 0.15*inch))

#     # ────────────────────────────────────────
#     # 5. TEAM HIERARCHY & ORG STRUCTURE
#     # ────────────────────────────────────────
#     story.append(Paragraph("5. Team Hierarchy & Org Structure", st["h2"]))
#     story.append(Paragraph(
#         f"<b>CEO / Founder:</b> {_safe(hierarchy.get('ceo_title', 'CEO'))}  •  "
#         f"<b>Total Employees:</b> {hierarchy.get('total_employees', '—')}",
#         st["body"],
#     ))

#     depts = hierarchy.get("departments", [])
#     if depts:
#         dept_data = [["Department", "Headcount", "Key Roles", "Skills Needed"]]
#         for d in depts:
#             roles_text  = ", ".join(
#         r["title"] if isinstance(r, dict) else str(r)
#          for r in d.get("roles", [])
#         )
#         skills_text = ", ".join(
#          s if isinstance(s, str) else str(s)
#          for s in d.get("skills_needed", [])
#              )
#             dept_data.append([
#                 _safe(d.get("name", "")),
#                 str(d.get("headcount", "")),
#                 Paragraph(_safe(roles_text),  st["small"]),
#                 Paragraph(_safe(skills_text), st["small"]),
#             ])
#         dt = Table(dept_data, colWidths=[1.4*inch, 0.8*inch, 2.5*inch, 2.3*inch])
#         dt.setStyle(_base_table_style())
#         story.append(dt)

#     gaps = hierarchy.get("hiring_gaps", [])
#     if gaps:
#         story.append(Spacer(1, 0.08*inch))
#         story.append(Paragraph(
#             "<b>Hiring Gaps:</b> " + ", ".join(_safe(g) for g in gaps),
#             st["body"],
#         ))

#     next_hires = hierarchy.get("recommended_next_hires", [])
#     if next_hires:
#         story.append(Paragraph("Recommended Next Hires:", st["h3"]))
#         nh_data = [["Role", "Priority", "Reason"]]
#         for h in next_hires:
#             nh_data.append([
#                 _safe(h.get("role", "")),
#                 _safe(h.get("priority", "")),
#                 Paragraph(_safe(h.get("reason", "")), st["small"]),
#             ])
#         nht = Table(nh_data, colWidths=[2*inch, 1*inch, 4*inch])
#         nht.setStyle(_base_table_style(
#             header_color=GREEN,
#             row_colors=[colors.HexColor("#f0fdf4"), WHITE],
#             grid_color="#bbf7d0",
#         ))
#         story.append(nht)

#     insight = hierarchy.get("org_insight", "")
#     if insight:
#         story.append(Spacer(1, 0.08*inch))
#         story.append(Paragraph(f"<i>{_safe(insight)}</i>", st["small"]))

#     story.append(Spacer(1, 0.15*inch))

#     # ────────────────────────────────────────
#     # 6. HIRING GUIDE
#     # ────────────────────────────────────────
#     if hiring_guide:
#         story.append(PageBreak())
#         story.append(Paragraph("6. Hiring Guide & Role Profiles", st["h2"]))
#         story.append(_divider())

#         # 6a. Hiring sequence
#         hiring_sequence = hiring_guide.get("hiring_sequence", [])
#         if hiring_sequence:
#             story.append(Paragraph("Recommended Hiring Sequence", st["h3"]))
#             seq_data = [["Order", "Role", "Rationale"]]
#             for s in hiring_sequence:
#                 seq_data.append([
#                     str(s.get("order", "")),
#                     _safe(s.get("role", "")),
#                     Paragraph(_safe(s.get("rationale", "")), st["small"]),
#                 ])
#             seq_t = Table(seq_data, colWidths=[0.6*inch, 2*inch, 4.4*inch])
#             seq_t.setStyle(_base_table_style())
#             story.append(seq_t)
#             story.append(Spacer(1, 0.12*inch))

#         # 6b. Individual hiring profiles
#         profiles = hiring_guide.get("hiring_profiles", [])
#         for idx, profile in enumerate(profiles, 1):
#             priority = profile.get("priority", "")
#             priority_color = RED if priority == "High" else (YELLOW if priority == "Medium" else GREEN)

#             story.append(Paragraph(
#                 f"Profile {idx}: {_safe(profile.get('role', 'Unknown Role'))}",
#                 st["h3"],
#             ))

#             # Summary row
#             exp = _safe(str(profile.get("experience_years", "—")))
#             summary_data = [
#                 ["Department", "Seniority", "Experience", "Priority", "Salary Range"],
#                 [
#                     _safe(profile.get("department", "—")),
#                     _safe(profile.get("seniority", "—")),
#                     exp + " yrs",
#                     _safe(priority),
#                     _safe(profile.get("salary_range", "—")),
#                 ],
#             ]
#             sum_t = Table(summary_data, colWidths=[1.4*inch, 1*inch, 1*inch, 0.9*inch, 2.7*inch])
#             sum_t.setStyle(TableStyle([
#                 ("BACKGROUND",    (0, 0), (-1, 0), priority_color),
#                 ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
#                 ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
#                 ("FONTSIZE",      (0, 0), (-1,-1), 8),
#                 ("BACKGROUND",    (0, 1), (-1, 1), LIGHT_BG),
#                 ("GRID",          (0, 0), (-1,-1), 0.4, colors.HexColor("#e2e8f0")),
#                 ("LEFTPADDING",   (0, 0), (-1,-1), 6),
#                 ("TOPPADDING",    (0, 0), (-1,-1), 4),
#                 ("BOTTOMPADDING", (0, 0), (-1,-1), 4),
#                 ("VALIGN",        (0, 0), (-1,-1), "TOP"),
#             ]))
#             story.append(sum_t)
#             story.append(Spacer(1, 0.06*inch))

#             why = profile.get("why_critical", "")
#             if why:
#                 story.append(Paragraph(f"<b>Why Critical:</b> {_safe(why)}", st["body"]))

#             must = profile.get("must_have_skills", [])
#             if must:
#                 story.append(Paragraph(
#                     "<b>Must-Have Skills:</b> " + " • ".join(_safe(s) for s in must),
#                     st["body"],
#                 ))

#             nice = profile.get("nice_to_have_skills", [])
#             if nice:
#                 story.append(Paragraph(
#                     "<b>Nice to Have:</b> " + " • ".join(_safe(s) for s in nice),
#                     st["small"],
#                 ))

#             quals = profile.get("qualifications", [])
#             if quals:
#                 story.append(Paragraph(
#                     "<b>Qualifications:</b> " + " | ".join(_safe(q) for q in quals),
#                     st["body"],
#                 ))

#             responsibilities = profile.get("key_responsibilities", [])
#             if responsibilities:
#                 story.append(Paragraph("<b>Key Responsibilities:</b>", st["body"]))
#                 for r in responsibilities:
#                     story.append(Paragraph(f"&nbsp;&nbsp;• {_safe(r)}", st["body"]))

#             signals = profile.get("interview_signals", [])
#             if signals:
#                 story.append(Paragraph(
#                     "<b>Interview Signals:</b> " + " | ".join(_safe(s) for s in signals),
#                     st["small"],
#                 ))

#             if idx < len(profiles):
#                 story.append(_section_divider())

#         # 6c. Culture fit + onboarding
#         culture = hiring_guide.get("culture_fit_signals", [])
#         if culture:
#             story.append(Spacer(1, 0.1*inch))
#             story.append(Paragraph("Culture Fit Signals", st["h3"]))
#             for c in culture:
#                 story.append(Paragraph(f"&#9733;&nbsp; {_safe(c)}", st["body"]))

#         onboarding = hiring_guide.get("onboarding_tips", "")
#         if onboarding:
#             story.append(Spacer(1, 0.08*inch))
#             story.append(Paragraph("Onboarding Tips", st["h3"]))
#             story.append(Paragraph(_safe(onboarding), st["body"]))

#         story.append(Spacer(1, 0.15*inch))

#     # ────────────────────────────────────────
#     # 7. STRATEGIC ANALYSIS & 30-DAY ACTION PLAN
#     # ────────────────────────────────────────
#     story.append(PageBreak())
#     section_num = 7 if hiring_guide else 6
#     story.append(Paragraph(f"{section_num}. Strategic Analysis & 30-Day Action Plan", st["h2"]))
#     story.append(_divider())

#     if analysis:
#         for line in analysis.split("\n"):
#             line = line.strip()
#             if not line:
#                 story.append(Spacer(1, 0.05*inch))
#             elif line.startswith("**") and line.endswith("**"):
#                 story.append(Paragraph(_safe(line.replace("**", "")), st["h3"]))
#             elif line.startswith("### "):
#                 story.append(Paragraph(_safe(line[4:]), st["h3"]))
#             elif line.startswith("## "):
#                 story.append(Paragraph(_safe(line[3:]), st["h2"]))
#             elif line.startswith("# "):
#                 story.append(Paragraph(_safe(line[2:]), st["h1"]))
#             elif line.startswith("- ") or line.startswith("* "):
#                 story.append(Paragraph(f"• {_safe(line[2:])}", st["body"]))
#             else:
#                 story.append(Paragraph(_safe(line), st["body"]))
#     else:
#         story.append(Paragraph("Strategic analysis not available.", st["small"]))

#     # ────────────────────────────────────────
#     # FOOTER
#     # ────────────────────────────────────────
#     story.append(Spacer(1, 0.3*inch))
#     story.append(_divider())
#     story.append(Paragraph(
#         f"Generated by BizGenius  •  {datetime.now().strftime('%Y-%m-%d %H:%M')}  •  Confidential",
#         st["small"],
#     ))

#     doc.build(story)
#     buf.seek(0)
#     return buf

"""
BizGenius FastAPI Backend - Report Service
Fully corrected version:
  - Fixed IndentationError in competitors block
  - Removed invalid WORDWRAP TableStyle command
  - Added VALIGN TOP everywhere
  - Wrapped long cell text in Paragraph() for auto-wrap
  - Safe HTML escaping throughout analysis section
  - Fixed roles/skills_needed handling for dict and str items
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER


# ── Color palette ──────────────────────────────────────────────
PURPLE  = colors.HexColor("#7c6bff")
DARK_BG = colors.HexColor("#0d0d24")
LIGHT_BG = colors.HexColor("#f8f7ff")
GREEN   = colors.HexColor("#34d399")
RED     = colors.HexColor("#f87171")
YELLOW  = colors.HexColor("#fbbf24")
GRAY    = colors.HexColor("#64748b")
WHITE   = colors.white
BLACK   = colors.HexColor("#1e1b4b")
ORANGE  = colors.HexColor("#fb923c")


def _styles():
    s = getSampleStyleSheet()

    h1 = ParagraphStyle("H1", fontSize=22, fontName="Helvetica-Bold",
                         textColor=PURPLE, spaceAfter=6)
    h2 = ParagraphStyle("H2", fontSize=15, fontName="Helvetica-Bold",
                         textColor=BLACK, spaceBefore=14, spaceAfter=4)
    h3 = ParagraphStyle("H3", fontSize=12, fontName="Helvetica-Bold",
                         textColor=PURPLE, spaceBefore=8, spaceAfter=3)
    h4 = ParagraphStyle("H4", fontSize=11, fontName="Helvetica-Bold",
                         textColor=BLACK, spaceBefore=6, spaceAfter=2)
    body   = ParagraphStyle("Body",   fontName="Helvetica", fontSize=10,
                             textColor=BLACK, leading=15, spaceAfter=4)
    small  = ParagraphStyle("Small",  fontName="Helvetica", fontSize=9,
                             textColor=GRAY, leading=13)
    center = ParagraphStyle("Center", fontName="Helvetica", fontSize=10,
                             textColor=BLACK, alignment=TA_CENTER)
    tag_green  = ParagraphStyle("TagG", fontName="Helvetica-Bold", fontSize=10, textColor=GREEN)
    tag_red    = ParagraphStyle("TagR", fontName="Helvetica-Bold", fontSize=10, textColor=RED)
    tag_yellow = ParagraphStyle("TagY", fontName="Helvetica-Bold", fontSize=10, textColor=YELLOW)
    tag_orange = ParagraphStyle("TagO", fontName="Helvetica-Bold", fontSize=10, textColor=ORANGE)

    return dict(h1=h1, h2=h2, h3=h3, h4=h4, body=body, small=small,
                center=center, tag_green=tag_green, tag_red=tag_red,
                tag_yellow=tag_yellow, tag_orange=tag_orange)


def _divider():
    return HRFlowable(width="100%", thickness=1, color=PURPLE, spaceAfter=8, spaceBefore=8)


def _section_divider():
    return HRFlowable(width="100%", thickness=0.5, color=GRAY, spaceAfter=6, spaceBefore=6)


def _safe(text: str) -> str:
    """Escape HTML special chars so ReportLab Paragraph doesn't choke."""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))


def _role_title(r) -> str:
    """Extract a display string from a role that may be a dict or a plain string."""
    if isinstance(r, dict):
        return r.get("title", str(r))
    return str(r)


def _skill_str(s) -> str:
    """Ensure a skill entry is always a plain string."""
    return s if isinstance(s, str) else str(s)


# ── Shared TableStyle helper ────────────────────────────────────
def _base_table_style(header_color=PURPLE, row_colors=None, grid_color="#e2e8f0"):
    if row_colors is None:
        row_colors = [LIGHT_BG, WHITE]
    return TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  header_color),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), row_colors),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor(grid_color)),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ])


# ════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ════════════════════════════════════════════════════════════════
def generate_pdf_report(data: dict) -> BytesIO:
    ui           = data["user_input"]
    ml           = data["ml_results"]
    analysis     = data.get("analysis", "")
    competitors  = data.get("competitors", [])
    hierarchy    = data.get("hierarchy", {})
    risks        = data.get("probable_risks", [])
    hiring_guide = data.get("hiring_guide", {})

    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.75*inch, rightMargin=0.75*inch,
        topMargin=0.75*inch,  bottomMargin=0.75*inch,
    )
    st    = _styles()
    story = []

    # ────────────────────────────────────────
    # COVER
    # ────────────────────────────────────────
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("BizGenius Startup Intelligence Report", st["h1"]))
    story.append(Paragraph(
        f"<b>Domain:</b> {_safe(ui.get('domain', ''))}  •  "
        f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y %H:%M')}",
        st["small"],
    ))
    story.append(_divider())

    # ────────────────────────────────────────
    # 1. STARTUP SNAPSHOT
    # ────────────────────────────────────────
    story.append(Paragraph("1. Startup Snapshot", st["h2"]))
    snap = [
        ["Field", "Value"],
        ["Domain",            _safe(ui.get("domain", "—"))],
        ["Idea",              _safe((ui.get("description", "—") or "")[:200])],
        ["Company Age",       f"{ui.get('company_age', '—')} years"],
        ["Founders",          str(ui.get("founder_count", "—"))],
        ["Employees",         str(ui.get("employees", "—"))],
        ["Funding Rounds",    str(ui.get("funding_rounds", "—"))],
        ["Avg Funding/Round", f"${ui.get('funding_per_round', 0):,.0f}"],
        ["Investors",         str(ui.get("investor_count", "—"))],
    ]
    t = Table(snap, colWidths=[2.2*inch, 4.8*inch])
    t.setStyle(_base_table_style())
    story.append(t)
    story.append(Spacer(1, 0.15*inch))

    # ────────────────────────────────────────
    # 2. ML PREDICTION RESULTS
    # ────────────────────────────────────────
    story.append(Paragraph("2. ML Prediction Results", st["h2"]))
    classification = ml.get("classification", "—")
    sp        = ml.get("success_probability", 0) * 100
    risk_lvl  = ml.get("risk_level", "—")
    pred_fund = ml.get("predicted_funding_usd", 0) or 0
    probs     = ml.get("probabilities", {})

    tag_style = (
        st["tag_green"]  if classification == "Success" else
        st["tag_red"]    if classification == "Failure" else
        st["tag_yellow"]
    )
    story.append(Paragraph(f"Classification: {classification}", tag_style))
    story.append(Spacer(1, 0.05*inch))

    ml_data = [
        ["Metric", "Value"],
        ["Success Probability",    f"{sp:.1f}%"],
        ["Failure Probability",    f"{probs.get('failure', 0)*100:.1f}%"],
        ["Uncertain Probability",  f"{probs.get('uncertain', 0)*100:.1f}%"],
        ["Risk Level",             str(risk_lvl)],
        ["Predicted Next Funding", f"${pred_fund:,.2f}" if pred_fund else "N/A"],
    ]
    mt = Table(ml_data, colWidths=[3*inch, 4*inch])
    mt.setStyle(_base_table_style())
    story.append(mt)
    story.append(Spacer(1, 0.15*inch))

    # ────────────────────────────────────────
    # 3. RISK FACTORS
    # ────────────────────────────────────────
    story.append(Paragraph("3. Risk Factors", st["h2"]))
    if risks:
        risk_data = [["#", "Risk Factor"]]
        for i, r in enumerate(risks, 1):
            risk_data.append([str(i), _safe(str(r))])
        rt = Table(risk_data, colWidths=[0.5*inch, 6.5*inch])
        rt.setStyle(_base_table_style(
            header_color=RED,
            row_colors=[colors.HexColor("#fff5f5"), WHITE],
            grid_color="#fecaca",
        ))
        story.append(rt)
    else:
        story.append(Paragraph("No specific risk factors identified.", st["small"]))
    story.append(Spacer(1, 0.15*inch))

    # ────────────────────────────────────────
    # 4. COMPETITOR ANALYSIS
    # ────────────────────────────────────────
    story.append(Paragraph("4. Competitor Analysis", st["h2"]))
    if competitors:
        comp_data = [["#", Paragraph("<b>Competitor / Intelligence</b>", st["body"])]]
        for i, c in enumerate(competitors, 1):
            doc_text = c.get("document", c.get("name", c.get("summary", str(c))))
            comp_data.append([
                str(i),
                Paragraph(_safe(str(doc_text)[:400]), st["body"]),
            ])
        ct = Table(comp_data, colWidths=[0.5*inch, 6.5*inch])
        ct.setStyle(_base_table_style())
        story.append(ct)
    else:
        story.append(Paragraph("No competitor data available.", st["small"]))
    story.append(Spacer(1, 0.15*inch))

    # ────────────────────────────────────────
    # 5. TEAM HIERARCHY & ORG STRUCTURE
    # ────────────────────────────────────────
    story.append(Paragraph("5. Team Hierarchy & Org Structure", st["h2"]))
    story.append(Paragraph(
        f"<b>CEO / Founder:</b> {_safe(hierarchy.get('ceo_title', 'CEO'))}  •  "
        f"<b>Total Employees:</b> {hierarchy.get('total_employees', '—')}",
        st["body"],
    ))

    depts = hierarchy.get("departments", [])
    if depts:
        dept_data = [["Department", "Headcount", "Key Roles", "Skills Needed"]]
        for d in depts:
            # roles may be list of dicts {title, count, expertise} or plain strings
            roles_text = ", ".join(
                _role_title(r) for r in d.get("roles", [])
            )
            # skills_needed may not exist (new schema uses head_expertise per dept)
            skills_list = d.get("skills_needed") or d.get("head_expertise") or []
            skills_text = ", ".join(_skill_str(s) for s in skills_list)

            dept_data.append([
                _safe(d.get("name", "")),
                str(d.get("headcount", "")),
                Paragraph(_safe(roles_text),  st["small"]),
                Paragraph(_safe(skills_text), st["small"]),
            ])
        dt = Table(dept_data, colWidths=[1.4*inch, 0.8*inch, 2.5*inch, 2.3*inch])
        dt.setStyle(_base_table_style())
        story.append(dt)

    gaps = hierarchy.get("hiring_gaps", [])
    if gaps:
        story.append(Spacer(1, 0.08*inch))
        story.append(Paragraph(
            "<b>Hiring Gaps:</b> " + ", ".join(_safe(g) for g in gaps),
            st["body"],
        ))

    next_hires = hierarchy.get("recommended_next_hires", [])
    if next_hires:
        story.append(Paragraph("Recommended Next Hires:", st["h3"]))
        nh_data = [["Role", "Priority", "Reason"]]
        for h in next_hires:
            nh_data.append([
                _safe(h.get("role", "")),
                _safe(h.get("priority", "")),
                Paragraph(_safe(h.get("reason", "")), st["small"]),
            ])
        nht = Table(nh_data, colWidths=[2*inch, 1*inch, 4*inch])
        nht.setStyle(_base_table_style(
            header_color=GREEN,
            row_colors=[colors.HexColor("#f0fdf4"), WHITE],
            grid_color="#bbf7d0",
        ))
        story.append(nht)

    insight = hierarchy.get("org_insight", "")
    if insight:
        story.append(Spacer(1, 0.08*inch))
        story.append(Paragraph(f"<i>{_safe(insight)}</i>", st["small"]))

    story.append(Spacer(1, 0.15*inch))

    # ────────────────────────────────────────
    # 6. HIRING GUIDE
    # ────────────────────────────────────────
    if hiring_guide:
        story.append(PageBreak())
        story.append(Paragraph("6. Hiring Guide & Role Profiles", st["h2"]))
        story.append(_divider())

        # 6a. Hiring sequence
        hiring_sequence = hiring_guide.get("hiring_sequence", [])
        if hiring_sequence:
            story.append(Paragraph("Recommended Hiring Sequence", st["h3"]))
            seq_data = [["Order", "Role", "Rationale"]]
            for s in hiring_sequence:
                seq_data.append([
                    str(s.get("order", "")),
                    _safe(s.get("role", "")),
                    Paragraph(_safe(s.get("rationale", "")), st["small"]),
                ])
            seq_t = Table(seq_data, colWidths=[0.6*inch, 2*inch, 4.4*inch])
            seq_t.setStyle(_base_table_style())
            story.append(seq_t)
            story.append(Spacer(1, 0.12*inch))

        # 6b. Individual hiring profiles
        profiles = hiring_guide.get("hiring_profiles", [])
        for idx, profile in enumerate(profiles, 1):
            priority = profile.get("priority", "")
            priority_color = RED if priority == "High" else (YELLOW if priority == "Medium" else GREEN)

            story.append(Paragraph(
                f"Profile {idx}: {_safe(profile.get('role', 'Unknown Role'))}",
                st["h3"],
            ))

            exp = _safe(str(profile.get("experience_years", "—")))
            summary_data = [
                ["Department", "Seniority", "Experience", "Priority", "Salary Range"],
                [
                    _safe(profile.get("department", "—")),
                    _safe(profile.get("seniority", "—")),
                    exp + " yrs",
                    _safe(priority),
                    _safe(profile.get("salary_range", "—")),
                ],
            ]
            sum_t = Table(summary_data, colWidths=[1.4*inch, 1*inch, 1*inch, 0.9*inch, 2.7*inch])
            sum_t.setStyle(TableStyle([
                ("BACKGROUND",    (0, 0), (-1, 0), priority_color),
                ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
                ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE",      (0, 0), (-1, -1), 8),
                ("BACKGROUND",    (0, 1), (-1, 1), LIGHT_BG),
                ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#e2e8f0")),
                ("LEFTPADDING",   (0, 0), (-1, -1), 6),
                ("TOPPADDING",    (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ]))
            story.append(sum_t)
            story.append(Spacer(1, 0.06*inch))

            why = profile.get("why_critical", "")
            if why:
                story.append(Paragraph(f"<b>Why Critical:</b> {_safe(why)}", st["body"]))

            must = profile.get("must_have_skills", [])
            if must:
                story.append(Paragraph(
                    "<b>Must-Have Skills:</b> " + " • ".join(_safe(s) for s in must),
                    st["body"],
                ))

            nice = profile.get("nice_to_have_skills", [])
            if nice:
                story.append(Paragraph(
                    "<b>Nice to Have:</b> " + " • ".join(_safe(s) for s in nice),
                    st["small"],
                ))

            quals = profile.get("qualifications", [])
            if quals:
                story.append(Paragraph(
                    "<b>Qualifications:</b> " + " | ".join(_safe(q) for q in quals),
                    st["body"],
                ))

            responsibilities = profile.get("key_responsibilities", [])
            if responsibilities:
                story.append(Paragraph("<b>Key Responsibilities:</b>", st["body"]))
                for r in responsibilities:
                    story.append(Paragraph(f"&nbsp;&nbsp;• {_safe(r)}", st["body"]))

            signals = profile.get("interview_signals", [])
            if signals:
                story.append(Paragraph(
                    "<b>Interview Signals:</b> " + " | ".join(_safe(s) for s in signals),
                    st["small"],
                ))

            if idx < len(profiles):
                story.append(_section_divider())

        # 6c. Culture fit + onboarding
        culture = hiring_guide.get("culture_fit_signals", [])
        if culture:
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph("Culture Fit Signals", st["h3"]))
            for c in culture:
                story.append(Paragraph(f"&#9733;&nbsp; {_safe(c)}", st["body"]))

        onboarding = hiring_guide.get("onboarding_tips", "")
        if onboarding:
            story.append(Spacer(1, 0.08*inch))
            story.append(Paragraph("Onboarding Tips", st["h3"]))
            story.append(Paragraph(_safe(onboarding), st["body"]))

        story.append(Spacer(1, 0.15*inch))

    # ────────────────────────────────────────
    # 7. STRATEGIC ANALYSIS & 30-DAY ACTION PLAN
    # ────────────────────────────────────────
    story.append(PageBreak())
    section_num = 7 if hiring_guide else 6
    story.append(Paragraph(f"{section_num}. Strategic Analysis & 30-Day Action Plan", st["h2"]))
    story.append(_divider())

    if analysis:
        for line in analysis.split("\n"):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.05*inch))
            elif line.startswith("**") and line.endswith("**"):
                story.append(Paragraph(_safe(line.replace("**", "")), st["h3"]))
            elif line.startswith("### "):
                story.append(Paragraph(_safe(line[4:]), st["h3"]))
            elif line.startswith("## "):
                story.append(Paragraph(_safe(line[3:]), st["h2"]))
            elif line.startswith("# "):
                story.append(Paragraph(_safe(line[2:]), st["h1"]))
            elif line.startswith("- ") or line.startswith("* "):
                story.append(Paragraph(f"• {_safe(line[2:])}", st["body"]))
            else:
                story.append(Paragraph(_safe(line), st["body"]))
    else:
        story.append(Paragraph("Strategic analysis not available.", st["small"]))

    # ────────────────────────────────────────
    # FOOTER
    # ────────────────────────────────────────
    story.append(Spacer(1, 0.3*inch))
    story.append(_divider())
    story.append(Paragraph(
        f"Generated by BizGenius  •  {datetime.now().strftime('%Y-%m-%d %H:%M')}  •  Confidential",
        st["small"],
    ))

    doc.build(story)
    buf.seek(0)
    return buf