import gspread
from oauth2client.service_account import ServiceAccountCredentials

def update_google_sheet(data_list):
    # Setup koneksi
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    # Pastikan nama spreadsheet SAMA PERSIS dengan yang di Google Drive
    sheet = client.open("xtrade-project").sheet1
    
    # Menambahkan baris tanpa perlu menangkap return value yang kompleks
    sheet.append_row(data_list)
    return True # Jika berhasil sampai sini, berarti sukses