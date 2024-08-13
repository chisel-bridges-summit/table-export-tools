# table-export-tools

This repo includes the tools used to export the sticky note collaborations done in Miro into an open source repo for sharing the output of Bridges Summit events.

# Miro Sticky Note Exporter
## Sticky Note Export Process
## export_sticky_notes.py

This Python script exports all sticky notes from every board in a Miro workspace using the Miro API v2. The script fetches all boards in the workspace, retrieves the sticky notes from each board, and saves them to a text file.

## Features

- Connects to Miro API v2 to retrieve boards and sticky notes.
- Uses a `.env` file to securely manage your Miro API token.

## Prerequisites

- Python 3.x
- `requests` library
- `python-dotenv` library

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/miro-sticky-note-exporter.git
cd miro-sticky-note-exporter
```

### 2. Install Required Packages

Make sure you have the required Python packages installed:

```bash
pip install requests python-dotenv
```

### 3. Obtain an OAuth Token from Miro

1. **Log in to Miro** and navigate to the [Miro Developer Portal](https://developers.miro.com/).
2. **Create a new app**:
   - Click on **Create new app**.
   - Provide the necessary details such as the app name and description.
   - Under **OAuth 2.0 settings**, set the redirect URL (e.g., `https://localhost` for local development).
3. **Generate OAuth Token**:
   - After creating the app, go to the **OAuth & Permissions** tab.
   - Click on **Get your OAuth token** to generate a personal access token for your app.
   - Copy the token.

### 4. Create a `.env` File

Create a `.env` file in the root directory of the project:

```plaintext
MIRO_API_TOKEN=your_miro_api_token_here
```

Replace `your_miro_api_token_here` with the OAuth token you obtained from Miro.

### 5. Update `.gitignore`

Ensure that your `.gitignore` file includes `.env` to prevent it from being committed to version control:

```plaintext
.env
```

### 6. Run the Script

Run the script to export all sticky notes:

```bash
python miro_sticky_note_exporter.py
```
