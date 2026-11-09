# Python Things

Small Python scripts. So far there's one: an email-to-Obsidian exporter.

## Obsidian Email Scraper

`ObsidianEmailScraper.py` logs into your email inbox and copies every email into a single Markdown note for [Obsidian](https://obsidian.md) (a notes app that stores notes as plain text files). Each email becomes a section with its subject as the heading, then who sent it, the date and the message text:

```markdown
## Your order has shipped
- From: Shop <orders@example.com>
- Date: Mon, 3 Nov 2026 09:12:00 +1100

Hi, your parcel is on its way...
```

### Before you run it, know that it:

- **Reads your whole inbox.** On a big mailbox this is slow and makes a very large note. Try it on a test account, or a small folder, first.
- **Overwrites the note each time.** It rewrites `extracted_emails.md` from scratch on every run.
- **Skips emails that have no plain-text part** (for example HTML-only newsletters).
- **Only reads.** It never deletes or changes your emails.

### What you need

- Python 3 (on a Mac, check with `python3 --version`). The script only uses Python's built-in modules, so there's nothing to install.
- Your email provider's **IMAP server** address, for example `imap.gmail.com` for Gmail or `outlook.office365.com` for Outlook.
- An **app password**, not your normal password. Most providers (Gmail, Outlook, iCloud) require one for scripts like this. Search "<your provider> app password" to create one; you need two-step verification switched on.

### How to run it

1. Download this repository (green **Code** button › **Download ZIP**) and unzip it.
2. Open `ObsidianEmailScraper.py` in a text editor and fill in the settings at the top:
   ```python
   EMAIL = 'you@gmail.com'
   PASSWORD = 'your-app-password'
   IMAP_SERVER = 'imap.gmail.com'
   OBSIDIAN_VAULT_PATH = '/Users/you/Documents/MyVault'   # your Obsidian vault folder
   ```
3. In Terminal, go to the folder and run it:
   ```bash
   cd path/to/PythonThings
   python3 ObsidianEmailScraper.py
   ```
4. Open Obsidian: the note `extracted_emails.md` appears in your vault.

> **Keep your password private.** Don't commit the file to GitHub once your password is in it. A safer approach is to read it from an environment variable instead, for example `PASSWORD = os.environ['EMAIL_PASSWORD']`.

### Ideas for next steps

- Add error messages for a wrong password or server.
- Fetch only recent or unread emails instead of everything (change `'ALL'` in `mail.search` to `'UNSEEN'`).
- Run it on a schedule, for example with a cron job on a Mac or Linux.
