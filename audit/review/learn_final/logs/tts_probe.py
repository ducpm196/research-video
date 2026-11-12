import asyncio, sys, time
import edge_tts

async def main():
    t = time.time()
    c = edge_tts.Communicate("Xin chào, đây là một câu thử giọng.", "vi-VN-NamMinhNeural")
    n = 0
    async for ch in c.stream():
        if ch["type"] == "audio":
            n += len(ch["data"])
    print("bytes", n, "sec", round(time.time() - t, 1))

try:
    asyncio.run(main())
except Exception as e:
    print("ERR", type(e).__name__, str(e)[:150])
