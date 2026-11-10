# Nguồn đã đọc nguyên văn cho BCH L12 (bài hành trình: nâng cấp một chuỗi khối đang chạy, 2008 → 2022)

Đọc ngày 2026-11-02 bằng curl (+ pdftotext cho PDF, gỡ thẻ HTML cho trang web). Mọi trang dưới đây trả mã 200, không trang nào bị chặn.
Chỉ trích các câu bài giảng dựa vào (CITED); mọi con số khác trong bài là phép tính lại (VER, `checks` của bài và
`audit/bch/verify_bch.py` L12) hoặc ghi rõ “(số minh hoạ)”. Không nêu tên cá nhân trong lời đọc; tên tác giả chỉ ở `source:`.
Nội dung an ninh (tính dễ sửa mã giao dịch, tấn công đảo khối) chỉ ở mức khái niệm phòng thủ. Không có lời khuyên đầu tư, không nói giá.

Hành trình theo ROADMAP §8.1 mục 3 (Bitcoin 2008 → SegWit 2017 → Ethereum chuyển sang bằng chứng cổ phần 2022). Nguồn ứng viên của ROADMAP
(sách trắng, BIP 141, ethereum.org) đều đọc được; thêm BIP 9, BIP 91 và ba trang của bitcoincore.org để có năm kích hoạt và cơ chế triển khai.

## [N08] S. Nakamoto, *Bitcoin: A Peer-to-Peer Electronic Cash System* (sách trắng, 2008)
Tải: https://bitcoin.org/bitcoin.pdf (184 292 byte, pdftotext -layout). Văn bản PDF không ghi ngày phát hành; năm 2008 lấy từ câu
“as of 2008” trong mục 7 và từ curriculum/bch.yaml (đã dùng ở bài 6). Bài nói “năm 2008”, không nói ngày.
- Abstract: “the main benefits are lost if a trusted third party is still required to prevent double-spending. We propose a solution to the
  double-spending problem using a peer-to-peer network.”
- Abstract: “As long as a majority of CPU power is controlled by nodes that are not cooperating to attack the network, they'll generate the
  longest chain and outpace attackers.”
- Mục 4: “the proof-of-work difficulty is determined by a moving average targeting an average number of blocks per hour. If they're
  generated too fast, the difficulty increases.”
- Mục 7: “A block header with no transactions would be about 80 bytes. If we suppose blocks are generated every 10 minutes,
  80 bytes * 6 * 24 * 365 = 4.2MB per year. With computer systems typically selling with 2GB of RAM as of 2008, and Moore's Law predicting
  current growth of 1.2GB per year, storage should not be a problem even if the block headers must be kept in memory.”
- Mục 8: “It is possible to verify payments without running a full network node. A user only needs to keep a copy of the block headers of
  the longest proof-of-work chain … and obtain the Merkle branch linking the transaction to the block it's timestamped in.”
- Mục 8: “the verification is reliable as long as honest nodes control the network, but is more vulnerable if the network is overpowered by
  an attacker.” “Businesses that receive frequent payments will probably still want to run their own nodes for more independent security
  and quicker verification.”

## [B141] BIP 141, *Segregated Witness (Consensus layer)* — Status: Deployed; Assigned: 2015-12-21
Tải: https://raw.githubusercontent.com/bitcoin/bips/master/bip-0141.mediawiki (26 314 byte; cùng nội dung trang github.com/bitcoin/bips).
- Abstract: “This BIP defines a new structure called a "witness" that is committed to blocks separately from the transaction merkle tree.
  … In particular, scripts and signatures are moved into this new structure.” “… for the purpose of making this BIP soft fork compatible.”
- Motivation: “Nonintentional malleability becomes impossible. Since signature data is no longer part of the transaction hash, changes to
  how the transaction was signed are no longer relevant to transaction identification.”
- Motivation: “Size of witness could be ignored / discounted when calculating the block size, effectively increasing the block size to some
  extent”.
- Block size: “Blocks are currently limited to 1,000,000 bytes (1MB) total size. … Block weight is defined as Base size * 3 + Total size.”
  “The new rule is block weight ≤ 4,000,000.”
