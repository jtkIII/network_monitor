import random
import asyncio


async def get_bot_stats() -> dict[str, int]:
    """
    Placeholder function.
    Eventually classify connections by user-agent, port, or known bot behavior.
    """
    await asyncio.sleep(0.05)  # simulate async I/O
    total = 100 + random.randint(-10, 10)
    bots = int(total * random.uniform(0.1, 0.3))
    legit = total - bots
    return {"total": total, "bots": bots, "legit": legit}

