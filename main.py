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
    input_array = user_input.split()

    if input_array[0] == '!help':
        return '```Commands:\n!help: Returns list of commands\n!roll: Roll dice\n\nHow to roll:\nType "1d20" to roll a 20 sided dice 1 time\nType "2d20" to roll a 20 sided dice 5 times\nType "1d50" to roll a 50 sided dice 1 time\nTo add or subtract from a roll, type "1d20 + 2" or "1d20 - 2" for example\n\nFor all rolls: XdY +/- Z\n - X: number of dice\n - Y: size of dice\n - Z: constant addition\n\nAdding extra words after the roll allows you to label it\nEx: "1d20 Roll to hit"```'
    
    num_verification = validate(input_array)

    # Command is incorrect
    if num_verification == 0:
        return '```You have entered an incorrect command. Type "!help" for more info```'

    # Command is correct and does not have an add or subtract
    elif num_verification == 1:
        result = roll(input_array[1])
        if len(input_array) > 2:
            result = to_string(input_array[2:]) + "\n\n" + result
        return "```" + result + "```"

    # Command is correct and has an add and subtract
    else:
        result = roll(input_array[1], operand=input_array[2], constant_str=input_array[3])
        if len(input_array) > 4:
            result = to_string(input_array[4:]) + "\n\n" + result
        return "```" + result + "```"


def validate(input_array):
    length = len(input_array)

    if length < 2:
        return 0
    
    roll = input_array[1].split("d")

    if len(roll) < 2 or len(roll) > 2:
        return 0
    
    if not roll[0].isnumeric() or not roll[1].isnumeric():
        return 0

    if length >= 4 and (input_array[2] == "+" or input_array[2] == "-" and input_array[3].isnumeric()):
        return 2
    else:
        return 1
    

def roll(input, operand="+", constant_str=0):
    nums_str = input.split("d")
    nums = [int(nums_str[0]), int(nums_str[1])]
    constant = int(constant_str)

    result = ""
    sum = 0
    num = 0

    if nums[0] == 0 or nums[1] == 0:
        return "You somehow rolled a nonexistent dice"

    for i in range(nums[0]):
        if i != 0 and i != nums[0]:
            result += " + "
        num = randint(1, nums[1])
        sum += num
        result += str(num)
    
    if constant > 0:
        sum += constant
        result = "(" + result + f') {operand} ' + constant_str + f"\n\nTotal: {sum}"
    elif nums[0] > 1:
        result += f"\n\nTotal: {sum}"

    result = "Roll: " + result
    
    return result


def to_string(user_input_array):
    result = '['

    for i in range(len(user_input_array)):
        if i == 0:
            result += user_input_array[i]
            continue
        result += " " + user_input_array[i]

    return result + ']'


# Handles sending messages
async def send(message, user_message):
    try:
        response = respond(user_message)
        await message.reply(response)
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

    if message.content[0:6] == '!roll ' or message.content == '!help':
        await send(message, user_message)


# Code main entry point
def main():
    client.run(token = TOKEN)
if __name__ == '__main__':
    main()