- Sigops: “Sigops per block is currently limited to 20,000. … The sigop limit is likewise quadrupled to ≤ 80,000.”
- Backward compatibility: “As a soft fork, older software will continue to operate without modification. Non-upgraded nodes, however, will
  not see nor validate the witness data and will consider all witness programs as anyone-can-spend scripts … Wallets should always be wary
  of anyone-can-spend scripts and treat them with suspicion.” “What a non-upgraded wallet cannot do: Validating segregated witness
  transaction. It assumes such a transaction is always valid”.
- New script semantics: “developers should test the scripts on testnet with the default relay policy turned on, and with a small amount of
  money after BIP141 is activated on mainnet.”
- Deployment: “This BIP will be deployed by "version bits" BIP9 with the name "segwit" and using bit 1. For Bitcoin mainnet, the BIP9
  starttime will be midnight 15 November 2016 UTC … and BIP9 timeout will be midnight 15 November 2017 UTC”.

## [B9] BIP 9, *Version bits with timeout and delay*
Tải: https://raw.githubusercontent.com/bitcoin/bips/master/bip-0009.mediawiki (14 058 byte).
- “These are tallied each retarget period.” “The threshold is ≥1916 blocks (95% of 2016), or ≥1512 for testnet (75% of 2016).”
- “LOCKED_IN for one retarget period after the first retarget period with STARTED blocks of which at least threshold have the associated bit
  set in nVersion.” “ACTIVE for all blocks after the LOCKED_IN retarget period.” “FAILED for one retarget period past the timeout time, if
  LOCKED_IN was not reached.”

## [B91] BIP 91, *Reduced threshold Segwit MASF* — Status: Deployed; Assigned: 2017-05-22
Tải: https://raw.githubusercontent.com/bitcoin/bips/master/bip-0091.mediawiki (6 634 byte).
- Abstract: “This document specifies a method to activate the existing BIP9 segwit deployment with a majority hashpower less than 95%.”
- Specification: “While this BIP is active, all blocks must set the nVersion header top 3 bits to 001 together with bit field (1<<1) …
  Blocks that do not signal as required will be rejected.”
- Deployment: “with an 80%(this can be adjusted if desired) 269 block activation threshold and 336 block confirmation window”; “start time of
  midnight June 1st, 2017”; mã tham chiếu: “nOverrideMinerConfirmationWindow = 336; // ~2.33 days”.
- “This BIP will cease to be active when segwit (BIP141) is locked-in, active, or failed”.

## [BC16] bitcoincore.org: *Bitcoin Core 0.13.1 Released* (2016-10-27); *Segregated Witness Benefits* (2016-01-26); *Segwit next steps* (2016-06-24)
Tải: https://bitcoincore.org/en/2016/10/27/release-0.13.1/, https://bitcoincore.org/en/2016/01/26/segwit-benefits/,
https://bitcoincore.org/en/2016/06/24/segwit-next-steps/ (curl, 200).
- 0.13.1: “Linear scaling of sighash operations to ensure that transactions using segwit can’t trigger the problem that caused a block in 2015
  to take 25 seconds to validate.”
- 0.13.1: “if all wallets switch to using segwit, the network will be able to support about 70% more transactions.”
- 0.13.1: “each byte of a segregated witness is given a weight of 1, each other byte in a block is given a weight of 4”.
- 0.13.1: “May 2016 marked the activation of segwit on Bitcoin’s testnet.” “As of the Bitcoin Core 0.13.1 release, segwit has been activated
  for over six months on testnet with no known consensus failures.”
- 0.13.1: “The segwit soft fork is fully backwards compatible with all Bitcoin wallets”.
- Benefits: “for certain transactions, signature-hashing scales quadratically rather than linearly. … This has been seen in the wild, where an
  individual block required 25 seconds to validate, and maliciously designed transactions could take over 3 minutes.”
- Next steps: “Lock-in: once 95% of blocks in a 2,016-block long retarget period have signaled …” “Activation: 2,016 blocks (about two weeks)
  after segwit is locked-in, it will activate.”

