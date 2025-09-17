#!/usr/bin/env python3
from telethon.sync import TelegramClient, events
import asyncio
import sys
import random
import time

api_id = 29664037
api_hash = '9fce2596e2a1e9720c0f938742e87ad6'
phone = +79911132234

client = TelegramClient('tg_session', api_id, api_hash)

# Typing effect function
def type_effect(text, speed=0.03, variation=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(max(0, speed + random.uniform(-variation, variation)))
    print()

async def main():
    try:
        # Connect and authenticate
        await client.start(phone=phone)
        type_effect("\nTelegram CLI Ready! Commands:")
        type_effect("  /c [username] - Start chat")
        type_effect("  /s [message]  - Send message")
        type_effect("  /exit         - Quit\n")

        current_chat = None

        # Handler for new incoming messages
        @client.on(events.NewMessage(incoming=True))
        async def new_message_handler(event):
            sender = await event.get_sender()
            name = sender.first_name if sender else "Unknown"
            print("\n[New message] ", end='')
            type_effect(f"{name}: {event.text}")
            print(">~~~< ", end="", flush=True)

        while True:
            cmd = input(">~~~< ").strip().split(maxsplit=1)
            if not cmd:
                continue

            # Chat with a user/group
            if cmd[0] == "/c":
                if len(cmd) < 2:
                    type_effect("Usage: /c username")
                    continue
                try:
                    current_chat = await client.get_entity(cmd[1])
                    type_effect(f"Chatting with: {current_chat.first_name or current_chat.title}")
                    # Show last 3 messages
                    async for msg in client.iter_messages(current_chat, limit=3):
                        sender = await msg.get_sender()
                        name = sender.first_name if sender else "Unknown"
                        type_effect(f"{name}: {msg.text}")
                except Exception as e:
                    type_effect(f"Error: {e}")

            # Send a message
            elif cmd[0] == "/s":
                if not current_chat:
                    type_effect("No active chat. Use /c first!")
                    continue
                if len(cmd) < 2:
                    type_effect("Usage: /s Hello!")
                    continue
                await client.send_message(current_chat, cmd[1])
                type_effect("Message sent!")

            # Exit
            elif cmd[0] == "/exit":
                await client.disconnect()
                type_effect("Bye!")
                sys.exit(0)

            else:
                type_effect("Unknown command. Try /c, /s, or /exit")

    except Exception as e:
        type_effect(f"Fatal error: {e}")
        await client.disconnect()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())