# Danphe Leaderboard Bot

A lightweight Discord bot for tracking and displaying team scores on a Google Sheet–backed leaderboard.  
“Danphe” (the national bird of Nepal) helps you view the top performers, and—if you’re an admin—adjust team scores with simple slash‑style commands.

---

## Features

- **View Leaderboard**  
  `danphe top <k>`  
  Shows the top _k_ teams sorted by their “Danphe Points.”

- **Admin Score Management**  
  `danphe increase_score '<team name>' <points>`  
  Increase a team’s points (requires admin permission).

- **Built‑in Help**  
  `danphe help`  
  Displays command usage and examples in an embedded message.

---

## Prerequisites

- **Python 3.10+**  
- **discord.py** (`pip install discord.py`)  
- **Google Sheets API** credentials with access to your target sheet  
- **OAuth2 Client Secrets** JSON for Google Sheets access  
- **Environment variables** (see Configuration below)

---

## Installation

1. **Clone this repository**  
   ```bash
   git clone https://github.com/your‑org/danphe‑leaderboard.git
   cd danphe‑leaderboard
   ```
2. **Create & activate a virtualenv**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Sheets credentials**

   * Place your `credentials.json` (OAuth2 client secrets) in the project root.
   * Share your target Google Sheet with the service account email.

---

## Configuration

Create a `.env` file in the project root with:

```dotenv
DISCORD_TOKEN=your-discord-bot-token
SHEET_ID=your_google_sheet_id
```

* **DISCORD\_TOKEN**: Bot token from the Discord Developer Portal.
* **SHEET\_ID**: The ID (long alphanumeric) of your leaderboard sheet.

---

## Usage

1. **Start the bot**

   ```bash
   python -m bot.main
   ```

2. **Invite to your server**
   Use the OAuth2 URL with `bot` and `applications.commands` scopes.

3. **Commands**

   * **Help**

     ```txt
     danphe help
     ```

     Shows an embedded help message.

   * **View Top k Teams**

     ```txt
     danphe top 5
     ```

     Shows the top 5 teams by points.

   * **Increase Team Score** *(Admins only)*

     ```txt
     danphe increase_score 'Uunchai' 10
     ```

     Increases “Uunchai”’s score by 10 points.

---

## Code Structure

* **`get_help()`**
  Constructs the Discord Embed for available commands.

* **`get_responses()`**
  Parses user input, enforces admin checks, and routes commands to:

  * `get_top_k_individual(k)`
  * `increase_score(team, points)`

* **`sheet_operations.py`**

  * `get_df()`
    Reads the entire sheet into a pandas DataFrame.
  * `get_top_k_individual(k)`
    Returns top‑k rows sorted by “Danphe Points.”
  * `increase_score(username, increase_point)`
    Finds the row, updates the score cell.

---
