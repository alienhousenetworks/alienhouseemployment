import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .services import export_employee_master_sheet


def sync_to_google_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )
    client = gspread.authorize(creds)

    sheet = client.open("Employee Master Sheet").sheet1
    sheet.clear()

    rows = export_employee_master_sheet()
    sheet.append_row(rows[0].keys())

    for row in rows:
        sheet.append_row(list(row.values()))

