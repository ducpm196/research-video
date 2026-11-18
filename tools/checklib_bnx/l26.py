"""BNX L26 — Maven, Gradle và Jenkins: mô hình tham chiếu của luật phân giải phiên bản (Maven: gần nhất thắng, cùng độ sâu thì khai báo trước thắng;
Gradle: phiên bản cao nhất), thứ tự các pha dựng mặc định, số máy dựng cần có (công thức hàng đợi). Chỉ thư viện chuẩn, không mạng.
Kiểm độc lập ở audit/bnx/ver/l26.py (chạy THẬT Maven 3.9.11: dependency:tree, package, dựng hai lần so sha256; Groovy parse cho Jenkinsfile/build.gradle)."""

BNX_L26_PHASES = ["resources", "compile", "testResources", "testCompile", "test", "jar"]


def bnx_l26_phases():
    return list(BNX_L26_PHASES)


def _so(v):
    return tuple(int(p) for p in v.split("."))


def bnx_l26_maven(du_an, cay):
    """du_an: [(tên, bản)] theo thứ tự khai; cay: {(tên, bản): [(tên, bản)…]}. Duyệt theo độ sâu, thư viện nào đã chọn thì bỏ yêu cầu sau."""
    chon, hang = {}, list(du_an)
    while hang:
        ten, ban = hang.pop(0)
        if ten in chon:
            continue
        chon[ten] = ban
        hang += cay.get((ten, ban), [])
    return chon


def bnx_l26_gradle(du_an, cay):
    """Luật mặc định của Gradle: trong mọi yêu cầu lấy phiên bản cao nhất (không dải, không strictly)."""
    chon, hang = {}, list(du_an)
    while hang:
        ten, ban = hang.pop(0)
        if ten in chon and _so(chon[ten]) >= _so(ban):
            continue
        chon[ten] = ban
        hang += cay.get((ten, ban), [])
    return chon


def bnx_l26_agents(builds_per_hour, minutes_per_build, parallel_per_agent=1):
    """Số máy dựng tối thiểu (làm tròn lên) để hàng đợi không dài thêm mãi: khối lượng phút dựng mỗi giờ chia cho 60 phút của mỗi máy."""
    return -(-builds_per_hour * minutes_per_build // (60 * parallel_per_agent))


BNX_L26_PHA_MUC_TIEU = [("process-resources", "resources:resources"), ("compile", "compiler:compile"),
                        ("process-test-resources", "resources:testResources"), ("test-compile", "compiler:testCompile"),
                        ("test", "surefire:test"), ("package", "jar:jar")]


def bnx_l26_phase_goals():
    """Sáu pha của vòng đời mặc định (gói jar) có mục tiêu của phần mở rộng gắn vào, theo thứ tự chạy. Pha khác mục tiêu."""
    return list(BNX_L26_PHA_MUC_TIEU)


def bnx_l26_phase_count():
    """Số pha của vòng đời mặc định từ validate tới package (17); chỉ 6 pha có mục tiêu gắn vào với gói jar."""
    return 17
