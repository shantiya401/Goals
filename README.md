Goals Bot

This is a Telegram bot designed to help users register, manage, and view their short-term and long-term goals. Users can input details about their goals, including descriptions, deadlines, priorities, and budgets, making it easier to track their personal objectives.

Features

User-Friendly Interface: Simple inline buttons for easy navigation.

Goal Registration: Users can register both short-term and long-term goals.

View Goals: Users can view their registered goals and check on completed objectives.

JSON Storage: Goals are stored in a JSON file for persistence across sessions.


Getting Started

Prerequisites

Python 3.x

pyTelegramBotAPI library


You can install the necessary library using pip:

  
```python
pip install pyTelegramBotAPI
```

Installation

1. Clone the repository:

```python
git clone https://github.com/shantiya401/Goals.git
cd Goals
```


2. Set up your bot token: Replace the placeholder token in the source code with your actual bot token.

```python
bot_token = "YOUR_BOT_TOKEN_HERE"
```
3. Run the bot:

Execute the script to start the bot:

```python
python your_bot_script.py
```


Usage

Start the Bot: Use the /start command to begin interacting with the bot.

Register Goals: Choose to register either short-term or long-term goals, providing necessary details such as subject, description, deadline, priority, and budget.

View Goals: Navigate to view your registered goals, and check on passed goals if applicable.


Bot Commands

/start: Initiates the bot and presents the main menu.

Inline Buttons:

"ثبت اهداف": Register a new goal.

"بازدید اهداف": View existing goals.



Goal Registration Flow

1. Select whether the goal is short-term or long-term.


2. Provide a subject for the goal.


3. Input a brief description.


4. Specify a deadline for achieving the goal.


5. Assign a priority level (Normal, Important, Very Important).


6. Enter the budget allocated for the goal.



Viewing Goals

Users can view their short-term, long-term, or passed goals.

Each goal is presented with its subject, description, and deadline, along with a budget.


Data Storage

The bot saves the goals in a JSON file located in the json directory. The structure is as follows:

```python
{
  "short_term_goals": [],
  "long_term_goals": [],
  "passed_goals": []
}
```

This setup allows for easy data retrieval and management.

Contributing

Contributions are welcome! If you want to improve the bot or add new features, feel free to fork the repository and submit a pull request.

License

This project is open-source and available under the MIT License.


---

Feel free to modify any part of this README to better fit your project or to add additional details you think may be important!

