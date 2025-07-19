
-----

# Tulga CLI
TulgaBot is a tool that allows you to chat and voice chat with virtual characters via Character AI

## Installation

```bash
git clone https://github.com/davidsuragan/TulgaBOT-cli.git
cd TulgaBOT-cli
pip install -r requirements.txt
```

## Getting Started

1.  **Obtain your token:**
    *   ⚠️ **DO NOT SHARE YOUR TOKEN!** It is required to send requests from your account.
    *   Open link https://character.ai/chat/2WPyJRflV_4nTx6_-tuNrhkiiqhDyOsn9O25BR1sDO8
    *   Open **Developer Tools** in your browser (usually F12).
    *   Go to the **Network** tab.
    *   Refresh the page or send a message to any character.
    *   In the list of network requests, click on any request (for example, to `/settings`).
    <img src="https://github.com/dauitsuragan002/tulgatts/raw/main/img/asset.jpg" alt="How to find the Authorization Token" width="650"/>

    *   Go to the **Headers** section.
    *   Find the **Authorization** header. It will look like:
        ```
        Authorization: Token <your_token_here>
        ```
    *   Copy only the token part (after `Token `).
    *   Set the `CHARACTER_AI_TOKEN` environment variable or create a `.env` file in the project root and add `CHARACTER_AI_TOKEN=your_copied_token`.

2.  **Run the application:**

    ```bash
    python app.py
    ```

## Usage

1.  Choose a mode (voice/text):

      * `text` - text-only chat
      * `voice` - voice chat

2.  Select a character:

      * Nursultan Nazarbaev
      * Tokaev
      * Pavel Durov
      * Nurlan Saburov
      * Putin
      * Skriptonit
      * Elon Musk
      * Albert E
      * J.A.R.V.I.S
      * Yandex Alica
      * Tony Stark

3.  Type your message

4.  To end the conversation, type `quit`, `exit`, or `bye`

## Authors

  - David Suragan ([https://t.me/david667s](https://t.me/david667s)) - Main developer
  - Claude (Anthropic AI) - AI assistant, code optimization, and documentation

## Disclaimer

This project is created for educational and research purposes only. The use of the Character AI service should comply with their terms of service.

## Acknowledgments

This project was built with the help of the [PyCharacterAI](https://github.com/Xtr4F/PyCharacterAI) library. We extend our immense gratitude to the PyCharacterAI authors for creating an excellent tool that enables interaction with the Character AI platform. Without their efforts, this project would not have been possible.
