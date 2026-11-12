"""BNX L17 — Spring Security và Spring Cloud: mô hình tham chiếu của chuỗi bộ lọc (vị trí trạm, trạm nào chặn, mã trạng thái)
và của cổng chia tải xoay vòng trên các bản dịch vụ qua kiểm sức khoẻ. Chỉ thư viện chuẩn, không mạng.
Kiểm độc lập ở audit/bnx/ver/l17.py (chạy THẬT Spring Security 7.1.2 và so với mô hình này; đếm xoay vòng bằng đường khác)."""

# Thứ tự trạm do Spring Security 7.1.2 dựng cho cấu hình của bài (in ra bằng FilterChainProxy.getFilters; TramQuanSat là trạm bài thêm).
BNX_L17_CHAIN = ["DisableEncodeUrlFilter", "WebAsyncManagerIntegrationFilter", "SecurityContextHolderFilter", "HeaderWriterFilter",
                 "CsrfFilter", "LogoutFilter", "OAuth2ProtectedResourceMetadataFilter", "BearerTokenAuthenticationFilter", "TramQuanSat",
                 "RequestCacheAwareFilter", "SecurityContextHolderAwareRequestFilter", "AnonymousAuthenticationFilter",
                 "ExceptionTranslationFilter", "AuthorizationFilter"]
_SAFE = {"GET", "HEAD", "TRACE", "OPTIONS"}


def bnx_l17_pos(name):
    """Vị trí (từ 1) của một trạm trong chuỗi."""
    return BNX_L17_CHAIN.index(name) + 1


def bnx_l17_chain_len():
    return len(BNX_L17_CHAIN)


def bnx_l17_trace(method, token, need):
    """Lần theo một yêu cầu. token: None hoặc {'sig': bool, 'expired': bool, 'scopes': [..]}. need: quyền mà đường dẫn đòi.
    Trả (mã trạng thái, tên trạm quyết định, có đi qua trạm quan sát không, có tới dịch vụ không)."""
    if method not in _SAFE and token is None:
        return 403, "CsrfFilter", False, False            # lệnh ghi không kèm mã chống giả mạo: chặn ở trạm 5
    if token is not None and (not token["sig"] or token["expired"]):
        return 401, "BearerTokenAuthenticationFilter", False, False
    if token is None:
        return 401, "ExceptionTranslationFilter", True, False   # trạm quyền ném lỗi, trạm dịch lỗi thấy khách vô danh
    if need is not None and need not in token["scopes"]:
        return 403, "ExceptionTranslationFilter", True, False   # đã biết là ai, thiếu quyền
    return 200, None, True, True


def bnx_l17_status(method, token, need):
    return bnx_l17_trace(method, token, need)[0]


def bnx_l17_authorities(scope_claim):
    """Trường scope 'a b' → ['SCOPE_a', 'SCOPE_b'] (máy chủ tài nguyên thêm tiền tố)."""
    return ["SCOPE_" + s for s in scope_claim.split()]


def bnx_l17_round_robin(health, n):
    """health: danh sách True/False theo thứ tự đăng ký; n yêu cầu chia xoay vòng cho các bản khoẻ.
    Trả danh sách số yêu cầu từng bản nhận (bản trượt nhận 0)."""
    alive = [i for i, h in enumerate(health) if h]
    cnt = [0] * len(health)
    if not alive:
        return cnt
    q, r = divmod(n, len(alive))
    for j, i in enumerate(alive):
        cnt[i] = q + (1 if j < r else 0)
    return cnt


def bnx_l17_stale_window(check_interval_s, cache_ttl_s):
    """Cận trên (giây) một bản đã chết còn nhận yêu cầu: chờ lần kiểm sức khoẻ kế + danh sách đệm ở bên gọi còn sống."""
    return check_interval_s + cache_ttl_s


def bnx_l17_lost(rate_per_s, health_total, seconds):
    """Số yêu cầu rơi vào MỘT bản chết trong `seconds` giây khi bên gọi vẫn chia đều cho health_total bản."""
    return rate_per_s * seconds // health_total
