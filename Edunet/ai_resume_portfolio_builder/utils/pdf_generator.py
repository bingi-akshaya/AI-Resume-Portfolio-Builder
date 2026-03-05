from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib import colors


def generate_pdf(filename, content, photo_url=None, qr_path=None):
    """Build a polished, Zety‑like PDF from resume lines.

    The first non‑blank line is treated as the name and rendered in a large
    font; the second line (if present) is contact info. If ``photo_url`` is
    provided we attempt to download it and display it alongside the name.
    Sections headed with "Header:" produce colored headers. Skills lists are
    rendered on a single line separated by commas instead of vertical bullets.

    ``qr_path`` (if given) is placed in the bottom right corner of the
    document.
    """

    # parse content into list and sections
    lines = [l for l in content if l is not None]
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="TitleName",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor="#00539C",
        spaceAfter=6,
    )
    contact_style = ParagraphStyle(
        name="Contact",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        spaceAfter=12,
    )
    section_header = ParagraphStyle(
        name="SectionHeader",
        parent=styles["Heading2"],
        backColor=colors.lightgrey,
        textColor="#003d73",
        spaceBefore=12,
        spaceAfter=6,
        leftIndent=0,
    )
    bullet = ParagraphStyle(
        name="Bullet",
        parent=styles["Normal"],
        leftIndent=12,
        bulletIndent=0,
        bulletFontName="Helvetica",
        fontSize=10,
    )

    pdf = SimpleDocTemplate(
        filename,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
    )
    elements = []

    # optional photo loading
    photo_path = None
    if photo_url:
        try:
            from urllib.request import urlopen
            import tempfile
            resp = urlopen(photo_url)
            data = resp.read()
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            temp.write(data)
            temp.flush()
            photo_path = temp.name
        except Exception:
            photo_path = None

    # render name/contact/photo header
    if lines:
        name_line = lines[0].strip()
        if name_line:
            elements.append(Paragraph(name_line, title_style))
        if photo_path:
            try:
                im = Image(photo_path, width=1.2 * inch, height=1.2 * inch)
                im.hAlign = "CENTER"
                elements.append(im)
            except Exception:
                pass
        if len(lines) > 1 and lines[1].strip():
            elements.append(Paragraph(lines[1], contact_style))
        elements.append(Spacer(1, 12))

    # we'll build a table for sidebar + main content in a second step
    body = lines[2:] if len(lines) > 2 else []

    # split into sections for later table construction
    sections = []
    i = 0
    while i < len(body):
        if not body[i].strip():
            i += 1
            continue
        if body[i].endswith(":"):
            header_text = body[i][:-1]
            i += 1
            items = []
            while i < len(body) and body[i].strip() and not body[i].endswith(":"):
                items.append(body[i])
                i += 1
            sections.append((header_text, items))
        else:
            sections.append((None, [body[i]]))
            i += 1

    # now construct two-column table: left = sidebar (photo, contact, skills, languages, etc.)
    sidebar_lines = []
    main_lines = []

    # copy contact again into sidebar
    if lines and len(lines) > 1 and lines[1].strip():
        sidebar_lines.append(lines[1].strip())
    # iterate sections and dispatch
    for hdr, items in sections:
        if hdr in ("Skills", "Languages", "Certifications", "Awards & Honors"):
            sidebar_lines.append(hdr + ":")
            for it in items:
                sidebar_lines.append(it)
        else:
            if hdr:
                main_lines.append(hdr + ":")
            for it in items:
                main_lines.append(it)
    # build sidebar paragraph list
    sidebar_parts = []
    for line in sidebar_lines:
        if line.endswith(":"):
            sidebar_parts.append(Paragraph(line[:-1], section_header))
        elif line.lstrip().startswith("- "):
            txt = line.lstrip()[2:]
            sidebar_parts.append(Paragraph(txt, bullet, bulletText="•"))
        else:
            sidebar_parts.append(Paragraph(line, styles["Normal"]))

    main_parts = []
    for line in main_lines:
        if line.endswith(":"):
            main_parts.append(Paragraph(line[:-1], section_header))
        elif line.lstrip().startswith("- "):
            txt = line.lstrip()[2:]
            main_parts.append(Paragraph(txt, bullet, bulletText="•"))
        else:
            main_parts.append(Paragraph(line, styles["Normal"]))

    # assemble table data
    data_table = [[sidebar_parts, main_parts]]
    table = Table(data_table, colWidths=[2.3 * inch, 3.7 * inch])
    table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(table)

    # attach QR if available
    if qr_path:
        try:
            im = Image(qr_path, width=1.2 * inch, height=1.2 * inch)
            im.hAlign = "RIGHT"
            elements.append(Spacer(1, 12))
            elements.append(im)
        except Exception:
            pass

    pdf.build(elements)

