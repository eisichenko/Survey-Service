# Survey-Service

### Installation

1. Run `sudo apt-get install python3-tk` is needed to show histograms from command line

2. `pip install -r requirements.txt` to install all packages

3. Install `PostgreSQL` (you can switch to any other database like SQLite easily)

4. Provide following secrets in `.env` file in the root of this project or using `environment variables`. **Keep you bot `token` in secret, as anyone who has it can do anything with your bot.** Example:

```python
TOKEN=<your bot token (use @BotFather to get it)>
DB_NAME=<database name>
DB_USER=<db user name>
DB_PASS=<db user password>
DB_HOST=<db host>
DB_PORT=<db port>
```

5. `python3 survey_bot/manage.py start_bot` - to start Telegram bot

6. `python3 survey_bot/manage.py runserver` to run website for managing bot surveys (url: http://127.0.0.1:8000/)

### Usage

There are to ways to interact with bot users:

1. Command line interface (CLI)

2. Website

- To run website use `python3 survey_bot/manage.py runserver` and go to http://127.0.0.1:8000/

- To see CLI commands run `python3 survey_bot/manage.py help` and go to `[bot_admin]` section. You will see commands like this:
    
1. `close_polls`
2. `close_questions`
3. `delete_polls`
4. `delete_questions`
5. `delete_students`
6. `get_poll_histogram`
7. `get_poll_options`
8. `get_poll_results`
9. `get_question_results`
10. `list_polls`
11. `list_questions`
12. `list_students`
13. `send_message`
14. `send_poll`
15. `send_poll_results`
16. `send_question`
17. `start_bot`

You can run any of them by `python3 survey_bot/manage.py <command>`.
