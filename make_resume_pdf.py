#!/usr/bin/env python3
"""Build resume.pdf (public version: phone stripped, email removed 2026-10-25 at Adam's direction)
matching the site resume section. Requires fpdf2 (pip install fpdf2)."""
import os

from fpdf import FPDF

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resume.pdf")

pdf = FPDF(format="Letter", unit="mm")
pdf.set_auto_page_break(auto=True, margin=16)
pdf.set_margins(18, 16, 18)
pdf.add_page()

def name():
    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(20, 24, 34)
    pdf.cell(0, 9, "Adam Joseph Laloge", new_x="LMARGIN", new_y="NEXT")

def headline():
    pdf.set_font("helvetica", "", 11)
    pdf.set_text_color(70, 80, 100)
    pdf.cell(0, 6, "UI/UX Engineer | Human-Centered AI Systems", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 5, "West Harrison, Indiana | github.com/AStellarScene", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

def section(title):
    pdf.ln(3)
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(15, 110, 95)
    pdf.cell(0, 6, title.upper(), new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(180, 188, 200)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(2)

def body(text, size=10.5):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("helvetica", "", size)
    pdf.set_text_color(35, 40, 52)
    pdf.multi_cell(0, 5.2, text)
    pdf.ln(1)

def job_head(text):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("helvetica", "B", 10.5)
    pdf.set_text_color(20, 24, 34)
    pdf.multi_cell(0, 5.2, text)

def bullet(text):
    pdf.set_font("helvetica", "", 10.5)
    pdf.set_text_color(35, 40, 52)
    pdf.set_x(pdf.l_margin)
    y = pdf.get_y()
    pdf.cell(5, 5.2, chr(183))
    pdf.set_xy(pdf.l_margin + 5, y)
    pdf.multi_cell(0, 5.2, text)

name()
headline()

section("Profile")
body("Engineering Test Technician and software developer in medical-device testing. Builds test software and automated test equipment, including technician-facing interfaces, backend code, embedded controllers, and AI agent workspaces. Uses moderated usability sessions and operator workflows to shape requirements. Finishing a B.S. in UX Design at WGU.")

section("Experience")
job_head("Baxter International, Inc. | Batesville, IN | 2025 - Present")
body("Engineering Test Technician", 10.5)
for b in [
    "Medical-device verification: Perform verification testing of medical devices under regulated requirements.",
    "PLM and issue management: Manage document control and validation data in PLM. Document product issues and escalate them to Engineering.",
    "Software development: Build test software, from the technician-facing interface through the backend.",
    "AI agent workflows: Build specialized AI agent workspaces that support automated testing and software development.",
    "Automated test equipment: Design, build, and validate automated test equipment for medical-device testing, including equipment with embedded controllers.",
    "Electrical and mechanical assembly: Perform electrical and mechanical assembly of projects according to engineering documentation.",
    "Innovation and hackathons: Contribute to invention disclosures and participate in hackathons.",
]:
    bullet(b)
pdf.ln(2)
job_head("Computer Solutions and Innovations, LLC | Versailles, IN | 2023 - 2024")
body("On-Site IT Support", 10.5)
bullet("Delivered in-person and remote support for hardware and software issues.")
bullet("Assisted with infrastructure planning, hardware asset management, purchasing, and system upgrades.")

section("Education")
bullet("WGU School of Business | B.S. User Experience Design, in progress (expected January 2027)")
bullet("Ivy Tech Community College | A.A.S. Software Development, May 2024, Magna Cum Laude, 3.9 GPA")

section("Certifications")
bullet("AWS Certified Cloud Practitioner (2023)")
bullet("CompTIA Project+ (2024)")

section("Skills")
skills = [
    ("UX & Human Factors", "HMI design for test equipment; usability testing (moderated sessions with end users); heuristic evaluation (Nielsen's 10); wireframing and user flows; UI prototyping (Figma, Adobe Illustrator, Affinity Designer, Miro); user needs gathering and requirements definition; personas and journey maps; calibration procedure UX/UI design; user training and support for internal tools; systems analysis and design; W3C/WCAG, Material Design, and Apple Human Interface Guidelines."),
    ("Test, V&V & Reliability", "Medical device verification and validation; lifecycle testing (hospital beds, patient support systems); requirements traceability; failure investigation (reproduction, documentation, escalation); automated regression and unit testing; automated test equipment (ATE) engineering; modular test action libraries; safety system design; calibration methods; test data recording and analysis; technical documentation, spec writing, and validation documentation; PLM document control."),
    ("Software & Embedded", "Python; C#/.NET; C++; JavaScript; HTML/CSS; Rust; SQL and database design; Linux and Bash; Docker; WebSockets; Git/GitHub; code review and branching workflows; embedded microcontrollers; sensor integration; OpenCV; Agile/Scrum."),
    ("AI & Agentic Work", "GitHub Copilot agent architectures; AI agent workspaces; Retrieval-Augmented Generation (RAG); Model Context Protocol (MCP) and tool integrations; AI output evaluation, testing, and validation; natural language protocol ingestion; structured iterative prompting; AI assisted refactoring and debugging."),
]
for title, text in skills:
    job_head(title)
    body(text)

pdf.output(OUT)
print("wrote", OUT)
