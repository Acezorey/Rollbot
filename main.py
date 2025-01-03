import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from random import randint


# Loading discord token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


# Bot setup
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)


# Handles creation of message response
def respond(user_input):
    lowercase = user_input.lower()

    if lowercase != '' and lowercase[0] == '!':
        lowercase = lowercase[1:]
        output_nums = []

        if lowercase == "help":
            return 'To roll a d20, type "!1d20"\nTo roll two d20s, type "!2d20"\nTo roll a d50, type "!1d50", and so on\nAll commands begin with a "!" at the start, followed by the number of dice, "d", and the size of the dice'
        elif len(lowercase) < 3 or "d" not in lowercase:
            return 'Invalid command. Type "!help" for more info'
        else:
            nums = lowercase.split("d")

            if len(nums) > 2:
                return 'Invalid command. Type "!help" for more info'
            elif not nums[0].isnumeric() or not nums[1].isnumeric():
                return 'Invalid command. Type "!help" for more info'
            else:
                for i in range(int(nums[0])):
                    output_nums.append(randint(1, int(nums[1])))

        if len(output_nums) == 0:
            return "You somehow rolled a nonexistent dice"
        elif len(output_nums) > 1:
            output_string = "Roll: "
            sum = 0
            for i in range(len(output_nums)):
                if i != (len(output_nums) - 1):
                    output_string += (str(output_nums[i]) + " + ")
                else:
                    output_string += (str(output_nums[i]))
                sum += output_nums[i]
            output_string += ("\nTotal: " + str(sum))
            return output_string
        else:
            return f'Roll: {output_nums[0]}'


# Handles sending messages
async def send(message, user_message):
    try:
        response = respond(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)


# Indicates that the bot is now active
@client.event
async def on_ready():
    print(f'{client.user} is now online')


# Detects discord messages and sends responses
@client.event
async def on_message(message):

    # Ensures the bot does not respond to itself
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send(message, user_message)


# Code main entry point
def main():
    client.run(token = TOKEN)
if __name__ == '__main__':
    main()