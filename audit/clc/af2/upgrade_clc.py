"""Nâng trọn bộ 13 bài CLC (L00–L12) lên chuẩn AF4 (common.upgrade_lesson force_code=True + lab P8 độc lập)."""
import sys as _sys; from pathlib import Path as _P; _sys.path.insert(0, str(_P(__file__).resolve().parents[2])); import _frozen  # noqa: E402,F401
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audit" / "review"))
sys.path.insert(0, str(ROOT / "audit" / "s9_11"))
import af2_kit as ak  # noqa: E402
import af2_upgrader as up  # noqa: E402
import common  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

LESSONS = [
    (
        "L00", "py", "Trách nhiệm khách hàng theo mô hình hạ tầng, nền tảng, hàm theo sự kiện và phần mềm",
        "# Lab CLC L00 — Ma trận trách nhiệm chia sẻ 4 mô hình đám mây\n\n"
        "Xét hệ thống gồm 5 lớp `['Hardware', 'OS', 'Runtime', 'App', 'Data']` (phần cứng, hệ điều hành, môi trường chạy, mã ứng dụng, dữ liệu). "
        "Tính số lớp khách hàng tự quản lý ở hạ tầng như dịch vụ (`IaaS`: 4 lớp trên phần cứng), nền tảng như dịch vụ (`PaaS`: 2 lớp trên cùng), hàm theo sự kiện (`FaaS`: 2 lớp hàm & dữ liệu), phần mềm như dịch vụ (`SaaS`: 1 lớp dữ liệu) và mức chênh lệch giữa `IaaS` với `SaaS`.\n\n"
        "Định dạng đầu ra (3 dòng):\n`iaas_layers=<số>`\n`paas_faas_saas=<a,b,c>`\n`iaas_minus_saas=<số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLC L00 duong_dan/bai_cua_ban.py\n```",
        "layers = ['Hardware', 'OS', 'Runtime', 'App', 'Data']\n"
        "cust = {\n"
        "    'IaaS': {'OS', 'Runtime', 'App', 'Data'},\n"
        "    'PaaS': {'App', 'Data'},\n"
        "    'FaaS': {'App', 'Data'},\n"
        "    'SaaS': {'Data'},\n"
        "}\n"
        "n = {m: sum(1 for x in layers if x in cust[m]) for m in cust}\n"
        "print(f\"iaas_layers={n['IaaS']}\")\n"
        "print(f\"paas_faas_saas={n['PaaS']},{n['FaaS']},{n['SaaS']}\")\n"
        "print(f\"iaas_minus_saas={n['IaaS'] - n['SaaS']}\")\n",
    ),
    (
        "L01", "py", "Độ sẵn sàng song song qua 2 và 3 vùng sẵn sàng (AZ) với ngưỡng 99,0%",
        "# Lab CLC L01 — Độ sẵn sàng song song đa vùng sẵn sàng (AZ)\n\n"
        "Mỗi vùng sẵn sàng (AZ: Availability Zone) độc lập có độ sẵn sàng `99,0%` (`xác suất hỏng p = 0,01`). "
        "Tính độ sẵn sàng khi chạy song song trên `2` vùng và `3` vùng (`1 - p^k`), cùng số phút ngừng kỳ vọng mỗi năm (`525 600` phút) ở mức 2 vùng.\n\n"
        "Định dạng đầu ra (3 dòng):\n`az2_avail_pct=<4 chữ số>%`\n`az3_avail_pct=<4 chữ số>%`\n`az2_downtime_min_year=<1 chữ số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLC L01 duong_dan/bai_cua_ban.py\n```",
        "p = 0.01\n"
        "a2 = 1.0 - p ** 2\n"
        "a3 = 1.0 - p ** 3\n"
        "dt = (1.0 - a2) * 525600\n"
        "print(f'az2_avail_pct={100 * a2:.4f}%')\n"
        "print(f'az3_avail_pct={100 * a3:.4f}%')\n"
        "print(f'az2_downtime_min_year={dt:.1f}')\n",
    ),
    (
        "L02", "py", "Chia dải mạng ảo riêng (VPC) 172.16.0.0/20 thành các mạng con /24",
        "# Lab CLC L02 — Chia mạng con trên mạng ảo riêng (VPC) bằng thư viện ipaddress\n\n"
        "Dùng thư viện chuẩn `ipaddress` chia mạng ảo riêng (`VPC`) dải `172.16.0.0/20` thành các mạng con (`subnet`) `/24`. "
        "Đếm tổng số mạng con `/24`, số địa chỉ IP mỗi mạng con và số IP khả dụng cho máy ảo sau khi trừ `5` địa chỉ nhà cung cấp giữ.\n\n"
        "Định dạng đầu ra (3 dòng):\n`subnets_24=<số>`\n`ips_per_24=<số>`\n`usable_cloud_ips=<số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLC L02 duong_dan/bai_cua_ban.py\n```",
        "import ipaddress\n"
        "vpc = ipaddress.IPv4Network('172.16.0.0/20')\n"
        "subs = list(vpc.subnets(new_prefix=24))\n"
        "n_ip = subs[0].num_addresses\n"
        "print(f'subnets_24={len(subs)}')\n"
        "print(f'ips_per_24={n_ip}')\n"
        "print(f'usable_cloud_ips={n_ip - 5}')\n",
    ),
    (
        "L03", "py", "Đánh giá chính sách phân quyền định danh (IAM): Explicit Deny luôn thắng Allow",
        "# Lab CLC L03 — Bộ đánh giá chính sách phân quyền định danh (IAM)\n\n"
        "Viết hàm `eval_iam(policies, action)` nhận danh sách cặp `(hiệu lực, tập thao tác)`. "
        "Nếu có bất kỳ câu `'Deny'` (từ chối tường minh) khớp `action` hoặc `'*'` thì trả `'DENY'`; ngược lại nếu có `'Allow'` khớp thì trả `'ALLOW'`; mặc định `'DENY'`. Kiểm thử 3 trường hợp trên bộ quyền cụ thể.\n\n"
        "Định dạng đầu ra (3 dòng):\n`read_allow=<ALLOW|DENY>`\n`terminate_deny=<ALLOW|DENY>`\n`unmatched_default=<ALLOW|DENY>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLC L03 duong_dan/bai_cua_ban.py\n```",
        "def eval_iam(policies, action):\n"
        "    hits = [eff for eff, acts in policies if action in acts or '*' in acts]\n"
        "    if 'Deny' in hits: return 'DENY'\n"
        "    return 'ALLOW' if 'Allow' in hits else 'DENY'\n"
        "p_ro = [('Allow', {'s3:GetObject'})]\n"
        "p_mix = [('Allow', {'*'}), ('Deny', {'ec2:TerminateInstances'})]\n"
        "print(f\"read_allow={eval_iam(p_ro, 's3:GetObject')}\")\n"
        "print(f\"terminate_deny={eval_iam(p_mix, 'ec2:TerminateInstances')}\")\n"
        "print(f\"unmatched_default={eval_iam(p_ro, 'iam:PassRole')}\")\n",
    ),
    (
        "L04", "py", "Kỳ vọng mất đối tượng ở độ bền 11 số 9 trên kho 25 triệu đối tượng",
        "# Lab CLC L04 — Đối chiếu độ bền 11 số 9 với kho 25 000 000 đối tượng\n\n"
        "Tính số đối tượng kỳ vọng mất mỗi năm trên kho `25 000 000` đối tượng ở mức độ bền 11 số 9 (`xác suất mất 10^-11/năm`) và 4 số 9 (`10^-4/năm`), "
        "cùng số năm trung bình để mất `1` đối tượng ở mức 11 số 9.\n\n"
        "Định dạng đầu ra (3 dòng):\n`loss_11nines=<5 chữ số>`\n`loss_4nines=<1 chữ số>`\n`years_per_loss=<số nguyên>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLC L04 duong_dan/bai_cua_ban.py\n```",
        "n = 25_000_000\n"
        "l11, l4 = n * 1e-11, n * 1e-4\n"
        "yrs = round(1.0 / l11)\n"
        "print(f'loss_11nines={l11:.5f}')\n"
        "print(f'loss_4nines={l4:.1f}')\n"
        "print(f'years_per_loss={yrs}')\n",
    ),
    (
        "L05", "py", "Điểm hoà vốn giữa gói trả theo giờ (0,15 USD/h) và gói đặt trước (840 USD/năm)",
        "# Lab CLC L05 — Tính điểm hoà vốn gói trả theo giờ và đặt trước\n\n"
        "Máy chủ trả theo giờ (`On-Demand`) có giá `0,15 USD/giờ`, trong khi gói đặt trước 1 năm (`Reserved`) trả trước `840 USD`. "
        "Tính số giờ hoà vốn, tỉ lệ phần trăm trên `8 760` giờ của cả năm và số tiền tiết kiệm nếu chạy suốt năm.\n\n"
        "Định dạng đầu ra (3 dòng):\n`breakeven_hours=<số>`\n`breakeven_pct_year=<1 chữ số>%`\n`full_year_saved_usd=<số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLC L05 duong_dan/bai_cua_ban.py\n```",
        "be = round(840 / 0.15)\n"
        "pct = 100.0 * be / 8760\n"
        "saved = round(8760 * 0.15 - 840)\n"
        "print(f'breakeven_hours={be}')\n"
        "print(f'breakeven_pct_year={pct:.1f}%')\n"
        "print(f'full_year_saved_usd={saved}')\n",
    ),
    (
        "L06", "py", "Tính tài nguyên GB-giây cho hàm theo sự kiện (serverless) 2,5 triệu lượt gọi",
        "# Lab CLC L06 — Chi phí GB-giây của hàm theo sự kiện (Serverless)\n\n"
        "Tính tổng `GB-giây` cho `2 500 000` lượt gọi hàm theo sự kiện ở hai cấu hình: `0,5 GB` chạy `160 ms/lượt`, và `1,0 GB` giúp giảm thời gian xuống `80 ms/lượt`. "
        "Kiểm tra xem tổng `GB-giây` của hai phương án có bằng nhau hay không.\n\n"
        "Định dạng đầu ra (3 dòng):\n`gb_sec_512mb=<số>`\n`gb_sec_1gb=<số>`\n`same_gb_sec=<0|1>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLC L06 duong_dan/bai_cua_ban.py\n```",
        "calls = 2_500_000\n"
        "g1 = round(calls * 0.160 * 0.5)\n"
        "g2 = round(calls * 0.080 * 1.0)\n"
        "print(f'gb_sec_512mb={g1}')\n"
        "print(f'gb_sec_1gb={g2}')\n"
        "print(f'same_gb_sec={int(g1 == g2)}')\n",
    ),
    (
        "L07", "py", "So sánh điểm khôi phục mục tiêu (RPO) của chụp nhanh 12 giờ vs nhật ký WAL 2 phút",
        "# Lab CLC L07 — Giảm ngưỡng mất dữ liệu (RPO) nhờ nhật ký giao dịch WAL\n\n"
        "So sánh điểm khôi phục mục tiêu (`RPO`) khi chỉ chụp nhanh (`snapshot`) mỗi `12` giờ (`720` phút) với phương án đẩy thêm nhật ký giao dịch (`WAL`) mỗi `2` phút, "
        "và tính hệ số thu hẹp cửa sổ mất dữ liệu.\n\n"
        "Định dạng đầu ra (3 dòng):\n`snap_rpo_min=<số>`\n`wal_rpo_min=<số>`\n`rpo_cut=<số>x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLC L07 duong_dan/bai_cua_ban.py\n```",
        "snap_min = 12 * 60\n"
        "wal_min = 2\n"
        "print(f'snap_rpo_min={snap_min}')\n"
        "print(f'wal_rpo_min={wal_min}')\n"
        "print(f'rpo_cut={snap_min // wal_min}x')\n",
    ),
    (
        "L08", "py", "Ước lượng cước truyền dữ liệu ra ngoài (Egress) 30 TB và mức tiết kiệm nhờ CDN biên",
        "# Lab CLC L08 — Tính cước truyền dữ liệu ra ngoài (Egress) 30 TB/tháng\n\n"
        "Tính lượng GB tương ứng của `30 TB` (`1 TB = 1 024 GB`), chi phí hàng tháng ở mức `0,08 USD/GB`, và khoản tiết kiệm nếu mạng phân phối nội dung tại biên (`CDN`) hấp thụ `75%` lưu lượng khỏi máy chủ nguồn.\n\n"
        "Định dạng đầu ra (3 dòng):\n`egress_gb=<số>`\n`monthly_usd=<2 chữ số>`\n`cdn_saved_usd=<2 chữ số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLC L08 duong_dan/bai_cua_ban.py\n```",
        "gb = 30 * 1024\n"
        "cost = gb * 0.08\n"
        "saved = cost * 0.75\n"
        "print(f'egress_gb={gb}')\n"
        "print(f'monthly_usd={cost:.2f}')\n"
        "print(f'cdn_saved_usd={saved:.2f}')\n",
    ),
    (
        "L09", "py", "Mã hoá phong bì (KMS): xoay khoá chính chỉ bọc lại 25 000 khoá dữ liệu DEK",
        "# Lab CLC L09 — Tính chi phí xoay khoá chính theo mã hoá phong bì (KMS)\n\n"
        "Kho dữ liệu có `2 TB` (`2 * 10^12 byte`) được bảo vệ bởi `25 000` khoá dữ liệu (`DEK`), mỗi khoá dài `32 byte`. "
        "Tính tổng số byte và KB cần bọc lại khi xoay khoá chính tại dịch vụ quản lý khoá (`KMS`), và xác nhận nhỏ hơn nhiều so với dữ liệu gốc.\n\n"
        "Định dạng đầu ra (3 dòng):\n`dek_bytes=<số>`\n`dek_kb=<1 chữ số>`\n`smaller_than_raw=<0|1>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLC L09 duong_dan/bai_cua_ban.py\n```",
        "dek_b = 25_000 * 32\n"
        "raw_b = 2 * 10 ** 12\n"
        "print(f'dek_bytes={dek_b}')\n"
        "print(f'dek_kb={dek_b / 1000:.1f}')\n"
        "print(f'smaller_than_raw={int(dek_b < raw_b)}')\n",
    ),
    (
        "L10", "py", "Dung lượng thường trực của chủ động–chủ động (Active-Active) 2 vùng vs 3 vùng N+1",
        "# Lab CLC L10 — Tính dung lượng dự phòng liên vùng ở tải 1 800 yêu cầu/giây\n\n"
        "Hệ thống phục vụ tải bình thường `1 800 yêu cầu/giây (req/s)` và phải sống sót khi mất 1 vùng. "
        "Tính tổng công suất cần cấp ở mô hình chủ động–chủ động (`Active-Active`) `2` vùng (mỗi vùng gánh `1 800`), mô hình `3` vùng dự phòng `N+1` (mỗi vùng gánh `900`), và phần trăm dự phòng dư của phương án 2 vùng.\n\n"
        "Định dạng đầu ra (3 dòng):\n`cap_2region=<số>`\n`cap_3region=<số>`\n`headroom_2region=<1 chữ số>%`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLC L10 duong_dan/bai_cua_ban.py\n```",
        "norm = 1800\n"
        "cap2, cap3 = 2 * norm, 3 * (norm // 2)\n"
        "head = 100.0 * (cap2 - norm) / norm\n"
        "print(f'cap_2region={cap2}')\n"
        "print(f'cap_3region={cap3}')\n"
        "print(f'headroom_2region={head:.1f}%')\n",
    ),
    (
        "L11", "py", "Rà thiết kế ứng dụng 3 tầng chuyển sang dịch vụ quản lý đa vùng (99,9%/AZ)",
        "# Lab CLC L11 — Rà phương án chuyển ứng dụng 3 tầng và kiểm tra 6 trụ cột\n\n"
        "Phương án mục tiêu gồm: cơ sở dữ liệu đa vùng sẵn sàng (`db_az = 2`, mỗi AZ `99,9%`), tầng ứng dụng không giữ trạng thái co giãn trong khoảng `[3, 12]` máy, và đầy đủ `6` trụ cột kiến trúc tốt (`Vận hành`, `An toàn`, `Tin cậy`, `Hiệu năng`, `Chi phí`, `Bền vững`). "
        "Tính độ sẵn sàng mới của tầng dữ liệu và kiểm tra xem mọi điểm lỗi đơn (`SPOF`) đã được loại bỏ chưa.\n\n"
        "Định dạng đầu ra (4 dòng):\n`multi_az_avail=<6 chữ số>%`\n`app_bounds=<min,max>`\n`spof_cleared=<0|1>`\n`pillars=<số>`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLC L11 duong_dan/bai_cua_ban.py\n```",
        "av = 1.0 - (1.0 - 0.999) ** 2\n"
        "bounds, db_az = (3, 12), 2\n"
        "pillars = [\n"
        "    'van_hanh', 'an_toan', 'tin_cay',\n"
        "    'hieu_nang', 'chi_phi', 'ben_vung',\n"
        "]\n"
        "ok = int(db_az >= 2 and bounds[0] >= 2)\n"
        "print(f'multi_az_avail={100 * av:.6f}%')\n"
        "print(f'app_bounds={bounds[0]},{bounds[1]}')\n"
        "print(f'spof_cleared={ok}')\n"
        "print(f'pillars={len(pillars)}')\n",
    ),
    (
        "L12", "py", "Đối chiếu sự cố 2017 với ngân sách ngừng 99,99% và hệ số tăng trưởng kho đối tượng",
        "# Lab CLC L12 — Ngân sách ngừng 99,99% vs 99,95% và hệ số tăng trưởng kho đối tượng\n\n"
        "Sự cố tháng 2/2017 kéo dài từ `09:37` tới `13:54` (`257` phút). Tính ngân sách ngừng cả năm (`525 600` phút) ở mức `99,99%` và tỉ số vượt ngân sách năm của sự cố; đồng thời tính hệ số tăng trưởng số đối tượng từ `200 tỉ` (năm 2010) lên `100 nghìn tỉ` (năm 2021).\n\n"
        "Định dạng đầu ra (3 dòng):\n`outage_min=<số>`\n`ratio_99_99=<1 chữ số>x`\n`growth_2010_2021=<số>x`\n\n"
        "Chấm tự động:\n```bash\nbash labs/cham.sh CLC L12 duong_dan/bai_cua_ban.py\n```",
        "out = (13 * 60 + 54) - (9 * 60 + 37)\n"
        "bud = 525600 * 0.0001\n"
        "growth = round(100_000_000_000_000 / 200_000_000_000)\n"
        "print(f'outage_min={out}')\n"
        "print(f'ratio_99_99={out / bud:.1f}x')\n"
        "print(f'growth_2010_2021={growth}x')\n",
    ),
]

