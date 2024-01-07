import asyncio
import inspect
from telethon import TelegramClient, events

from config import get_settings


class NewTelegramBot:
    def __init__(self, api_id: int, api_hash: str, bot_chat_id: int, commands_actions: list[dict[str, str]]):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_chat_id = bot_chat_id
        self.commands_actions = commands_actions
        self.client = TelegramClient('anon', self.api_id, self.api_hash)
        self.response_event = asyncio.Event()
        self.event_handler = None

    async def answer_handler(self, event, actions, command):
        if event.chat_id == self.bot_chat_id:
            if len(actions) == 1:
                if event.text == actions[0]['text']:
                    print(f"Received expected response for /{command}: {event.text}")
                else:
                    print(f"Received unexpected response for /{command}: {event.text}")
            else:
                if event.text == actions[0]['text']:
                    print(f"Received expected response for /{command}: {event.text}")
                else:
                    print(f"Received unexpected response for /{command}: {event.text}")
                actions.append(actions.pop(0))
            self.response_event.set()

    async def send_messages(self):
        async with self.client:
            for i in range(len(self.commands_actions)):
                for j in range(len(self.commands_actions[i]['commands'])):
                    for command in self.commands_actions[i]['commands'][j].split(", "):
                        self.response_event.clear()

                        # Remove existing event handler
                        if self.event_handler:
                            self.client.remove_event_handler(self.event_handler)

                        # Add a new event handler for the current command
                        self.event_handler = lambda e, a=self.commands_actions[i]['actions'], c=command: self.answer_handler(
                            e, a, c)
                        self.client.add_event_handler(self.event_handler,
                                                      events.NewMessage(incoming=True, outgoing=False))

                        await self.client.send_message(self.bot_chat_id, "/" + command)

                        # Wait for a response with a timeout
                        try:
                            await asyncio.wait_for(self.response_event.wait(), timeout=3)
                        except asyncio.TimeoutError:
                            print(f"Timeout waiting for response after 3sec to /{command}")
                        finally:
                            await asyncio.sleep(1.5)


def get_source_code_from_functions_using_inspect(dp):
    handlers = dp.observers['message'].handlers

    for handler in handlers:
        code_lines = inspect.getsource(handler.callback).split('\n')
        raw_commands = code_lines[0].split('@dp.message(Command(commands=[')
        raw_commands.pop(0)
        commands = []
        for i in range(len(raw_commands)):
            if i == len(raw_commands) - 1:
                commands.append(raw_commands[i].split('])')[0].replace("'", '').replace('"', ''))
            else:
                commands.append(raw_commands[i].split(']),')[0].replace("'", '').replace('"', ''))

        raw_actions = code_lines[2:-1]
        actions = []
        for raw_action in raw_actions:
            raw_action = raw_action.strip("await ")
            act = raw_action.split("(")
            actions.append(dict(action=act[0], text=act[1].split(")")[0].replace("'", '').replace('"', '')))

        yield dict(commands=commands, actions=actions)


if __name__ == "__main__":
    # Replace with your own values
    settings = get_settings()
    from bot import dp

    commands_actions = list(get_source_code_from_functions_using_inspect(dp))
    dce = 5
    new_telegram_bot = NewTelegramBot(api_id=settings.API_ID, api_hash=settings.API_HASH, bot_chat_id=settings.BOT_CHAT_ID, commands_actions=commands_actions)
    new_telegram_bot.client.start()
    new_telegram_bot.client.loop.run_until_complete(new_telegram_bot.send_messages())
