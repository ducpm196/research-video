# Lộ trình theo nghề (SINH TỰ ĐỘNG — không sửa tay)

Sinh bởi `audit/review/tracks.py` từ `curriculum/tracks.yaml` (mục tiêu của từng nghề) và tiên quyết của mọi lộ trình.
Mỗi nghề liệt kê ĐÚNG các bài cần học — gồm mọi bài nền mà mục tiêu đòi hỏi — theo thứ tự thoả mọi tiên quyết (đã kiểm từng cạnh).
“✓” = số bài đã có video hoàn thiện (theo `audit/review/audit_all.tsv`).

## Nền tảng chung (mọi nghề học trước)

Mục tiêu: FND, JVA, JV2, PYT, DMS, CS112, CS115:L00-L21, CS115:L44, CS115:L45, CS115:L46 · **124 bài** · ✓ 124

**FND** → **JVA** → **JV2** → **PYT** → **DMS** → **CS112** → **CS115** (L00–L21, L44–L46)

## Kỹ sư AI / học máy

Mục tiêu: CS115, AIF, DSC, MLP, MLO, CVI, RLN, PAR:L00-L02, PAR:L11-L12, SEP, CAS:L10 · **265 bài** · ✓ 265

**FND** → **PYT** (L00–L09) → **DMS** (L00–L07, L09–L10, L16–L19) → **CS112** (L00–L08, L12, L14, L16, L18, L24) → **CS115** → **CPR** (L00) → **CSA** (L00–L08, L10–L11, L13–L15) → **OSY** (L00–L01, L04, L08–L09, L12, L14) → **NET** (L00–L02, L09, L12) → **SWF** (L00–L01, L03–L04, L06, L11–L12) → **DBS** (L00–L02) → **DSY** (L00) → **CLD** (L00–L03, L05, L08, L10) → **DVO** (L00–L01, L03–L04, L07) → **AIF** → **DSC** → **MLP** → **MLO** → **LLM** (L00–L01, L03–L06, L08–L09) → **RLN** → **CVI** → **PAR** (L00–L03, L05–L07, L10–L12) → **SEP** → **CAS** (L00, L10)

## Kỹ sư mô hình ngôn ngữ lớn và AI agent

Mục tiêu: LLM, AGT, IRS:L00-L05, RLN:L10-L11, SEC:L04, SEC:L06, MLO:L06-L13, SEP, CAS:L00 · **219 bài** · ✓ 219

**FND** → **PYT** (L00–L07) → **DMS** (L00–L10, L13, L19) → **CS112** (L00–L01, L03–L08, L16, L18, L24) → **CS115** (L00–L03, L05–L09, L12–L15, L17–L23, L29, L35, L39, L41, L44) → **CPR** (L00) → **CSA** (L00–L03, L05–L08, L10, L13–L15) → **OSY** (L00–L01, L08–L09, L12, L14) → **NET** (L00–L01, L09, L12) → **SWF** (L00–L01, L03–L06, L11–L12) → **SDP** (L00–L01) → **DBS** (L00–L02, L07–L09) → **SEC** (L00–L06) → **DSY** (L00, L06–L07, L12) → **CLD** (L00–L03, L05, L08, L10–L11) → **DVO** (L00–L01, L03–L04, L07) → **DEN** (L00, L07) → **AIF** (L00–L01, L08–L10) → **DSC** (L00–L11, L13–L14) → **MLO** (L00–L02, L05–L13) → **LLM** → **AGT** → **RLN** (L00–L01, L04, L07–L11) → **IRS** (L00–L05) → **SEP** → **CAS** (L00)

## Nhà khoa học dữ liệu / phân tích dữ liệu

Mục tiêu: DBS:L00-L03, DAN, DSC, MLP, MLO:L08-L10, SEP, CAS:L10 · **126 bài** · ✓ 126

