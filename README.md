# Password-Generator

## Program Screenshot:
![Test](Screenshot.png "t")

## Info
This is a simple password generator written in Python for a college project. For the UI it uses Tkinter with my custom theme [Williams-Theme](https://github.com/unavailable-name/Williams-Theme "Williams-Theme"). The actual random nubmer generation uses `random.SecureRandom()` which internally uses os provided randomness that is classed as cryptographically secure.

## Usage
There are only a few settings available. Here they are and what they do:
- `Has Letters`: Generate a password that contains letters (a-zA-Z)
- `Has Digits`: Generates a password that contains numbers (0-9)
- `Has Punctuation`: Generates a password that contains all ASCII punctuation
- `Number of characters`: Changes number of characters in the output (Who would have thought?)

Alongside the settings, there are 2 extra buttons `Copy` and `Save` - they both do what they say on the tin. Copy copies the result into your clipboard, Save prompts you to save a file somewhere on your computer.

`Generate Password` Generates a Password.
