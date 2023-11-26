# HashGPT Bot
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Creating Your Own Bot](#creating-your-own-bot)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)

## Introduction

This project is a chatbot that utilizes OpenAI's GPT-3.5 and GPT-4 APIs for intelligent conversations. You can use your own API key and access additional features via Telegram commands. Get started with this powerful chatbot for enhanced language processing.

## Features

Utilize your own API key for a personalized and seamless integration experience with our chatbot. It comes packed with a variety of functionalities that enhance your interactions. You can activate specific features directly within Telegram using these commands:

    /read - Extracts and reads the content of the provided URL, delivering the main information straight to your chat.
    /google - Conducts a Google search with the specified query and presents you with the top results.
    /youtube - Retrieves the transcripts of a selected YouTube video for quick and easy text reference.
    /dalle - Leverages OpenAI's DALL-E model to generate imaginative and relevant images based on your prompt.

Newly Added Features:

1. File Summarization:
    - Send a PDF file to the chatbot to receive a concise summary of the content, enabling you to grasp the essence of the document without reading it in its entirety.

2. Voice Interaction:
    - Engage with the chatbot using voice messages. Simply send a voice command or query, and the bot will respond with an audible voice message, making the interaction more dynamic and accessible.

By incorporating these new capabilities, our chatbot becomes even more versatile and user-friendly, enriching your Telegram experience.

## Installation

1. Open the Telegram app on your device.

2. Search for the HashGPT bot by entering its username `hashgpt4301_bot`. Select the bot from the search results.

3. Open a chat with the bot by clicking on its name.

4. Start interacting with the bot by sending messages. You can type `/help` in the chat with the bot and the bot will provide you with a list of supported commands and their functionalities.

## Usage

1. Visit your [OpenAI's API Keys page](https://platform.openai.com/account/api-keys).

2. Provide your API KEY using `/api_key <your-api-key>` command. Make sure to replace `<your-api-key>` with your actual API key obtained from [OpenAI's API Keys page](https://platform.openai.com/account/api-keys).

3. You can start using HashGPT bot with GPT-3.5 and GPT-4 models.
 
4. The standard configuration employs the GPT-3.5 model. If you wish to activate the GPT-4 model, please use the command `/gpt4 gpt-4`. Conversely, to revert to the GPT-3.5 model, the appropriate command is `/gpt3 gpt-3.5`.

## Creating Your Own Bot

If you prefer a personalized bot, this section guides you on setting up your own chatbot on a local machine using this Django repository.

#### Prerequisites:
- Python 3.6 or higher installed on your local machine.
- Telegram account and basic knowledge of bot creation through BotFather.
- OpenAI API key from your OpenAI account.

#### Step-by-Step Guide:

1. **Clone the Repository**: 
   - Use `git clone https://github.com/sazaktechs/hashgpt-telegrambot.git` to clone the project repository to your local machine.

2. **Set Up a Virtual Environment**: 
   - Navigate to the cloned directory.
   - Run `python3 -m venv venv` to create a virtual environment.
   - Activate it by running `source venv/bin/activate` (Unix) or `.\venv\Scripts\activate` (Windows).

3. **Install Dependencies**:
   - Inside the activated virtual environment, install the necessary packages with `pip install -r requirements.txt`.

4. **Telegram Bot Creation**:
   - Create a new Telegram [bot](https://core.telegram.org/bots/features#botfather) via BotFather and obtain the associated token.

5. **Environment Variables**: 
   - Add your obtained Telegram Bot Token and OpenAI API key to a `.env` file.

6. **Start the Django Development Server**:
   - Launch your server using `python manage.py runserver`.

7. **Webhook Setup**:
   - Set a [webhook](https://core.telegram.org/bots/api#setwebhook) by using the [Local Bot API Server](https://github.com/tdlib/telegram-bot-api) to point new messages to your local development server.

8. **Interact with Your Bot**:
   - Open Telegram and start a conversation with your newly created bot.

## Contributing

Have ideas for how HashGPT can be improved? Feel free to open an issue or a pull request!

## License



## Contact Information

