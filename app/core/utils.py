import asyncio

def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # Create a new loop if none exists
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)