## [BC17] bitcoincore.org: *Segregated Witness Wallet Development Guide*; *Correcting misinformation on Segwit2x and btc1* (2017-08-18)
Tải: https://bitcoincore.org/en/segwit_wallet_dev/ và https://bitcoincore.org/en/2017/08/18/btc1-misleading-statements/ (curl, 200).
- Guide, mục Activation: “As of block height 481824, all SegWit ready nodes started enforcing the new SegWit consensus rules.”
- Bài 2017-08-18: “Segregated Witness (or Segwit, a soft fork which will be active within the coming days)” — căn cứ cho “kích hoạt năm 2017”
  (bài không nói ngày kích hoạt; số khối 481 824 lấy từ Guide).

## [E22] ethereum.org: *The Merge* (roadmap/merge, cập nhật trang 2026-05-15)
Tải: https://ethereum.org/en/roadmap/merge/ (curl, 200).
- “The Merge was executed on September 15, 2022. This completed Ethereum's transition to proof-of-stake consensus, officially deprecating
  proof-of-work and reducing energy consumption by ~99.95%.”
- “Proof-of-work secured Ethereum Mainnet from genesis until The Merge. This allowed the Ethereum blockchain … come into existence in
  July 2015”.
- “On December 1, 2020, the Beacon Chain was created as a separate blockchain to Mainnet, running in parallel. The Beacon Chain was not
  originally processing Mainnet transactions.”
- Ẩn dụ của trang: “it became time to hot-swap the new engine for the old one mid-flight.”
- “No history was lost in The Merge.” “you do not need to do anything with your funds or wallet to account for The Merge. … There is no such
  thing as "old ETH"/"new ETH" … people telling you otherwise are likely scammers.”
- “a full Ethereum node now requires both an execution client and a consensus client.”
- Misconceptions: “The Merge was a change of consensus mechanism, not an expansion of network capacity, and was never intended to lower gas
  fees.” “transaction speed is mostly the same on layer 1 now as it was before The Merge.” “Historically, on proof-of-work, the target was to
  have a new block every ~13.3 seconds. Under proof-of-stake, slots occur precisely every 12 seconds … blocks are produced ~10% more
  frequently than on proof-of-work.”
- “blocks are bundled into epochs (6.4 minute spans of time containing 32 chances for blocks) … If validators agree to justify the epoch, it
  gets finalized in the next epoch. Undoing finalized transactions is economically inviable as it would require obtaining and burning over
  one-third of the total staked ETH.”
- “Validator exits are rate limited for security reasons. … approximately 0.33% of total ETH staked can be exited from the network in a
  single day.”
- “The Merge upgrade did not include certain anticipated features such as the ability to withdraw staked ETH. This functionality was enabled
  separately with the Shanghai/Capella upgrade.”

## [E22e] ethereum.org: *Ethereum energy consumption* (cập nhật trang 2026-07-28)
Tải: https://ethereum.org/en/energy-consumption/ (curl, 200).
- “Ethereum's energy consumption is approximately ~0.0026 TWh/yr … The estimate for Ethereum comes from a CCRI … study.” “The estimated
  2,601 MWh (0.0026 TWh)”.
- Bảng (nguồn truy cập 7/2023): “PoW Ethereum 21 8,100x” và “PoS Ethereum 0.0026 1x”.
- “CCRI estimates that The Merge reduced Ethereum's annualized electricity consumption by more than 99.988%.”
- “The stats on this page are estimates based on publicly available data - they do not represent an official statement or promise”.
- “a proof-of-work mechanism was used to get the network started.” “From the very beginning, Ethereum planned to implement a proof-of-stake
  based consensus mechanism, but doing so without sacrificing security and decentralization took years of focused research and development.”

## [E22p] ethereum.org: *Proof-of-stake (PoS)* (developers/docs/consensus-mechanisms/pos)
Tải: https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/ (curl, 200).
- “To participate as a validator, a user must deposit 32 ETH into the deposit contract”.
- “Time in proof-of-stake Ethereum is divided into slots (12 seconds) and epochs (32 slots). One validator is randomly selected to be a block
  proposer in every slot.”
- “If a pair of checkpoints attracts votes representing at least two-thirds of the total staked ETH, the checkpoints are upgraded.”
- “To revert a finalized block, an attacker would commit to losing at least one-third of the total supply of staked ETH.”
- “an attacker could prevent the network from reaching finality by voting with one-third of the total stake. There is a mechanism to defend
  against this: the inactivity leak. This activates whenever the chain fails to finalize for more than four epochs.”