**FND** (L00–L06) → **PYT** (L00–L09) → **DMS** (L00–L03, L05–L07, L09–L10, L19) → **CS115** (L00–L03, L05–L09, L12–L15, L17–L23, L44) → **NET** (L00, L09, L12) → **SWF** (L00, L11) → **DBS** (L00–L03) → **CLD** (L00, L03, L10) → **DVO** (L00) → **DSC** → **DAN** → **MLP** → **MLO** (L00–L02, L05–L06, L08–L10) → **SEP** → **CAS** (L00, L10)

## Kỹ sư dữ liệu (dữ liệu lớn, luồng, hướng sự kiện)

Mục tiêu: DBS, DSY, DEN, EVT, CAS:L08 · **183 bài** · ✓ 183

**FND** → **PYT** (L00–L07) → **DMS** (L00–L10, L13, L19) → **CS112** (L00–L08, L12–L13, L23) → **CS115** (L00–L02, L06–L07, L12–L14) → **CPR** (L00) → **CSA** (L00–L02, L05–L08, L10, L13–L15) → **OSY** (L00–L01, L04–L06, L08–L09, L12, L14) → **NET** (L00–L02, L05, L09, L12) → **SWF** (L00–L01, L03–L05, L07, L11) → **SDP** (L00–L07, L14) → **DBS** → **SEC** (L00, L04, L12–L14) → **WEB** (L00, L03, L06, L12–L14) → **DSY** → **CLD** (L00, L03–L04, L10–L11, L14) → **SAR** (L00, L02, L04–L09) → **DEN** → **EVT** → **CAS** (L00, L08)

## Kỹ sư phần mềm fullstack web và di động

Mục tiêu: SWF, SDP, DBS, WEB, HCI, DVO, SEC:L00-L06, SEP, CAS:L05, CAS:L07 · **238 bài** · ✓ 238

**FND** → **PYT** (L00–L07) → **DMS** (L00–L07, L09–L10, L13–L15, L19) → **CS112** (L00–L08, L12–L14, L16, L18–L20, L23, L27) → **CS115** (L00–L03, L05–L09, L12–L15, L17–L21, L44) → **CPR** (L00) → **CSA** (L00–L02, L05–L08, L10, L14–L15) → **OSY** (L00–L01, L04–L06, L08–L09, L12, L14) → **NET** (L00–L02, L09–L14) → **SWF** → **SDP** → **DBS** → **SEC** (L00–L08) → **WEB** → **CLD** (L00–L03, L05, L08, L10–L13) → **DVO** → **DSC** (L00–L02, L04, L06–L08, L13) → **TOC** (L00–L03) → **HCI** → **SEP** → **CAS** (L00, L05, L07)

## Kỹ sư hệ thống: DevOps, SRE, điện toán đám mây, Kubernetes

Mục tiêu: LNX, OSY, NET, CLD, CLC, DVO, SAR, CAS:L05-L08 · **195 bài** · ✓ 195

**FND** → **PYT** (L00–L07) → **DMS** (L00–L05, L07, L13–L15) → **CS112** (L00–L01, L03–L08, L16, L18, L24) → **CS115** (L00–L02, L06–L07, L12–L14) → **CPR** (L00) → **LNX** → **CSA** (L00–L02, L05–L08, L10, L13–L15) → **OSY** → **NET** → **SWF** (L00–L01, L03–L04, L06, L11–L12) → **DBS** (L00–L02, L04–L05, L11, L14) → **SEC** (L00, L04, L07, L12–L14) → **DSY** (L00, L03–L06, L13–L14) → **CLD** → **DVO** → **SAR** → **CLC** → **TOC** (L00–L03) → **CAS** (L00, L05–L08)

## Kiến trúc sư hệ thống lớn

Mục tiêu: SAR, DSY, EVT, CLD, DEN, SEC:L11-L14, CAS · **257 bài** · ✓ 257