COVERS_MAP = {
    "L00": [(1, "sym"), (2, "intuition"), (3, "example")],
    "L01": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L02": [(1, "example"), (2, "intuition"), (3, "check")],
    "L03": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L04": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L05": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L06": [(1, "example"), (2, "check"), (3, "practice")],
    "L07": [(1, "sym"), (2, "example"), (3, "check")],
    "L08": [(1, "example"), (2, "intuition"), (3, "practice")],
    "L09": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L10": [(1, "intuition"), (2, "example"), (3, "practice")],
    "L11": [(1, "example"), (2, "check"), (3, "pitfalls")],
    "L12": [(1, "stage1"), (2, "stage5"), (3, "practice")],
}

if __name__ == "__main__":
    for lid, ext, hint, de_md, sol in LESSONS:
        common.upgrade_lesson(
            "CLC", lid, hint, de_md, sol,
            add_code_if_missing=True,
            covers=COVERS_MAP[lid],
            force_code=True,
        )
    led_p, nblk = up.sync_course_ledger("CLC", default_lang="python")
    for lid, _, _, _, sol in LESSONS:
        common.sync_practice_run_blocks("CLC", lid, sol)
    print(f"=== CLC: {len(LESSONS)} bài OK, ledger={nblk} blocks ===", flush=True)
    tpl = subprocess.run([ak.VENV_PY, "-B", "audit/review/sync_tpl_from_lesson.py", "CLC", "--write"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    print("sync_tpl CLC:", tpl.stdout.strip() or tpl.stderr.strip())
