import imaplib
import email
from email.header import decode_header
import os

# Email credentials
EMAIL = 'your_email@example.com'
PASSWORD = 'your_password'
IMAP_SERVER = 'imap.example.com'

# Obsidian setup
OBSIDIAN_VAULT_PATH = '/path/to/your/vault'
NOTE_FILENAME = 'extracted_emails.md'

def connect_to_email_server():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    return mail

def fetch_emails(mail):
    mail.select('inbox')
    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()
    return email_ids

def extract_email_content(mail, email_id):
    status, msg_data = mail.fetch(email_id, '(RFC822)')
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding)
            from_ = msg.get('From')
            date = msg.get('Date')

            # Extract email body
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get('Content-Disposition'))
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == 'text/plain' and 'attachment' not in content_disposition:
                        return subject, from_, date, body
            else:
                body = msg.get_payload(decode=True).decode()
                return subject, from_, date, body
    return None

def write_to_obsidian(note_content):
    note_path = os.path.join(OBSIDIAN_VAULT_PATH, NOTE_FILENAME)
    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(note_content)

def main():
    mail = connect_to_email_server()
    email_ids = fetch_emails(mail)
    note_content = ''

    for email_id in email_ids:
        result = extract_email_content(mail, email_id)
        if result is None:   # e.g. an email with only HTML or attachments
            continue
        subject, from_, date, body = result
        if subject:
            note_content += f'## {subject}\n'
            note_content += f'- From: {from_}\n'
            note_content += f'- Date: {date}\n\n'
            note_content += f'{body}\n\n'

    write_to_obsidian(note_content)
    mail.logout()

if __name__ == '__main__':
    main()