- “Two primary behaviors can be considered dishonest: proposing multiple blocks in a single slot (equivocating) and submitting contradictory
  attestations.” “an immediate penalty (1/4096 of the validator's effective balance, up to 0.5 ETH) on Day 1, the correlation penalty on
  Day 18, and finally, ejection from the network on Day 36.”

## [E25] Pectra/Electra — thêm 2026-11-08 khi đọc kiểm (con số 0,33% của [E22] là cách tính TRƯỚC Pectra)
Tải bằng WebFetch, truy cập 2026-11-08: https://ethereum.org/en/roadmap/pectra/ (no revision given) và
https://raw.githubusercontent.com/ethereum/consensus-specs/master/specs/electra/beacon-chain.md (nhánh master, no revision given).
- Pectra: “This upgrade was successfully activated on Ethereum mainnet at epoch 364032, on 07-May-2025 at 10:05 (UTC).”; EIP-7251 “raises
  the maximum possible effective balance to 2048 ETH”.
- Electra spec: “MAX_PER_EPOCH_ACTIVATION_EXIT_CHURN_LIMIT | Gwei(2**8 * 10**9) (= 256,000,000,000)”; “MIN_PER_EPOCH_CHURN_LIMIT_ELECTRA |
  Gwei(2**7 * 10**9)”; “MIN_SLASHING_PENALTY_QUOTIENT_ELECTRA | uint64(2**12) (= 4,096)” (khớp “1/4096 … up to 0.5 ETH” của [E22p]:
  2048 / 4096 = 0,5); `get_activation_exit_churn_limit` = min(MAX_PER_EPOCH_ACTIVATION_EXIT_CHURN_LIMIT, get_balance_churn_limit(state)).
- VER: 86 400 / 384 = 225 kỷ nguyên mỗi ngày; 225 · 256 = 57 600 ETH mỗi ngày là trần rút. Bài KHÔNG đổi ra phần trăm (tổng cổ phần hiện
  tại không có nguồn đã đọc) — chỉ nói “tỉ lệ còn thấp hơn khi tổng cổ phần lớn”. Bài giữ 0,33% / 303 ngày như con số của trang chính thức,
  ghi rõ là cách tính cũ.

## [CS] ethereum/consensus-specs (nhánh master, truy cập 2026-11-09, no revision given) — thêm khi đọc kiểm lần ba (BN-0038)
Tải bằng curl: specs/phase0/beacon-chain.md, specs/altair/beacon-chain.md, specs/bellatrix/beacon-chain.md, specs/electra/beacon-chain.md.
- phase0: “`MIN_EPOCHS_TO_INACTIVITY_PENALTY` | `Epoch(2**2)` (= 4)”; `is_in_inactivity_leak`: “return get_finality_delay(state) > MIN_EPOCHS_TO_INACTIVITY_PENALTY”.
- altair `get_inactivity_penalty_deltas`: “Return the inactivity penalty deltas by considering timely target participation flags and inactivity
  scores.” — phạt mọi người xác thực `not in matching_target_indices` (không có cờ TIMELY_TARGET ở kỷ nguyên trước); `process_inactivity_updates`:
  “Increase the inactivity score of inactive validators”. → Bị rút dần là bên KHÔNG bỏ phiếu đúng hạn cho điểm mốc của chuỗi này (vắng mặt
  hoặc bỏ phiếu cho nhánh khác), không phải “bên bỏ phiếu ngược đa số” nói chung. Câu L12 stage5 đã sửa theo đây (BN-0038).
- bellatrix: “`MIN_SLASHING_PENALTY_QUOTIENT_BELLATRIX` | `Uint64(2**5)` (= 32)”; electra: “`MIN_SLASHING_PENALTY_QUOTIENT_ELECTRA` | `Uint64(2**12)`
  (= 4,096)”. → mức phạt ngày đầu 1/4096 của [E22p] là mức từ Pectra/Electra (7/5/2025); từ Hợp nhất (Bellatrix) tới đó là 1/32. Bài ghi cả hai.

## Con số tính lại (VER — `checks` của bài và audit/bch/verify_bch.py L12)
- 80 · 6 · 24 · 365 = 4 204 800 byte ≈ 4,2 MB mỗi năm (khớp [N08]); 2 · 10⁹ byte (2 GB) chia 4 204 800 ≈ 475 năm tiêu đề.
- Giao dịch 250 byte có 100 byte chữ ký (SỐ MINH HOẠ): trọng lượng 3 · 150 + 250 = 700; 4 000 000 / 700 ≈ 5714 giao dịch, hơn 4000 khoảng 43 %
  (khác “about 70%” của [BC16] vì tỉ lệ phụ thuộc phần chữ ký — bài nói rõ).
- 2016 − 1916 + 1 = 101 khối không báo tín hiệu là đủ để một chu kỳ không khoá (mô phỏng trong verify_bch.py).
- Khối toàn dữ liệu cũ (không nhân chứng): base = total = 1 000 000 → weight = 3 · 1 000 000 + 1 000 000 = 4 000 000 = giới hạn mới.
- Khối minh hoạ base 700 000 + nhân chứng 800 000: total 1 500 000, weight 2 100 000 + 1 500 000 = 3 600 000 ≤ 4 000 000.
- 20 000 · 4 = 80 000 (sigops gấp bốn).
- 1916 / 2016 ≈ 95,04 %; 269 / 336 ≈ 80,06 %; 336 · 10 phút = 3360 phút = 2,33 ngày; 2016 · 10 phút = 14 ngày.
- 481 824 = 239 · 2016 (khối kích hoạt nằm đúng ở đầu một chu kỳ 2016 khối, như quy tắc chuyển trạng thái của [B9]).
- 1/12/2020 → 15/9/2022 = 653 ngày chạy song song.
- 32 · 12 = 384 giây = 6,4 phút; 13,3 / 12 ≈ 1,108 (khớp “~10%”).
- 21 / 0,0026 ≈ 8077 (bảng làm tròn 8 100); 1 − 0,0026 / 21 ≈ 99,9876 % — làm tròn ba chữ số thập phân là 99,988 %.
- 32 / 4096 = 0,0078125 ETH (phạt tức thì với số dư hiệu dụng 32 — dưới trần 0,5).
- 100 phần cổ phần: ≥ 2/3 → 67 phần; đảo ngược cần mất ≥ 1/3 → hơn 33 phần (nối bài 7).

## Điều KHÔNG dạy (nguồn không ghi hoặc không đọc)
- Ngày phát hành sách trắng (31/10/2008) và ngày khối đầu: PDF không ghi → chỉ nói “năm 2008”.
- Ngày (lịch) kích hoạt SegWit: [BC17] chỉ cho số khối 481 824 và bài 18/8/2017 “active within the coming days” → bài nói “năm 2017, ở khối
  481 824”, không nói ngày. Cũng không dạy diễn biến tỉ lệ tín hiệu theo tháng, BIP 148 (không đọc), tranh cãi Segwit2x hay sự ra đời của
  đồng tiền tách ra năm 2017 (chính trị cộng đồng, ngoài phạm vi; bài 2017-08-18 có nhắc nhưng không dạy).
- Chi tiết khai thác tính dễ sửa mã giao dịch hay tấn công đảo khối: không dạy (phòng thủ). Chỉ dạy: “đổi cách ký có thể đổi mã giao dịch”.
- Năng lượng của Bitcoin theo năm, giá, lợi suất đặt cọc (APR): không dạy (không lời khuyên đầu tư); bảng [E22e] chỉ dùng hai dòng của
  Ethereum.
- Hai con số giảm năng lượng (~99,95 % ở trang Merge, > 99,988 % theo CCRI ở trang năng lượng) là hai ƯỚC TÍNH khác nhau; bài nêu cả hai và
  dạy “đọc nguồn của con số”, không chọn một con số là đúng.
- Thời gian chốt thực tế (khoảng hai kỷ nguyên ≈ 12,8 phút) suy ra từ câu “gets finalized in the next epoch” và 6,4 phút mỗi kỷ nguyên —
  ghi “khoảng” và là INFERRED; ethereum.org không ghi con số 12,8.
- Sharding / lộ trình sau 2022 ngoài “Shanghai/Capella cho rút cổ phần”: không dạy chi tiết; ngày của bản nâng cấp đó không có trong [E22] → không nói.
