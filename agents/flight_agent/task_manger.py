from .agent import execute
async def run(payload):
    print("payload", payload)
    return await execute(payload)