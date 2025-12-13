from config import load_config
from monitor import Monitor

import asyncio

try:
    config = load_config()
except OSError:
    print("config.json not found!")
    raise OSError("config.json file is required")
except ValueError as e:
    print(f"Invalid config.json: {e}")
    raise


async def run():
    monitor = Monitor(config)

    try:
        await monitor.initialize()
        await monitor.run()
    except Exception as e:
        print(f"Error occured monitoring sensors: {e}")


if __name__ == "__main__":
    asyncio.run(run())
