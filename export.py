import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


def export_to_excel(trades):
    df = pd.DataFrame(trades, columns=[
        "PnL", "Setup", "Note", "Timestamp"
    ])

    file_path = "trading_report.xlsx"
    df.to_excel(file_path, index=False)

    return file_path


def export_to_pdf(trades):
    file_path = "trading_report.pdf"
    pdf = SimpleDocTemplate(file_path)

    data = [["PnL", "Setup", "Note", "Timestamp"]] + list(trades)

    table = Table(data)

    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ])

    table.setStyle(style)

    pdf.build([table])

    return file_path