from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from datetime import date

styles = getSampleStyleSheet()
H1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=20, spaceAfter=10)
H2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=13, spaceBefore=10, spaceAfter=6)
Body = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=10.5, leading=14)
Small = ParagraphStyle('Small', parent=styles['BodyText'], fontSize=9, leading=12, textColor=colors.HexColor('#333333'))

PRODUCT = 'Test'
TIMELINE_DAYS = 45
BASE = 120000
DISCOUNT = 15000
TOTAL = BASE - DISCOUNT

payments = [
  ('Milestone 1 — Kickoff', 'Day 1', '₹30,000'),
  ('Milestone 2 — Core build', 'Day 14', '₹25,000'),
  ('Milestone 3 — Beta + QA', 'Day 28', '₹25,000'),
  ('Milestone 4 — Final delivery + handover', 'Day 45', '₹25,000'),
]


def dash_list(lines):
  # Avoid bullet symbols (which can render as black boxes in some viewers)
  return Paragraph('<br/>'.join([f'- {l}' for l in lines]), Body)


def build_proposal(out_path: str):
  doc = SimpleDocTemplate(out_path, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
  story = []

  story.append(Paragraph(f'Project Proposal — {PRODUCT}', H1))
  story.append(Paragraph(f'Date: {date.today().isoformat()}', Small))
  story.append(Spacer(1, 12))

  story.append(Paragraph('Commercial Summary', H2))
  t = Table([
    ['Product', PRODUCT],
    ['Timeline', f'{TIMELINE_DAYS} days'],
    ['Price (base)', f'₹{BASE:,.0f}'],
    ['Discount', f'₹{DISCOUNT:,.0f}'],
    ['Total', f'₹{TOTAL:,.0f}'],
  ], colWidths=[5*cm, 10*cm])
  t.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor('#999999')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#cccccc')),
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f2f5ff')),
    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
  ]))
  story.append(t)
  story.append(Spacer(1, 10))

  story.append(Paragraph('Payment Schedule (with due dates)', H2))
  pt = Table([
    ['Milestone', 'Due', 'Amount'],
    *payments,
  ], colWidths=[9*cm, 3*cm, 3*cm])
  pt.setStyle(TableStyle([
    # Light header (avoid dark blocks)
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f2f5ff')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#111827')),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor('#999999')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#cccccc')),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('ALIGN', (1,1), (2,-1), 'CENTER'),
  ]))
  story.append(pt)
  story.append(Spacer(1, 12))

  story.append(Paragraph('Overview', H2))
  story.append(Paragraph(
    'This proposal covers delivery of a psychometric assessment platform (“Test”) including assessment creation, user onboarding, scoring, reporting, and admin workflows. '
    'Delivery is planned over 45 days with milestone-based payments.',
    Body
  ))

  story.append(Paragraph('Scope & Deliverables', H2))
  story.append(dash_list([
    'Admin panel: create/edit tests, questions, sections, scoring rules, and schedules.',
    'Candidate flow: invite/login, take assessment, save progress, submit.',
    'Scoring engine: compute scores, normalize, and generate category-wise insights.',
    'Reports: candidate report + downloadable summary; admin analytics view.',
    'Deployment + handover: repository, environment setup, and runbook.',
  ]))

  story.append(Paragraph('Timeline (45 days)', H2))
  story.append(dash_list([
    'Day 1–14: Core architecture, database, admin scaffolding, basic candidate flow.',
    'Day 15–28: Scoring engine, report templates, analytics views, UX polish.',
    'Day 29–45: QA + fixes, deployment, documentation, and final handover.',
  ]))

  story.append(Paragraph('Assumptions', H2))
  story.append(dash_list([
    'Content (questions, categories, scoring logic) will be provided/approved during the first 2 weeks.',
  ]))

  story.append(Paragraph('Out of Scope', H2))
  story.append(dash_list([
    'Native mobile apps.',
    'Advanced proctoring / AI anti-cheat.',
    'Custom integrations beyond the agreed scope (unless added via change request).',
  ]))

  story.append(Paragraph('Support & Maintenance', H2))
  story.append(Paragraph(
    'Includes 30 days of post-delivery maintenance support. Additional support can be requested as needed.',
    Body
  ))

  story.append(Paragraph('Change Requests', H2))
  story.append(Paragraph('Any scope additions after sign-off will be estimated and billed separately, with timeline adjustments as needed.', Body))

  story.append(Spacer(1, 18))
  story.append(Paragraph('Acceptance', H2))
  story.append(Paragraph('Approved by: ______________________    Date: ____________', Body))

  doc.build(story)


def build_quote(out_path: str):
  doc = SimpleDocTemplate(out_path, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
  story = []
  story.append(Paragraph(f'Quotation — {PRODUCT}', H1))
  story.append(Paragraph(f'Date: {date.today().isoformat()}', Small))
  story.append(Spacer(1, 10))

  story.append(Paragraph(f'Total: ₹{TOTAL:,.0f}', Body))
  story.append(Paragraph(f'Timeline: {TIMELINE_DAYS} days', Body))
  story.append(Spacer(1, 8))

  story.append(Paragraph('Payment Schedule (due on milestones)', H2))
  pt = Table([
    ['Milestone', 'Due', 'Amount'],
    *payments,
  ], colWidths=[9*cm, 3*cm, 3*cm])
  pt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f2f5ff')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#111827')),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('BOX', (0,0), (-1,-1), 0.6, colors.HexColor('#999999')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#cccccc')),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('ALIGN', (1,1), (2,-1), 'CENTER'),
  ]))
  story.append(pt)
  story.append(Spacer(1, 10))

  story.append(Paragraph('Deliverables (summary)', H2))
  story.append(dash_list([
    'Admin panel to manage tests + questions + scoring',
    'Candidate assessment flow (start → submit)',
    'Scoring + basic reporting',
    'Deployment + documentation + handover',
  ]))

  story.append(Paragraph('Support & Maintenance', H2))
  story.append(Paragraph('Includes 30 days of post-delivery maintenance support. Additional support can be requested as needed.', Body))

  story.append(Spacer(1, 14))
  story.append(Paragraph('Approved by: ______________________    Date: ____________', Body))

  doc.build(story)


if __name__ == '__main__':
  build_proposal('/home/ubuntu/clawd/output/Test-Proposal-Formatted-v5.pdf')
  build_quote('/home/ubuntu/clawd/output/Test-Quote-Formatted-v5.pdf')
  print('ok')
