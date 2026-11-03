"""Đo edge-tts: độ trễ và loại lỗi mỗi lần gọi, đồng thời N câu. Chạy: .venv/Scripts/python audit/perf/tts_probe.py 1|3
Kết quả 2026-10-30: đồng thời 1 → 3/6 NoAudioReceived, 66 s; đồng thời 3 → 0/6, 26 s (lỗi do phía dịch vụ, không do đồng thời)."""
import asyncio, time, sys, edge_tts, os, tempfile
sys.stdout.reconfigure(encoding="utf-8")
T = ["Bài hôm nay nói về cách chia hệ thống thành các dịch vụ nhỏ.",
     "Mỗi dịch vụ có cơ sở dữ liệu riêng và giao tiếp qua mạng.",
     "Hãy dừng video và tự làm trước khi xem đáp án.",
     "Độ trễ trung vị là một trăm hai mươi mili giây.",
     "Ta kiểm lại bằng một ví dụ nhỏ với ba máy chủ.",
     "Lỗi thường gặp nhất là quên đặt thời hạn cho lời gọi mạng."]
async def one(i, t):
    f = os.path.join(tempfile.gettempdir(), f"probe{i}.mp3"); t0 = time.time()
    try:
        await asyncio.wait_for(edge_tts.Communicate(t + f" ({time.time():.0f})"[:0], "vi-VN-NamMinhNeural", rate="-5%").save(f), 60)
        return f"ok {time.time()-t0:5.1f}s {os.path.getsize(f)}B"
    except Exception as e:
        return f"ERR {time.time()-t0:5.1f}s {type(e).__name__}: {str(e)[:120]}"
async def main(conc):
    sem = asyncio.Semaphore(conc)
    async def g(i, t):
        async with sem: return await one(i, t)
    t0 = time.time(); r = await asyncio.gather(*[g(i, t) for i, t in enumerate(T)])
    print(f"đồng thời={conc} tổng {time.time()-t0:.1f}s"); [print("  ", x) for x in r]
asyncio.run(main(int(sys.argv[1])))