**FND** → **PYT** (L00–L07) → **DMS** (L00–L10, L13–L15, L19) → **CS112** (L00–L08, L12–L13, L16, L23) → **CS115** (L00–L03, L05–L09, L12–L15, L17–L21, L44) → **CPR** (L00) → **CSA** (L00–L08, L10, L13–L15) → **OSY** (L00–L01, L04–L06, L08–L09, L12, L14) → **NET** (L00–L02, L05, L09, L12–L14) → **SWF** (L00–L01, L03–L07, L11–L12) → **SDP** (L00–L07, L14) → **DBS** (L00–L05, L07–L16) → **SEC** (L00, L04, L11–L14) → **WEB** (L00, L03, L06, L12–L14) → **DSY** → **CLD** → **DVO** (L00–L01, L03–L04, L07, L09) → **SAR** → **DEN** → **EVT** → **DSC** (L00–L10, L14) → **MLO** (L00–L02, L05–L06, L08–L09) → **TOC** (L00–L03) → **CAS**

## Kỹ sư an toàn thông tin (phòng thủ)

Mục tiêu: SEC, NET, OSY, CSA:L00-L04, WEB:L09, CAS:L09, SEP:L07 · **136 bài** · ✓ 136

**FND** → **PYT** (L00–L07) → **DMS** (L00–L07, L09–L10, L13–L15, L19) → **CS112** (L00–L01, L03–L08, L16, L18, L24) → **CS115** (L00–L02, L06–L07, L12–L13) → **CPR** (L00) → **CSA** (L00–L08, L10, L14–L15) → **OSY** → **NET** → **SWF** (L00–L01, L03–L05, L07, L11–L12) → **SDP** (L00–L07, L14) → **SEC** → **WEB** (L00, L06, L09) → **SEP** (L00, L07) → **CAS** (L00, L09)

## Kỹ sư hệ nhúng và robot

Mục tiêu: CPR, ESY, RBM, ROB, CVI:L03, CVI:L05-L06, CAS:L01-L04 · **169 bài** · ✓ 169

**FND** → **PYT** (L00–L07) → **DMS** (L00–L07, L09–L10, L13–L15, L19) → **CS112** (L00–L01, L03–L08, L16, L18, L24) → **CS115** (L00–L09, L12–L15, L17–L23, L34, L44) → **CPR** → **CSA** (L00–L08, L15) → **OSY** (L00–L05) → **NET** (L00, L09, L12–L14) → **SWF** (L00–L01, L03–L05, L07) → **SDP** (L00–L02) → **AIF** (L00–L02) → **CVI** (L00–L01, L03–L06) → **CAS** (L00–L04) → **RBM** → **ESY** → **ROB**

## Đồ hoạ máy tính và thị giác máy tính

Mục tiêu: GFX, CVI, PAR:L06-L09 · **144 bài** · ✓ 144

**FND** → **PYT** (L00–L07) → **DMS** (L00–L03, L05–L07, L09–L10, L19) → **CS112** (L00–L01, L08, L12) → **CS115** (L00–L09, L12–L15, L17–L23, L34, L44) → **CPR** (L00) → **CSA** (L00–L11, L13, L15) → **OSY** (L00–L01, L04) → **NET** (L00, L09, L12) → **SWF** (L00, L11) → **DBS** (L00–L02) → **CLD** (L00, L03, L10) → **DVO** (L00) → **DSC** (L00–L10, L14) → **MLO** (L00–L02, L05–L06, L08) → **CVI** → **PAR** (L00, L02–L03, L05–L09) → **RBM** (L00–L01, L03, L07, L14) → **GFX**

## Khoa học máy tính lõi (nghiên cứu, học lên cao)

Mục tiêu: CPR, LNX, CS112, TOC, PLC, CSA, OSY, NET, DSY, PAR · **208 bài** · ✓ 208

**FND** → **PYT** (L00–L07) → **DMS** (L00–L03, L05–L10, L13–L15, L19) → **CS112** → **CS115** (L00–L03, L05–L09, L12–L13) → **CPR** → **LNX** → **CSA** → **OSY** → **NET** → **DBS** (L00–L02, L07, L11, L14) → **DSY** → **TOC** → **PLC** → **PAR**

## Blockchain

Mục tiêu: BCH, SEC:L07-L10 · **104 bài** · ✓ 104

