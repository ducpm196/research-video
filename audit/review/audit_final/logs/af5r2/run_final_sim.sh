#!/usr/bin/env bash
# Tái hiện mô phỏng dãy chặng của plan_AF5_20261123T0110Z.md mục 5.1 (CHỈ ĐỌC). Chạy từ gốc kho.
# Kết quả mong đợi: cỡ chặng 49/16/40/19/77/70/83/101/165/81/76; "cạnh THẬT trỏ sang chặng sau: 0"; 1 lời hẹn lệch (CS115:L21, hết khi có next:).
D='drop=DVO:L07<DSC:L08 drop=SDP:L12<PLC:L07 drop=SDP:L12<PLC:L12 drop=SEC:L13<DSC:L11 drop=SWF:L08<TOC:L01 drop=WEB:L01<TOC:L06 drop=WEB:L03<PLC:L07 drop=WEB:L06<SAR:L09 drop=WEB:L08<SAR:L04 drop=WEB:L12<ESY:L13 drop=WEB:L13<DSY:L02 drop=DEN:L12<DSC:L02 drop=AIF:L02<RBM:L15 drop=CVI:L03<ROB:L11 drop=CVI:L12<PAR:L13 drop=CAS:L01<ESY:L06 drop=CAS:L04<ESY:L10 drop=SEC:L14<DVO:L10 drop=WEB:L14<DVO:L07'
.venv/Scripts/python -B audit/review/audit_final/logs/af5r2/stage_explicit.py add=S05/CS115:L45-L46 rm=S09/CS115 add=S09/CS115:L22-L43 "move=DVO:S07>S08" $D \
  prefer=FND,JVA,JV2,PYT,BNK,BNX,INT,ACB,DMS,CS112,CS115,CPR,LNX,CSA,OSY,NET,SWF,SDP,DBS,SEC,WEB,DSY,CLD,DVO,SAR,DEN,EVT,CLC,AIF,DSC,DAN,MLP,MLO,LLM,AGT,RLN,IRS,CVI,TOC,PLC,PAR,HCI,SEP,CAS,RBM,ESY,ROB,GFX,BCH,PRJ