**FND** → **PYT** (L00–L07) → **DMS** (L00–L07, L09–L10, L13–L15, L19) → **CS112** (L00–L01, L03–L05) → **CS115** (L00–L01, L13) → **CPR** (L00) → **CSA** (L00–L02, L05–L08, L10, L13–L15) → **OSY** (L00–L01, L04–L06, L08–L09, L12, L14) → **NET** (L00–L02, L09, L12–L14) → **SWF** (L00–L01, L08–L09) → **DBS** (L00–L02, L11) → **SEC** (L00, L04, L07–L10) → **DSY** (L00, L03–L05) → **DSC** (L00–L02, L13) → **BCH**

## Kỹ sư Backend ngân hàng (Java / Spring Boot)

Mục tiêu: BNK, BNX, SPB, INT, ACB, SEP, CAS:L05 · **210 bài** · ✓ 197

**FND** → **JVA** → **JV2** → **PYT** (L00–L08) → **BNK** → **BNX** → **SPB** → **INT** → **ACB** → **DMS** (L00–L07, L09–L10, L19) → **CS115** (L00–L03, L05–L09, L12–L14, L17–L21) → **CPR** (L00) → **CSA** (L00–L02, L05–L08, L10, L14–L15) → **OSY** (L00–L01, L08–L09, L12, L14) → **SWF** (L00–L01, L03–L04, L06, L11) → **DBS** (L00–L02) → **CLD** (L00–L02, L05, L08) → **DVO** (L00–L01, L03–L04, L07) → **DSC** (L00–L02, L13) → **SEP** → **CAS** (L00, L05)

## Kỹ sư Backend nền tảng và kiến trúc hệ thống

Mục tiêu: BEP, DBS, SEC, DSY, EVT, CLD, SAR, DVO, SEP, CAS · **373 bài** · ✓ 350

**FND** → **JVA** → **JV2** → **PYT** (L00–L07) → **BNK** → **BNX** (L00–L04, L08–L31) → **SPB** → **BEP** → **DMS** (L00–L10, L13–L15, L19) → **CS112** (L00–L08, L12–L13, L16, L23) → **CS115** (L00–L03, L05–L09, L12–L15, L17–L21, L44) → **CPR** (L00) → **CSA** (L00–L08, L10, L13–L15) → **OSY** (L00–L01, L04–L06, L08–L09, L12, L14) → **NET** (L00–L02, L05, L09, L12–L14) → **SWF** (L00–L01, L03–L07, L11–L12) → **SDP** (L00–L07, L14) → **DBS** → **SEC** → **WEB** (L00, L03, L06, L12–L14) → **DSY** → **CLD** → **DVO** → **SAR** → **DEN** (L00, L04, L08–L13) → **EVT** → **DSC** (L00–L10, L13–L14) → **MLO** (L00–L02, L05–L06, L08–L09) → **TOC** (L00–L03) → **SEP** → **CAS**

## Kỹ sư AI ứng dụng, MLOps và kiểm thử chất lượng AI

Mục tiêu: CS115, AIF, DSC, MLP, MLO, LLM, AGT, AIP, SEP, CAS:L10 · **264 bài** · ✓ 258

**FND** → **PYT** (L00–L09) → **DMS** (L00–L10, L16–L19) → **CS112** (L00–L08, L14, L16, L18, L24) → **CS115** → **CPR** (L00) → **CSA** (L00–L03, L05–L08, L10, L13–L15) → **OSY** (L00–L01, L08–L09, L12, L14) → **NET** (L00–L01, L09, L12) → **SWF** (L00–L01, L03–L06, L11–L12) → **SDP** (L00–L01) → **DBS** (L00–L02, L07–L09) → **SEC** (L00–L06) → **DSY** (L00) → **CLD** (L00–L03, L05, L08, L10–L11) → **DVO** (L00–L01, L03–L04, L07) → **AIF** → **DSC** → **MLP** → **MLO** → **LLM** → **AGT** → **AIP** → **SEP** → **CAS** (L00, L10)
