import lib2
from lib2 import *
from l16 import _spoken  # ghép câu quá ngắn vào câu bên cạnh, giữ focus
from libj import jstep, nowrap
from labkit import write_lab, practice_steps, practice_scene

lib2.begin("L27")

# ── Mã chạy THẬT: JDK 21 thuần (com.sun.net.httpserver, java.net.http, javax.xml) cho SOAP; Python 3 (hashlib, os.rename) cho tệp lô ──
# SFTP thật cần máy chủ SSH (máy này không có sshd): phần truyền tệp là MÔ PHỎNG bằng hai thư mục cục bộ, ghi rõ trên màn hình;
# phần THẬT là toàn vẹn (sha256), đổi tên nguyên tử, tệp dở dang, đối soát số dòng. Đầu ra tất định (đệm ở audit/bnx/progcache/L27.json).
X_REQ = prog("YeuCau", r'''
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:ns="urn:bank">
  <soapenv:Body>
    <ns:LaySoDu>
      <ns:soTaiKhoan>001</ns:soTaiKhoan>
    </ns:LaySoDu>
  </soapenv:Body>
</soapenv:Envelope>
''', lang="xml", kind="other", reason="Phong bì SOAP gửi đi; chương trình SoapDemo đọc đúng tệp này và gửi qua HTTP thật tới máy chủ cục bộ.",
    read_check="Phân tích được bằng XML (ElementTree, có không gian tên) và gửi nguyên văn bởi SoapDemo.java trong nguồn L27_ChaySoap (đầu ra thật khớp từng dòng).")

X_WSDL = prog("Wsdl", r'''
<definitions name="Bank" targetNamespace="urn:bank"
    xmlns="http://schemas.xmlsoap.org/wsdl/"
    xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
    xmlns:tns="urn:bank" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <message name="LaySoDuIn"><part name="soTaiKhoan" type="xsd:string"/></message>
  <message name="LaySoDuOut"><part name="soDu" type="xsd:long"/></message>
  <portType name="BankPort">
    <operation name="LaySoDu">
      <input message="tns:LaySoDuIn"/>
      <output message="tns:LaySoDuOut"/>
    </operation>
  </portType>
  <binding name="BankBinding" type="tns:BankPort">
    <soap:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>
  </binding>
  <service name="BankService">
    <port name="BankPort" binding="tns:BankBinding">
      <soap:address location="http://localhost:8080/bank"/>
    </port>
  </service>
</definitions>
''', lang="xml", kind="other", reason="Tệp WSDL mô tả dịch vụ: kiểu dữ liệu, thông điệp, thao tác, ràng buộc giao thức, địa chỉ. Rút gọn (không có mô tả các thao tác ràng buộc chi tiết).",
    read_check="Phân tích được bằng XML (DOM có không gian tên) trong nguồn L27_ChaySoap: đếm đúng các phần tử message, portType, operation, binding, service. Không kiểm sinh mã khách từ WSDL (JDK 21 không còn công cụ wsimport).")

J_SOAP = prog("SoapDemo", r'''
import com.sun.net.httpserver.*;
import java.io.*;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import javax.xml.parsers.*;
import org.w3c.dom.*;
public class SoapDemo {
  static final String NS = "http://schemas.xmlsoap.org/soap/envelope/";
  static final String WSDL = "http://schemas.xmlsoap.org/wsdl/";
  static String phong(String than) {
    return "<soapenv:Envelope xmlns:soapenv=\"" + NS + "\">"
        + "<soapenv:Body>" + than + "</soapenv:Body></soapenv:Envelope>";
  }
  static String loi(String ma, String ct) {
    return phong("<soapenv:Fault><faultcode>" + ma + "</faultcode>"
        + "<faultstring>" + ct + "</faultstring></soapenv:Fault>");
  }
  static Document doc(String xml, boolean chan) throws Exception {
    var f = DocumentBuilderFactory.newInstance();
    f.setNamespaceAware(true);
    if (chan) f.setFeature(
        "http://apache.org/xml/features/disallow-doctype-decl", true);
    var in = new ByteArrayInputStream(xml.getBytes(StandardCharsets.UTF_8));
    return f.newDocumentBuilder().parse(in);
  }
  static String lay(String xml, String ten) throws Exception {
    var n = doc(xml, false).getElementsByTagNameNS("*", ten);
    return n.getLength() == 0 ? "" : n.item(0).getTextContent();
  }
  static String soTk(String vao) throws Exception {
    var n = doc(vao, true).getElementsByTagNameNS("*", "soTaiKhoan");
    return n.item(0).getTextContent();
  }
  static String xuLy(String vao, int[] ma) {
    try {
      if (soTk(vao).equals("001"))
        return phong("<ns:LaySoDuResponse xmlns:ns=\"urn:bank\">"
            + "<ns:soDu>1250000</ns:soDu></ns:LaySoDuResponse>");
      ma[0] = 500;
      return loi("soapenv:Client", "khong co so tai khoan");
    } catch (Exception e) {
      ma[0] = 400;
      return loi("soapenv:Client", "XML khong hop le hoac co DOCTYPE");
    }
  }
  static String gui(int cong, String xml) throws Exception {
    var u = URI.create("http://localhost:" + cong + "/bank");
    var rq = HttpRequest.newBuilder(u)
        .header("Content-Type", "text/xml; charset=utf-8")
        .header("SOAPAction", "urn:bank#LaySoDu")
        .POST(HttpRequest.BodyPublishers.ofString(xml)).build();
    var rs = HttpClient.newHttpClient().send(rq,
        HttpResponse.BodyHandlers.ofString());
    return rs.statusCode() + "|" + rs.body();
  }
  public static void main(String[] a) throws Exception {
    var sv = HttpServer.create(new InetSocketAddress("localhost", 0), 0);
    sv.createContext("/bank", h -> {
      String vao = new String(h.getRequestBody().readAllBytes(),
          StandardCharsets.UTF_8);
      int[] ma = {200};
      byte[] b = xuLy(vao, ma).getBytes(StandardCharsets.UTF_8);
      h.getResponseHeaders().add("Content-Type", "text/xml; charset=utf-8");
      h.sendResponseHeaders(ma[0], b.length);
      h.getResponseBody().write(b);
      h.close();
    });
    sv.start();
    int cong = sv.getAddress().getPort();
    String xml = Files.readString(Path.of("yeu_cau.xml"));
    String[] r = gui(cong, xml).split("\\|", 2);
    String js = "{\"soTaiKhoan\":\"001\"}", jt = "{\"soDu\":1250000}";
    System.out.println("yeu cau SOAP " + xml.length()
        + " byte, JSON tuong duong " + js.length() + " byte");
    System.out.println("tra loi " + r[0] + ": soDu " + lay(r[1], "soDu")
        + ", SOAP " + r[1].length() + " byte, JSON " + jt.length() + " byte");
    r = gui(cong, xml.replace(">001<", ">999<")).split("\\|", 2);
    System.out.println("tra loi " + r[0] + ": " + lay(r[1], "faultcode")
        + ", " + lay(r[1], "faultstring"));
    String xxe = "<?xml version=\"1.0\"?><!DOCTYPE x [<!ENTITY e SYSTEM "
        + "\"file:///etc/passwd\">]>" + xml;
    r = gui(cong, xxe).split("\\|", 2);
    System.out.println("tra loi " + r[0] + " khi yeu cau co DOCTYPE: "
        + lay(r[1], "faultstring"));
    var w = doc(Files.readString(Path.of("bank.wsdl")), false);
    String[] ten = {"message", "portType", "operation", "binding", "service"};
    StringBuilder sb = new StringBuilder("WSDL:");
    for (String t : ten)
      sb.append(" ").append(t).append(" ")
          .append(w.getElementsByTagNameNS(WSDL, t).getLength());
    System.out.println(sb);
    sv.stop(0);
  }
}
''', lang="java", kind="other", reason="SoapDemo.java: máy chủ SOAP tối giản bằng com.sun.net.httpserver và khách bằng java.net.http (JDK 21 thuần).",
    read_check="Biên dịch và chạy trong nguồn L27_ChaySoap cùng yeu_cau.xml và bank.wsdl; khớp từng ký tự đầu ra.")

SH_SOAP = prog("ChaySoap", r'''
javac -encoding UTF-8 SoapDemo.java
java -Dstdout.encoding=UTF-8 SoapDemo
''', lang="bash", files={"SoapDemo.java": "SoapDemo", "yeu_cau.xml": "YeuCau", "bank.wsdl": "Wsdl"}, timeout=120,
    claims=["yêu cầu SOAP hợp lệ trả 200 với soDu 1250000", "số tài khoản lạ trả 500 với Fault soapenv:Client", "yêu cầu có DOCTYPE bị từ chối",
            "tệp WSDL có 2 message, 1 portType, 1 operation, 1 binding, 1 service"])

# ── Tệp lô: Python thật (SFTP là mô phỏng bằng hai thư mục) ──
PY_GUI = prog("GuiLo", r'''
import hashlib, os, tempfile

def tao_lo(so_dong):
    dong = [f"{i:04d}|TK{i % 7:03d}|{i * 1000}" for i in range(1, so_dong + 1)]
    noi_dung = "\n".join(dong) + "\n"
    ma = hashlib.sha256(noi_dung.encode()).hexdigest()
    return noi_dung + f"TRAILER|{so_dong}|{ma}\n"

def gui(thu_muc, ten, noi_dung):
    tam = os.path.join(thu_muc, ten + ".part")
    with open(tam, "w") as f:
        f.write(noi_dung)
    os.rename(tam, os.path.join(thu_muc, ten))      # đổi tên nguyên tử

with tempfile.TemporaryDirectory() as nhan:
    lo = tao_lo(1000)
    gui(nhan, "lo1.csv", lo)
    open(os.path.join(nhan, "lo2.csv.part"), "w").write(lo[:300])   # đang gửi dở
    print("nguoi nhan thay:", sorted(f for f in os.listdir(nhan) if not f.endswith(".part")))
    print("tep dang gui do (bo qua):", [f for f in os.listdir(nhan) if f.endswith(".part")])
''', lang="python", claims=["người nhận chỉ lấy tệp đã đổi tên xong; tệp .part bị bỏ qua"])

PY_KIEM = prog("KiemLo", r'''
import hashlib

def tao_lo(so_dong):
    dong = [f"{i:04d}|TK{i % 7:03d}|{i * 1000}" for i in range(1, so_dong + 1)]
    nd = "\n".join(dong) + "\n"
    return nd + f"TRAILER|{so_dong}|{hashlib.sha256(nd.encode()).hexdigest()}\n"

def kiem(noi_dung):
    dong = noi_dung.rstrip("\n").split("\n")
    _, so, ma = dong[-1].split("|")
    du_lieu = "\n".join(dong[:-1]) + "\n"
    if len(dong) - 1 != int(so):
        return "THIEU DONG"
    if hashlib.sha256(du_lieu.encode()).hexdigest() != ma:
        return "SAI MA BAM"
    return "OK"

lo = tao_lo(1000)
cat = "\n".join(lo.split("\n")[:900] + lo.split("\n")[-2:])      # mất 100 dòng, giữ trailer
hong = lo.replace("0500|TK003|500000", "0500|TK003|500001")       # đổi 1 chữ số
print("nguyen ven:", kiem(lo))
print("mat 100 dong:", kiem(cat))
print("doi 1 chu so:", kiem(hong))
''', lang="python", claims=["tệp nguyên vẹn OK; mất 100 dòng báo THIEU DONG; đổi 1 chữ số báo SAI MA BAM (số dòng vẫn đủ)"])

PY_QUYMO = prog("QuyMoLo", r'''
import hashlib

for n in (1000, 1000000):
    h, byte, khoi = hashlib.sha256(), 0, 0
    buf = bytearray()
    for i in range(1, n + 1):
        buf += f"{i:08d}|TK{i % 1000:04d}|{i * 7 % 1000000:07d}\n".encode()
        if len(buf) >= 65536:
            h.update(buf[:65536]); byte += 65536; khoi += 1; del buf[:65536]
    if buf:
        h.update(buf); byte += len(buf); khoi += 1
    print(f"{n} dong: {byte} byte, {khoi} khoi 64 KiB, sha256 {h.hexdigest()[:12]}")
''', lang="python", timeout=180, claims=["10^3 dòng: 24 000 byte, 1 khối; 10^6 dòng: 24 000 000 byte, 367 khối; băm theo luồng"])

# ── Lab (cham.sh, Python) ──
LAB_PY = r'''
import hashlib


def kiem(noi_dung):
    dong = noi_dung.rstrip("\n").split("\n")
    _, so, ma = dong[-1].split("|")
    du_lieu = "\n".join(dong[:-1]) + "\n"
    if len(dong) - 1 != int(so):
        return "THIEU DONG"
    if hashlib.sha256(du_lieu.encode()).hexdigest() != ma:
        return "SAI MA BAM"
    return "OK"


def lo(dong):
    nd = "\n".join(dong) + "\n"
    return nd + f"TRAILER|{len(dong)}|{hashlib.sha256(nd.encode()).hexdigest()}\n"


dong = ["A01|100", "A02|200", "A03|300", "A04|400", "A05|500"]
tot = lo(dong)
thieu = tot.replace("A05|500\n", "")
sai = tot.replace("A03|300", "A03|301")
rong = tot.split("TRAILER")[0] + "TRAILER|5|" + "0" * 64 + "\n"
print("lo tot:", kiem(tot))
print("lo thieu mot dong:", kiem(thieu))
print("lo sai mot chu so:", kiem(sai))
print("lo co trailer gia:", kiem(rong))
'''
LAB_OUT = """lo tot: OK
lo thieu mot dong: THIEU DONG
lo sai mot chu so: SAI MA BAM
lo co trailer gia: SAI MA BAM"""
LAB_DE = """# Lab BNX L27 — Đối soát tệp lô: số dòng và mã băm

Tệp lô có dạng: các dòng dữ liệu, rồi **một dòng cuối** `TRAILER|<số dòng dữ liệu>|<sha256 của toàn bộ phần dữ liệu>` (dữ liệu = mọi dòng trước trailer, mỗi dòng kết thúc bằng xuống dòng). Mã băm là sha256 của dữ liệu đã mã hoá UTF-8, ghi dạng hex chữ thường (`hexdigest()` của `hashlib`).

Viết `mau.py` có hàm `kiem(noi_dung)` trả `"THIEU DONG"` khi số dòng dữ liệu khác số ghi ở trailer, trả `"SAI MA BAM"` khi số dòng đủ nhưng sha256 không khớp, ngược lại trả `"OK"`.
Kiểm theo thứ tự: số dòng trước, mã băm sau. Rồi tự dựng 5 dòng dữ liệu `A01|100` … `A05|500` (số minh hoạ) cùng trailer đúng, và in 4 dòng:

1. `lo tot: …` (lô đúng)   2. `lo thieu mot dong: …` (bỏ dòng `A05|500` nhưng giữ trailer cũ)   3. `lo sai mot chu so: …` (đổi `A03|300` thành `A03|301`)   4. `lo co trailer gia: …` (trailer ghi đúng 5 dòng nhưng mã băm toàn số 0)

Chạy: `python mau.py`. Chấm: `bash labs/cham.sh BNX L27 mau.py`.
"""


def build():
    write_lab("BNX", "L27", LAB_DE, "py", LAB_PY, LAB_OUT)
    hook = sc("hook", "hook", "Hệ cũ nói XML, đối tác gửi tệp lô: ba chỗ ngân hàng hay vấp", [
        st("""<p>Một ngân hàng nối với hệ thống cũ của đối tác: hỏi số dư bằng <b>phong bì XML</b>, và nhận bảng kê đêm bằng <b>tệp lô</b> gửi qua kênh mã hoá. Chạy thật ba ca:</p>
<div class="box key">Mã trạng thái của HTTP: <b>200</b> thành công, <b>400</b> yêu cầu sai, <b>500</b> máy chủ báo lỗi. Hỏi tài khoản có thật: trả <b>200</b>, số dư 1 250 000. Hỏi tài khoản lạ: trả <b>500</b> kèm phần lỗi. Gửi yêu cầu có khai báo loại văn bản cài bẫy: bị <b>400</b>.
Còn tệp lô: người nhận mở một tệp <b>đang gửi dở</b>, hoặc thiếu 100 dòng mà không ai biết. Làm sao tránh?</div>""",
           """Chào bạn, một ngân hàng nối với hệ thống cũ của đối tác: hỏi số dư bằng phong bì XML, nhận bảng kê đêm bằng tệp lô qua kênh mã hoá. Chạy thật ba ca. Tài khoản có thật trả mã hai trăm, thành công, số dư một triệu hai trăm năm mươi nghìn. Tài khoản lạ trả năm trăm, máy chủ báo lỗi. Yêu cầu cài bẫy bị bốn trăm, yêu cầu sai. Còn tệp lô, người nhận có thể mở tệp gửi dở, hoặc thiếu một trăm dòng mà không ai biết. Làm sao để tránh?""", focus=[1, 1, [1], 2, 2, 2]),
    ], checks=["alg.bnx_l27_soap_status('001', False) == 200 and alg.bnx_l27_soap_status('999', False) == 500 and alg.bnx_l27_soap_status('001', True) == 400",
               "alg.bnx_l27_batch_check(1000, 1000, True) == 'OK'"])

    pre = sc("prereq", "prereq", "Trước hết: sáu điều cần hiểu", [
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["① XML", "chữ có thẻ mở/đóng lồng nhau; <b>không gian tên</b> (namespace) gắn một địa chỉ làm nhãn cho cả bộ thẻ", "<code>&lt;ns:soDu&gt;1250000&lt;/ns:soDu&gt;</code>"],
                  ["② dịch vụ phong bì (<b>SOAP</b>)", "bên gọi gửi một <b>phong bì</b> XML bằng <b>HTTP POST</b> (kiểu yêu cầu gửi kèm dữ liệu, khác GET chỉ xin lấy), nhận lại phong bì", "phong bì có <b>thân</b> chứa lệnh; lỗi nằm trong <b>phần lỗi</b>"],
                  ["③ tệp mô tả dịch vụ (WSDL)", "tệp XML mô tả dịch vụ có những thao tác nào, nhận và trả gì, ở địa chỉ nào", "máy đọc được, sinh mã khách"]]),
           """Trước hết ta cần hiểu sáu điều. XML là chữ có thẻ mở và đóng lồng nhau, không gian tên gắn một địa chỉ làm nhãn cho bộ thẻ. Dịch vụ phong bì là bên gọi gửi một phong bì XML bằng lệnh gửi của HTTP và nhận lại một phong bì. Tệp mô tả dịch vụ là tệp XML nói dịch vụ có thao tác nào, ở địa chỉ nào.""",
           focus=[0, "1.2", "1.3", "1.4"], introduces=["bnx_soap"]),
        st(table(["khái niệm", "nghĩa", "ví dụ"],
                 [["④ mã băm (sha256)", "dãy ký tự cố định sinh từ nội dung; đổi một ký tự thì mã băm khác hẳn", "ghi ở dòng cuối của tệp lô"],
                  ["⑤ tệp lô và <b>SFTP</b>", "<b>tệp lô</b>: tệp <code>.csv</code>, mỗi dòng một bản ghi, các cột ngăn bằng một dấu; <b>SFTP</b>: truyền tệp qua kênh <b>SSH</b> (đường nối mã hoá giữa hai máy) (bài này mô phỏng bước truyền bằng thư mục cục bộ)","bảng kê đêm <code>lo.csv</code> nhận lúc 3 giờ sáng"],
                  ["⑥ đổi tên nguyên tử", "đổi tên tệp là một thao tác trọn vẹn: người khác thấy tên cũ hoặc tên mới, không thấy giữa chừng", "ghi <code>lo.csv.part</code> rồi đổi thành <code>lo.csv</code>"]]),
           """Mã băm là dãy ký tự cố định sinh từ nội dung, đổi một ký tự thì khác hẳn. Tệp lô là tệp bảng chữ, mỗi dòng một bản ghi, thường gửi qua kênh truyền tệp trên đường nối mã hoá giữa hai máy. Đổi tên nguyên tử là đổi tên tệp trọn vẹn, không ai thấy giữa chừng.""",
           focus=["1.2", "1.3", "1.4"], clear=True, introduces=["bnx_sftp"]),
    ], checks=["alg.bnx_l27_sha_len() == 64"])

    sym = sc("sym", "symbol", "Giải mã các tên trên màn hình", [
        st(table(["tên", "nghĩa"],
                 [["<code>Envelope</code>, <code>Body</code>", "<b>phong bì</b> và <b>thân</b>: lệnh gửi đi nằm trong thân"],
                  ["<code>Fault</code>", "<b>phần lỗi</b> thay cho kết quả: có <code>faultcode</code> (loại lỗi) và <code>faultstring</code> (lời mô tả)"],
                  ["<code>SOAPAction</code>", "đầu mục HTTP ghi thao tác định gọi"],
                  ["<code>message</code>, <code>portType</code>, <code>operation</code>, <code>binding</code>, <code>service</code>", "trong WSDL: thông điệp, nhóm thao tác, một thao tác, cách đóng gói qua giao thức, dịch vụ và địa chỉ"],
                  ["<code>DOCTYPE</code>", "khai báo loại văn bản ở đầu XML; có thể khai <b>thực thể ngoài</b> (nội dung lấy từ tệp khác), nguồn của tấn công <b>XXE</b>: đọc trộm tệp của máy chủ"],
                  ["<code>TRAILER|n|mã</code>", "dòng cuối tệp lô: <b>n</b> dòng dữ liệu và <b>mã băm</b> của phần dữ liệu"]]),
           """Lệnh gửi đi nằm trong thân của phong bì, còn phần lỗi thay cho kết quả, gồm loại lỗi và lời mô tả. Đầu mục HTTP ghi thao tác định gọi, và tệp mô tả dịch vụ có thông điệp, nhóm thao tác, cách đóng gói, dịch vụ và địa chỉ. Khai báo loại văn bản có thể khai thực thể ngoài, nguồn của kiểu tấn công đọc trộm tệp máy chủ. Dòng cuối tệp lô ghi số dòng và mã băm.""",
           focus=[["1.2", "1.3"], ["1.4", "1.5"], "1.6", "1.7"], introduces=["bnx_xxe"]),
        st(table(["viết trong mã", "đọc là", "ví dụ nhỏ"],
                 [["<code>type=\"xsd:string\"</code>, <code>message=\"tns:LaySoDuIn\"</code>", "<code>xsd:</code> và <code>tns:</code> là tiền tố không gian tên, khai ở đầu tệp bằng <code>xmlns:…</code>; <code>xsd:string</code> là kiểu chuỗi chuẩn; <code>tns:LaySoDuIn</code> trỏ tới thông điệp <code>LaySoDuIn</code> của chính dịch vụ này", "<code>xsd:long</code> là kiểu số nguyên lớn"],
                  ["<code>style=\"rpc\"</code>", "kiểu <b>gọi hàm từ xa</b>: mỗi thao tác như một hàm có tên và đối số", "<code>LaySoDu(\"001\")</code>"],
                  ["<code>javac -encoding UTF-8 SoapDemo.java</code>", "<code>javac</code> biên dịch tệp Java; <code>-encoding UTF-8</code> báo tệp có chữ có dấu; <code>java</code> chạy lớp đã biên dịch; <code>-Dstdout.encoding=UTF-8</code> đặt thuộc tính để in chữ có dấu", "<code>java SoapDemo</code> chạy lớp <code>SoapDemo</code>"]]),
           """Mã sắp tới có vài chỗ cần đọc trước. Chữ đứng trước dấu hai chấm là tiền tố không gian tên. Kiểu gọi hàm từ xa coi mỗi thao tác như một hàm có đối số. Lệnh đầu biên dịch tệp Java, lệnh sau chạy lớp đã biên dịch.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
        st(table(["viết trong mã", "đọc là", "ví dụ nhỏ"],
                 [["<code>f\"{i:08d}|TK{i % 1000:04d}\"</code>", "chuỗi f: <code>{…}</code> chèn giá trị; <code>:08d</code> là số nguyên đủ 8 chữ số, đệm số 0 bên trái; <code>%</code> là phần dư của phép chia", "<code>f\"{7:03d}\"</code> là <code>007</code>; <code>1234 % 1000</code> là <code>234</code>"],
                  ["<code>buf = bytearray()</code>, <code>buf += …</code>, <code>del buf[:65536]</code>", "<code>bytearray</code>: vùng byte sửa được; <code>+=</code> nối thêm vào cuối; <code>del buf[:n]</code> xoá <code>n</code> byte đầu", "<code>[:3]</code> là 3 phần tử đầu, <code>[-1]</code> là phần tử cuối"],
                  ["<code>with open(tam, \"w\") as f:</code>, <code>dong[-1].split(\"|\")</code>", "<code>with</code> mở tệp để ghi và tự đóng khi hết khối; <code>split(\"|\")</code> tách chuỗi thành danh sách theo dấu <code>|</code>", "<code>\"a|b\".split(\"|\")</code> là <code>[\"a\", \"b\"]</code>"]]),
           """Với tệp lô, chuỗi đặt trước chữ f chèn giá trị trong ngoặc nhọn, số tám chữ số đệm số không, và dấu phần trăm là phần dư. Vùng byte sửa được cho nối thêm và xoá đầu. Khối mở tệp tự đóng tệp, và hàm tách chia chuỗi theo dấu gạch đứng.""",
           focus=["1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_l27_sha_len() == 64"])

    intu = sc("intuition", "intuition", "Hình dung: một lời gọi phong bì, và đường đi của tệp lô", [
        st(svg(1500, 520,
               txt(750, 40, "Một lời gọi theo giao thức phong bì: HTTP POST mang phong bì XML", 26, "middle", "#1f2937", True),
               box(40, 120, 300, 130, ["khách", "gửi phong bì", "LaySoDu 001"], C_GRAY, 22, True),
               box(560, 90, 380, 190, ["máy chủ", "1 chặn khai báo loại văn bản", "2 lấy soTaiKhoan trong thân", "3 tra số dư"], C_BLUE, 22, True),
               box(1160, 120, 300, 130, ["trả phong bì", "200: soDu", "500: Fault"], C_GREEN, 22, True),
               arrow(345, 185, 555, 185, "#475569", "POST /bank", 22), arrow(945, 185, 1155, 185),
               box(40, 340, 500, 90, ["phong bì mẫu viết liền: 203 byte", "JSON tương đương: 20 byte"], C_AMBER, 22),
               box(600, 340, 500, 90, ["trả lời mẫu viết liền: 211 byte", "JSON tương đương: 16 byte"], C_AMBER, 22),
               txt(750, 480, "Đánh đổi: hợp đồng chặt, lỗi có cấu trúc, nhưng phong bì nặng khoảng mười lần JSON (đo thật, viết liền)", 24, "middle", "#1f2937", True)),
           """Hình này là một lời gọi theo giao thức phong bì: khách gửi phong bì XML tới máy chủ bằng lệnh gửi của HTTP. Máy chủ chặn khai báo loại văn bản cài bẫy, lấy số tài khoản trong thân, rồi tra số dư. Đánh đổi là hợp đồng chặt, và phong bì mẫu viết liền nặng hai trăm linh ba byte so với hai mươi byte của JSON, khoảng mười lần.""",
           ),
        st(svg(1500, 520,
               txt(750, 40, "Tệp lô: người nhận chỉ thấy tệp đã xong, rồi tự kiểm bằng dòng cuối", 26, "middle", "#1f2937", True),
               box(40, 120, 280, 90, ["bên gửi", "ghi lo.csv.part"], C_GRAY, 22),
               box(420, 120, 280, 90, ["đổi tên nguyên tử", "→ lo.csv"], C_AMBER, 22, True),
               box(800, 120, 320, 90, ["bên nhận: bỏ qua *.part", "chỉ lấy lo.csv"], C_BLUE, 22),
               box(1200, 120, 260, 90, ["kiểm dòng cuối", "TRAILER|n|mã"], C_GREEN, 22, True),
               arrow(325, 165, 415, 165), arrow(705, 165, 795, 165), arrow(1125, 165, 1195, 165),
               box(40, 290, 440, 90, ["mất dòng → số dòng ≠ n", "THIEU DONG"], C_RED, 22),
               box(540, 290, 440, 90, ["đổi một chữ số → mã băm lệch", "SAI MA BAM"], C_RED, 22),
               box(1040, 290, 420, 90, ["đủ dòng, đúng mã băm", "OK"], C_GREEN, 22),
               txt(750, 440, "Kênh mã hoá (SFTP) lo bí mật đường truyền; việc toàn vẹn của tệp là do ta kiểm", 24, "middle", "#1f2937", True),
               txt(750, 490, "MÔ PHỎNG: không có máy chủ SSH, bước truyền tệp là hai thư mục cục bộ; đổi tên, số dòng, mã băm là THẬT", 24, "middle", "#b45309", True)),
           """Hình thứ hai là tệp lô: bên gửi ghi tệp đuôi dở dang rồi đổi tên nguyên tử thành tên thật, bên nhận chỉ lấy tệp đã xong rồi kiểm dòng cuối. Mất dòng thì số dòng khác số ghi, đổi một chữ số thì mã băm lệch. Kênh mã hoá lo bí mật của đường truyền, còn toàn vẹn là việc ta tự kiểm.""",
           ),
    ], checks=["203 / 20 > 10 and 211 / 16 > 13"])

    form = sc("formula", "formula", "Suy ra từng bước: từ phong bì tới tệp lô an toàn", [
        st("""<p><b>Bước 1.</b> Muốn hai hệ thống khác nhau hiểu nhau, hai bên phải đồng ý một <b>dạng thông điệp</b> cố định. Giao thức phong bì dùng XML: <code>Envelope</code> bọc <code>Body</code>, lệnh nằm trong thân, kèm không gian tên để khỏi nhầm tên thẻ.</p>"""
           + X_REQ.show(lines=(1, 8), title="yeu_cau.xml: phong bì gửi đi"),
           """Bước một, muốn hai hệ thống khác nhau hiểu nhau, nên hai bên phải đồng ý một dạng thông điệp cố định.
           Giao thức phong bì dùng XML: phong bì bọc thân, lệnh nằm trong thân, kèm không gian tên để khỏi nhầm tên thẻ. Phong bì này hỏi số dư tài khoản không không một.""",
           clear=True),
        st("""<p><b>Bước 2. Mô tả bằng WSDL.</b> Để bên kia khỏi đoán, dịch vụ công bố một tệp mô tả: <code>message</code> (dữ liệu vào, ra), <code>portType</code> (nhóm thao tác), <code>binding</code> (cách đóng gói qua HTTP), <code>service</code> (địa chỉ).</p>"""
           + X_WSDL.show(lines=(5, 16), title="bank.wsdl (trích: hai message, một portType, một operation, một binding, mở đầu service)"),
           """Bước hai là mô tả: để bên kia khỏi đoán, dịch vụ công bố một tệp mô tả. Nó gồm hai thông điệp cho dữ liệu vào và ra, nhóm thao tác, ràng buộc cho cách đóng gói, và khối dịch vụ cho địa chỉ. Bài chỉ đếm phần tử, nên không sinh mã khách.""", focus=[[1], 2, 3],
           clear=True),
        st("""<p><b>Bước 3. Lỗi có cấu trúc.</b> Khi không tra được tài khoản, máy chủ không trả một dòng chữ mà trả <b>phần lỗi</b> trong phong bì (<code>faultcode</code>, <code>faultstring</code>), để máy bên kia xử lý được. Máy chủ thử trong bài trả HTTP <b>500</b> cho lỗi nghiệp vụ và <b>400</b> cho XML không hợp lệ: đó là điều đã <b>đo</b>.
Đặc tả chính thức quy định mã HTTP nào cho phần lỗi thì bài <b>chưa kiểm được</b> (NOT_VERIFIED: máy chủ w3.org chặn tải), nên không khẳng định.</p>"""
           + table(["tình huống", "mã HTTP của máy chủ thử", "nội dung"],
                   [["tài khoản có thật", "200", "soDu 1250000"],
                    ["tài khoản lạ", "500", "faultcode soapenv:Client"],
                    ["có khai báo loại văn bản", "400", "XML không hợp lệ"]]),
           """Bước ba là lỗi có cấu trúc: không tra được tài khoản thì máy chủ trả phần lỗi ngay trong phong bì, nên máy bên kia xử lý được. Máy chủ thử trả năm trăm cho lỗi nghiệp vụ và bốn trăm cho XML sai, đó là điều đã đo. Đặc tả chính thức quy định mã nào thì bài chưa kiểm được, nên ta không khẳng định.""",
           clear=True),
        jstep([(('<code>var f = DocumentBuilderFactory.newInstance();</code>',
                 'Java: <code>var</code> để máy tự suy kiểu của biến; <code>newInstance()</code> tạo bộ cấu hình cho bộ đọc XML; câu kết thúc bằng dấu chấm phẩy',
                 'Tạo bộ cấu hình cho bộ đọc XML, biến được máy tự suy kiểu.'), '<code>f</code> là bộ cấu hình', ''),
               (('<code>f.setNamespaceAware(true);</code>',
                 'bật chế độ hiểu không gian tên: <code>true</code> là bật',
                 'Bật chế độ hiểu không gian tên.'), '', ''),
               (('<code>if (chan) f.setFeature("…disallow-doctype-decl", true);</code>',
                 '<code>if (đk) câu;</code>: chỉ làm câu sau khi điều kiện đúng; <code>chan</code>: tham số đúng/sai của hàm chứa đoạn này; <code>setFeature(tên, true)</code> bật tính năng có tên cho trước, ở đây là cấm khai báo loại văn bản',
                 'Nếu tham số chặn đúng thì bật tính năng cấm khai báo loại văn bản, nên thực thể ngoài không được đọc.'), '', '')]),
        st("""<p><b>Bước 4. Chặn XML độc.</b> Một yêu cầu có thể mở đầu bằng khai báo loại văn bản, khai một <b>thực thể ngoài</b> trỏ tới tệp trên máy chủ. Nếu bộ phân tích làm theo, máy chủ bị đọc trộm tệp. Cách phòng được hướng dẫn của OWASP (tổ chức về an toàn ứng dụng web) nêu: <b>cấm khai báo loại văn bản</b> khi phân tích.</p>"""
           + code("""var f = DocumentBuilderFactory.newInstance();
f.setNamespaceAware(true);
if (chan) f.setFeature(
    "http://apache.org/xml/features/disallow-doctype-decl", true);""", "SoapDemo.java (trích, rút gọn)"),
           """Bước bốn là chặn XML độc: yêu cầu có thể mở đầu bằng khai báo loại văn bản, khai một thực thể ngoài trỏ tới tệp trên máy chủ. Nếu bộ phân tích làm theo, máy chủ bị đọc trộm tệp. Cách phòng theo hướng dẫn về an toàn ứng dụng web là cấm khai báo loại văn bản, như đoạn mã vừa xem.""", focus=[[1], 2, 3],
           clear=True),
        jstep([(('<code>def gui(thu_muc, ten, noi_dung):</code>',
                 'khai hàm Python tên <code>gui</code> với ba tham số; các dòng thụt vào là thân hàm',
                 'Khai hàm gửi tệp với ba tham số.'), '', ''),
               (('<code>os.path.join(thu_muc, ten + ".part")</code>',
                 '<code>os.path.join</code> ghép thư mục với tên thành đường dẫn; <code>+</code> nối thêm đuôi <code>.part</code> vào tên',
                 'Ghép thư mục với tên thành đường dẫn, dấu cộng nối thêm đuôi tạm.'), '', ''),
               (('<code>with open(tam, "w") as f:</code>, <code>f.write(noi_dung)</code>',
                 '<code>open(tam, "w")</code> mở tệp để ghi (<code>"w"</code>: write); <code>f.write(…)</code> ghi chữ vào tệp; <code>with</code> tự đóng tệp khi hết khối',
                 'Mở tệp để ghi và ghi nội dung vào; khối mở tệp tự đóng tệp.'), '', ''),
               (('<code>os.rename(tam, đường_dẫn_mới)</code>',
                 'đổi tên tệp <code>tam</code> thành tên mới trong một thao tác trọn vẹn',
                 'Đổi tên tệp tạm thành tên thật, nên người khác không thấy giữa chừng.'), '', '')]),
        st("""<p><b>Bước 5. Tệp lô: đổi tên nguyên tử.</b> Bên gửi ghi vào <code>lo.csv.part</code>, ghi xong mới đổi tên thành <code>lo.csv</code>. Bên nhận chỉ xử lý tên không đuôi <code>.part</code>, nên không bao giờ mở tệp đang ghi dở.</p>"""
           + PY_GUI.show(lines=(9, 13), title="GuiLo.py (trích): ghi vào tên tạm rồi đổi tên"),
           """Bước năm là đổi tên nguyên tử cho tệp lô: bên gửi ghi vào tệp tên tạm, ghi xong mới đổi thành tên thật. Bên nhận chỉ xử lý tệp không mang đuôi tạm, nên không bao giờ mở tệp đang ghi dở.""", focus=[1, 3],
           clear=True),
        st("""<p><b>Bước 6. Tệp lô: đối soát.</b> Dòng cuối ghi <b>n</b> dòng dữ liệu và <b>sha256</b> của phần dữ liệu. Bên nhận kiểm theo thứ tự: số dòng trước (rẻ), mã băm sau. Mất dòng thì lệch n; đổi một chữ số thì lệch mã băm dù số dòng vẫn đủ.</p>"""
           + """$$\\text{đủ } n \\text{ dòng và } \\text{sha256}(\\text{dữ liệu}) = \\text{mã ghi ở cuối} \\;\\Rightarrow\\; \\text{nhận}$$""",
           """Bước sáu là đối soát: dòng cuối ghi số dòng dữ liệu và mã băm của phần dữ liệu. Bên nhận kiểm số dòng trước vì rẻ, mã băm sau, vì mất dòng thì lệch số dòng, đổi một chữ số thì lệch mã băm.""", focus=[[1], 2],
           clear=True),
    ], checks=["alg.bnx_l27_batch_check(1000, 900, True) == 'THIEU DONG'", "alg.bnx_l27_batch_check(1000, 1000, False) == 'SAI MA BAM'",
               "alg.bnx_l27_soap_status('999', False) == 500"])

    ex = sc("example", "example", "Ví dụ chạy thật, từng phép tính", [
        st(SH_SOAP.show(lines=(1, 2), title="Chạy thật: biên dịch rồi chạy SoapDemo (máy chủ HTTP và khách của JDK, cổng tự chọn)"),
           """Ta chạy thật bằng JDK hai mươi mốt thuần. Chương trình dựng một máy chủ HTTP nhỏ, rồi dùng khách HTTP gửi ba yêu cầu, đọc phong bì và tệp mô tả vừa xem.""",
           clear=True),
        st(SH_SOAP.out_html("""yeu cau SOAP 246 byte, JSON tuong duong 20 byte
tra loi 200: soDu 1250000, SOAP 211 byte, JSON 16 byte""")
           + """<p class="note">246 là tệp thụt dòng; viết liền (bỏ dấu cách đầu dòng và xuống dòng giữa các thẻ) còn 203, cùng cách viết liền với JSON và phản hồi.</p>$$① \\; 203 : 20 \\approx 10{,}2 \\text{ lần}; \\qquad 211 : 16 \\approx 13{,}2 \\text{ lần}$$""",
           """Phép tính thứ nhất: yêu cầu hợp lệ nhận mã hai trăm và số dư một triệu hai trăm năm mươi nghìn. Tệp yêu cầu thụt dòng nặng hai trăm bốn mươi sáu byte, viết liền còn hai trăm linh ba, so với hai mươi byte của JSON là khoảng mười lần.""", focus=[[1], 2],
           clear=True),
        st(SH_SOAP.out_html("""tra loi 500: soapenv:Client, khong co so tai khoan
tra loi 400 khi yeu cau co DOCTYPE: XML khong hop le hoac co DOCTYPE""")
           + """$$② \\; \\text{tài khoản lạ} \\Rightarrow \\hl{500} \\text{ kèm Fault}; \\quad ③ \\; \\text{có khai báo loại văn bản} \\Rightarrow \\hl{400}$$""",
           """Phép tính thứ hai, tài khoản lạ nhận mã năm trăm với phần lỗi. Phép tính thứ ba, yêu cầu có khai báo loại văn bản cài thực thể ngoài bị từ chối ngay, nhận mã bốn trăm, và không tệp nào bị đọc.""",
           clear=True),
        st(SH_SOAP.out_html("WSDL: message 2 portType 1 operation 1 binding 1 service 1")
           + """$$④ \\; 2 \\text{ message} + 1 \\text{ portType} + 1 \\text{ operation} + 1 \\text{ binding} + 1 \\text{ service}$$""",
           """Phép tính thứ tư: bộ đọc XML đếm phần tử của tệp mô tả, ra hai thông điệp, một nhóm thao tác, một thao tác, một ràng buộc và một dịch vụ.""",
           clear=True),
        jstep([(('<code>with tempfile.TemporaryDirectory() as nhan:</code>',
                 'tạo một thư mục tạm tên <code>nhan</code>; hết khối <code>with</code> thì xoá thư mục',
                 'Tạo một thư mục tạm cho bên nhận, tự xoá khi hết khối.'), '', ''),
               (('<code>open(os.path.join(nhan, "lo2.csv.part"), "w").write(lo[:300])</code>',
                 'ghi 300 ký tự đầu của lô vào tệp <code>.part</code>: mô phỏng tệp đang gửi dở',
                 'Ghi ba trăm ký tự đầu vào tệp tạm, mô phỏng tệp gửi dở.'), '', ''),
               (('<code>sorted(f for f in os.listdir(nhan) if not f.endswith(".part"))</code>',
                 '<code>os.listdir</code> liệt kê tên tệp trong thư mục; giữ tên <b>không</b> kết thúc bằng <code>.part</code>; <code>sorted</code> xếp theo thứ tự chữ; dòng in sau lọc ngược lại, giữ tên có đuôi đó',
                 'Liệt kê tên tệp, giữ tên không có đuôi tạm rồi xếp theo thứ tự chữ.'), '', '')]),
        st(PY_GUI.show(lines=(15, 20), title="GuiLo.py (trích; tao_lo(n) dựng lô n dòng kèm TRAILER, định nghĩa ở đầu tệp): gửi một tệp xong và một tệp dở") + PY_GUI.out_html("""nguoi nhan thay: ['lo1.csv']
tep dang gui do (bo qua): ['lo2.csv.part']""")
           + """$$⑤ \\; \\text{tệp .part bị bỏ qua; chỉ lo1.csv được nhận}$$""",
           """Phép tính thứ năm là đổi tên nguyên tử: chương trình gửi một tệp đã xong và một tệp đang gửi dở. Người nhận chỉ thấy tệp đã đổi tên xong, còn tệp dở bị bỏ qua.""", focus=[1, 4],
           clear=True),
    ], checks=["round(203 / 20, 1) == 10.2 and round(211 / 16, 1) == 13.2", "alg.bnx_l27_soap_status('001', False) == 200",
               "alg.bnx_l27_wsdl_counts() == (2, 1, 1, 1, 1)"])

    chk = sc("check", "check", "Tự kiểm bằng đường khác: ba ca đối soát tệp lô", [
        jstep([(('<code>noi_dung.rstrip("\\n").split("\\n")</code>',
                 '<code>\\n</code> là ký tự xuống dòng; <code>rstrip</code> cắt xuống dòng ở cuối; <code>split</code> tách thành danh sách, mỗi dòng một phần tử',
                 'Cắt xuống dòng ở cuối, nên tách ra mỗi dòng một phần tử.'), '', ''),
               (('<code>_, so, ma = dong[-1].split("|")</code>',
                 '<code>dong[-1]</code>: phần tử cuối (dòng cuối); tách theo <code>|</code> thành ba phần gán vào ba tên; <code>_</code>: tên bỏ đi, giữ chỗ cho nhãn <code>TRAILER</code>',
                 'Tách dòng cuối thành ba phần; dấu gạch dưới giữ chỗ cho nhãn không dùng.'), '', ''),
               (('<code>"\\n".join(dong[:-1]) + "\\n"</code>',
                 '<code>dong[:-1]</code>: mọi dòng trừ dòng cuối; <code>join</code> nối chúng bằng xuống dòng; <code>+ "\\n"</code> thêm xuống dòng cuối: dựng lại đúng phần dữ liệu',
                 'Nối mọi dòng trừ dòng cuối bằng xuống dòng, dựng lại đúng phần dữ liệu.'), '', ''),
               (('<code>len(dong) - 1 != int(so)</code>',
                 '<code>len</code> đếm phần tử; trừ 1 để bỏ dòng cuối; <code>int</code> đổi chuỗi thành số; <code>!=</code>: khác nhau',
                 'Đếm số dòng trừ dòng cuối rồi so với số ghi ở dòng cuối.'), '', '')]),
        jstep([(('<code>hashlib.sha256(du_lieu.encode()).hexdigest()</code>',
                 '<code>encode</code> đổi chữ thành byte; <code>sha256</code> băm; <code>hexdigest</code> cho mã băm dạng chữ số hệ mười sáu',
                 'Đổi chữ thành byte, băm, lấy mã dạng chữ số hệ mười sáu.'), '', ''),
               (('<code>if … : return "THIEU DONG"</code>',
                 'điều kiện đúng thì trả kết quả ngay và thoát hàm; qua cả hai kiểm thì chạy tới <code>return "OK"</code>',
                 'Điều kiện đúng thì trả ngay và thoát hàm, nên qua cả hai kiểm mới tới kết quả tốt.'), '', '')]),
        st(PY_KIEM.show(lines=(8, 16), title="KiemLo.py (trích; tao_lo(n) dựng lô mẫu, ở đầu tệp): kiểm số dòng trước, mã băm sau"),
           """Hàm kiểm viết tay này tách dòng cuối, lấy số dòng và mã băm đã ghi. Nó so số dòng trước vì chỉ cần đếm, rồi mới băm phần dữ liệu và so với mã đã ghi.""", focus=[1, 2],
           clear=True),
        jstep([(('<code>"\\n".join(lo.split("\\n")[:900] + lo.split("\\n")[-2:])</code>',
                 'ghép hai danh sách bằng <code>+</code>: 900 phần tử đầu và hai phần tử cuối (dòng cuối và phần rỗng sau xuống dòng cuối); <code>join</code> nối lại thành chữ',
                 'Giữ chín trăm dòng đầu và dòng cuối, bỏ một trăm dòng ở giữa.'), '', ''),
               (('<code>lo.replace("0500|TK003|500000", "0500|TK003|500001")</code>',
                 '<code>replace</code> thay chuỗi cũ bằng chuỗi mới: ở đây đổi đúng một chữ số',
                 'Thay chuỗi cũ bằng chuỗi mới, đổi đúng một chữ số.'), '', '')]),
        st(PY_KIEM.show(lines=(18, 23), title="KiemLo.py (trích): ba ca thử"),
           """Ba ca thử là lô nguyên vẹn, lô cắt mất một trăm dòng nhưng giữ dòng cuối, và lô đổi một chữ số, nên mỗi ca thử đúng một lớp kiểm.""",
           clear=True),
        st(PY_KIEM.out_html("""nguyen ven: OK
mat 100 dong: THIEU DONG
doi 1 chu so: SAI MA BAM""") + table(["ca", "số dòng", "mã băm", "kết luận"],
                                    [["nguyên vẹn", "đủ 1000", "khớp", "OK"], ["mất 100 dòng", "chỉ 900", "(chưa cần kiểm)", "THIEU DONG"], ["đổi 1 chữ số", "đủ 1000", "lệch", "SAI MA BAM"]]),
           """Kết quả đúng như mong đợi vì mỗi ca bị đúng một lớp kiểm chặn: lô mất dòng bị báo ngay ở bước đếm, lô sai một chữ số bị báo sai mã băm.""",
           focus=[1, 3], clear=True),
    ], checks=["alg.bnx_l27_batch_check(1000, 1000, True) == 'OK'", "alg.bnx_l27_batch_check(1000, 900, True) == 'THIEU DONG'", "alg.bnx_l27_batch_check(1000, 1000, False) == 'SAI MA BAM'"])

    quymo = sc("quymo", "example", "Khi tệp lô lớn dần: đọc và băm theo luồng", [
        jstep([(('<code>for n in (1000, 1000000):</code>',
                 'vòng lặp qua dãy cho sẵn: <code>n</code> lần lượt là 1000 rồi 1000000',
                 'Vòng lặp qua hai cỡ tệp cho sẵn.'), '', ''),
               (('<code>h, byte, khoi = hashlib.sha256(), 0, 0</code>',
                 'gán ba biến một lúc: <code>h</code> là bộ băm còn trống, hai biến đếm bắt đầu từ 0; <code>h.update(x)</code> đưa thêm <code>x</code> vào bộ băm; <code>hexdigest()[:12]</code> lấy 12 ký tự đầu của mã',
                 'Gán ba biến một lúc: bộ băm trống và hai biến đếm.'), '', ''),
               (('<code>for i in range(1, n + 1):</code>',
                 '<code>range(1, n + 1)</code>: các số từ 1 tới n (dừng trước n + 1)',
                 'Vòng lặp chạy các số từ một tới n.'), '', ''),
               (('<code>h.update(buf[:65536]); byte += 65536; khoi += 1; del buf[:65536]</code>',
                 'dấu <code>;</code> ngăn các câu lệnh trên một dòng: băm khối đầu, cộng đếm byte và đếm khối, rồi xoá khối đó khỏi vùng đệm',
                 'Một dòng bốn việc: băm khối đầu, cộng hai bộ đếm, xoá khối đó khỏi vùng đệm.'), '', '')]),
        st(PY_QUYMO.show(lines=(3, 12), title="Đọc theo khối 64 KiB (1 KiB = 1024 byte, nên 65 536 byte), băm dần, không giữ cả tệp trong bộ nhớ"),
           """Số đo thật: chương trình sinh từng dòng vào vùng đệm, mỗi khi đủ một khối sáu mươi lăm nghìn năm trăm ba mươi sáu byte thì băm dần rồi bỏ khối đó.""",
           clear=True, introduces=["bnx_kib"]),
        st(PY_QUYMO.out_html()
           + """$$10^3 \\to 10^6 \\text{ dòng } (\\times 1000): \\; 24\\,000 \\to 24\\,000\\,000 \\text{ byte}; \\;\\; 1 \\to 367 \\text{ khối}$$""",
           """Mỗi dòng dài hai mươi bốn byte, nên một nghìn dòng là hai mươi bốn nghìn byte, vừa một khối. Một triệu dòng, gấp một nghìn lần, là hai mươi bốn triệu byte và ba trăm sáu mươi bảy khối, và đọc từng khối rồi băm dần thì bộ nhớ không đổi.""", focus=[1, 3],
           clear=True),
        st(table(["cách", "bộ nhớ", "khi nào gãy", "chọn khi"],
                 [["đọc cả tệp vào bộ nhớ rồi băm", "tỉ lệ với cỡ tệp: 24 MB ở 10⁶ dòng, 24 GB ở 10⁹ dòng", "tệp lớn hơn bộ nhớ trống", "tệp nhỏ, đơn giản"],
                  ["đọc và băm theo luồng", "gần như không đổi (một khối 64 KiB)", "không gãy theo cỡ tệp; thời gian tăng tuyến tính", "tệp lô thật của ngân hàng"],
                  ["chia tệp thành nhiều phần có mã băm riêng", "không đổi, và gửi lại từng phần được", "phải quản lý danh sách phần", "tệp rất lớn, mạng hay đứt"]]),
           """Bảng này cho thấy giải pháp cũ gãy ở đâu. Đọc cả tệp vào bộ nhớ cần bộ nhớ tỉ lệ cỡ tệp, hai mươi bốn tỉ byte ở một tỉ dòng. Đọc và băm theo luồng thì bộ nhớ gần như không đổi.""",
           focus=[0, "1.2", "1.3", "1.4"], clear=True),
    ], checks=["alg.bnx_l27_chunks(24000) == 1 and alg.bnx_l27_chunks(24000000) == 367", "24000000 // 24000 == 1000", "alg.bnx_l27_chunks(24 * 10**9) == 366211"])

    pit = sc("pitfalls", "pitfall", "Lỗi hay gặp, theo từng giai đoạn của hệ thống", [
        st("""<div class="box warn"><b>Lỗi 1 (người mới).</b> Tin rằng gửi qua kênh <b class="red">mã hoá</b> thì tệp chắc chắn <b>đủ và đúng</b>. Kênh mã hoá bảo vệ đường truyền, không kiểm nội dung bên gửi đưa vào.
Thiếu 100 dòng hay sai một chữ số vẫn đi qua trót lọt: ca thử cho thấy chỉ số dòng và mã băm bắt được.
<br><span class="note">Giới hạn: mã băm nằm cùng tệp chỉ bắt hỏng hoặc thiếu ngẫu nhiên; kẻ cố ý sửa tệp rồi tính lại được mã băm, nên chống giả mạo cần chữ ký.</span></div>"""
           + PY_KIEM.out_html(),
           """Lỗi thứ nhất, của người mới, là tin rằng kênh mã hoá bảo đảm tệp đủ và đúng. Kênh mã hoá chỉ bảo vệ đường truyền, nên thiếu một trăm dòng hay sai một chữ số vẫn đi qua, chỉ số dòng và mã băm mới bắt được. Mã băm cùng tệp chỉ bắt lỗi ngẫu nhiên, chống kẻ cố ý sửa cần chữ ký.""", focus=[1, 2], clear=True),
        st("""<div class="box warn"><b>Lỗi 2 (người đã đi làm, lúc mới dựng).</b> Bộ phân tích XML <b class="red">để mặc định</b>. Yêu cầu chứa khai báo loại văn bản với thực thể ngoài có thể làm máy chủ đọc tệp cục bộ.
OWASP khuyên cấm khai báo loại văn bản; chạy thật, cấu hình đó đổi kết quả từ "xử lý" thành 400.</div>""",
           """Lỗi thứ hai, lộ ra lúc mới dựng: để bộ phân tích XML ở cấu hình mặc định. Khi đó thực thể ngoài có thể khiến máy chủ đọc tệp cục bộ. Chạy thật, cấm khai báo loại văn bản thì kết quả đổi thành mã bốn trăm.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 3 (người đã đi làm, lúc tải tăng).</b> Băm tệp bằng cách <b class="red">đọc cả tệp vào bộ nhớ</b>. Chạy tốt ở 10³ dòng; ở 10⁹ dòng (24 GB) bộ nhớ cạn nếu máy chỉ còn dưới 24 GB trống (số minh hoạ).
Đọc theo khối 64 KiB thì ở 10⁶ dòng là 367 khối, bộ nhớ không đổi.</div>""",
           """Lỗi thứ ba, lộ ra khi tải tăng: băm tệp bằng cách đọc cả tệp vào bộ nhớ. Chạy tốt ở một nghìn dòng, nhưng ở một tỉ dòng, tức hai mươi bốn tỉ byte, bộ nhớ cạn nếu máy còn trống ít hơn thế; đọc theo khối thì bộ nhớ không đổi.""", clear=True),
        st("""<div class="box warn"><b>Lỗi 4 (người đã đi làm, lúc vận hành lâu dài).</b> Bên nhận <b class="red">quét thư mục theo giờ và lấy mọi tệp</b>, kể cả tệp đang ghi dở; hoặc xử lý cùng một tệp hai lần sau khi sự cố. Cách chữa: chỉ lấy tên không đuôi <code>.part</code>, kiểm dòng cuối, và ghi lại mã băm đã xử lý để lần sau bỏ qua.</div>""",
           """Lỗi thứ tư, lộ ra khi vận hành lâu: bên nhận quét thư mục theo giờ, lấy cả tệp ghi dở hoặc xử lý một tệp hai lần sau sự cố. Cách chữa là chỉ lấy tên không mang đuôi tạm, kiểm dòng cuối, ghi lại mã băm đã xử lý.""", clear=True),
    ], checks=["alg.bnx_l27_batch_check(1000, 900, True) == 'THIEU DONG'", "alg.bnx_l27_chunks(24 * 10**9) > 300000"])

    quiz = sc("quiz", "quiz", "Đến lượt bạn", [
        st(table(["câu", "đề"],
                 [["1", "Tệp lô có dòng cuối <code>TRAILER|500|…</code> nhưng chỉ có 498 dòng dữ liệu, và mã băm cũng không khớp. Kết luận nào được báo trước theo thứ tự kiểm, và vì sao?"],
                  ["2", "Mỗi dòng dài 40 byte, tệp 2 triệu dòng, khối đọc 64 KiB (65 536 byte). Bao nhiêu byte, bao nhiêu khối (làm tròn lên)?"],
                  ["3", "Quyết định (số minh hoạ): đối tác gửi tệp lô 3 giờ sáng qua kênh mã hoá, bạn quét thư mục mỗi 5 phút. Chọn: đòi họ đổi tên nguyên tử, tự đợi tệp không đổi kích thước 1 phút, hay để quét mỗi 5 phút rồi kiểm dòng cuối? Vì sao?"]]),
           """Đến lượt bạn, ba câu để làm ra giấy. Báo lỗi nào trước khi vừa thiếu dòng vừa lệch mã băm, tính số byte và khối của tệp hai triệu dòng, và chọn cách nhận tệp lô. Hãy dừng lại làm rồi xem đáp án.""",
           focus=[0, "1.2", "1.3", "1.4", 0], pause=30),
        st("""<p>Câu 1: kiểm số dòng trước (rẻ), nên báo <b>THIEU DONG</b>; không cần băm vì đã thấy lỗi.</p>
$$498 \\neq 500 \\Rightarrow \\hlg{\\text{THIEU DONG}}$$""",
           """Đáp án câu một. Ta kiểm số dòng trước vì rẻ, nên báo thiếu dòng, và không cần băm nữa vì đã thấy lỗi.
           Bốn trăm chín mươi tám khác năm trăm."""),
        st("""<p>Câu 2: byte = số dòng × 40; khối = byte : 65 536 làm tròn lên.</p>
$$2\\,000\\,000 \\times 40 = \\hlg{80\\,000\\,000} \\text{ byte}; \\qquad 80\\,000\\,000 : 65\\,536 \\approx 1220{,}7 \\Rightarrow \\hlg{1221} \\text{ khối}$$""",
           """Đáp án câu hai, hai triệu dòng nhân bốn mươi là tám mươi triệu byte, chia cho sáu mươi lăm nghìn năm trăm ba mươi sáu được khoảng một nghìn hai trăm hai mươi phẩy bảy. Làm tròn lên là một nghìn hai trăm hai mươi mốt khối, vì khối cuối chưa đầy vẫn phải đọc.""", focus=[[1], 2]),
        st(table(["lựa chọn", "được", "mất"],
                 [["đòi đối tác đổi tên nguyên tử", "chắc chắn không lấy tệp dở; không phải đoán", "phụ thuộc đối tác chịu đổi quy trình"],
                  ["tự đợi tệp không đổi kích thước 1 phút", "không cần đối tác đổi gì", "đoán: mạng đứng 2 phút vẫn lọt tệp dở; chậm thêm 1 phút"],
                  ["quét 5 phút một lần rồi kiểm dòng cuối", "bắt được tệp dở và tệp hỏng", "tệp dở vẫn bị đọc rồi mới bị từ chối; phải có quy trình đòi gửi lại"]]),
           """Đáp án câu ba: đòi đối tác đổi tên nguyên tử là chắc chắn nhất vì không phải đoán, đổi lại phụ thuộc đối tác. Hai cách còn lại hoặc phải đoán, hoặc để tệp dở bị đọc trước. Nên đòi đổi tên nguyên tử, và luôn kiểm dòng cuối làm lớp thứ hai."""),
    ], checks=["alg.bnx_l27_batch_check(500, 498, False) == 'THIEU DONG'", "2000000 * 40 == 80000000 and alg.bnx_l27_chunks(80000000) == 1221"])

    lab_pr = practice_scene(sc, "Tự làm: đối soát tệp lô", practice_steps(
        st, "BNX", "L27",
        """<p><b>Đề</b>: tệp lô có dòng cuối <code>TRAILER|n|sha256</code>. Viết <code>mau.py</code> có hàm <code>kiem(noi_dung)</code> trả <code>THIEU DONG</code> (số dòng lệch), <code>SAI MA BAM</code> (đủ dòng nhưng mã băm lệch) hoặc <code>OK</code> (kiểm số dòng trước).</p>
<p>Dựng lô 5 dòng <code>A01|100</code> … <code>A05|500</code> rồi in 4 dòng: <code>lo tot</code>, <code>lo thieu mot dong</code>, <code>lo sai mot chu so</code> (đổi A03|300 thành A03|301), <code>lo co trailer gia</code> (mã băm toàn số 0).</p>
<p class="note">Số liệu khác ví dụ trong bài; chi tiết trong <code>de.md</code>.</p>""",
        """Đến phần bạn tự làm: viết hàm Python kiểm tệp lô theo dòng cuối, kiểm số dòng trước rồi tới mã băm. Tự dựng một lô năm dòng, chạy hàm cho bốn trường hợp: lô đúng, thiếu một dòng, sai một chữ số, và có dòng cuối giả. Hãy dừng video và tự viết.""",
        LAB_OUT, "mau.py",
        """<div class="box key"><b>Nếu kẹt:</b> tách dòng cuối bằng <code>split("|")</code>; đếm các dòng còn lại; ghép phần dữ liệu lại với dấu xuống dòng cuối mỗi dòng rồi băm bằng <code>hashlib.sha256(…).hexdigest()</code>.
Lời giải đầy đủ ở <code>labs/BNX/L27/loi_giai.py</code> — chỉ mở sau khi bạn đã thử.</div>""",
        """Nếu kẹt, tách dòng cuối theo dấu gạch đứng, đếm các dòng còn lại, ghép phần dữ liệu lại rồi băm bằng thư viện băm của Python. Lời giải nằm trong thư mục thực hành, chỉ mở sau khi đã tự thử.""", pause=150), "BNX", "L27")

    rec = sc("recap", "recap", "Chuỗi logic & tư duy cần mang theo", [
        st(chain("phong bì + mô tả dịch vụ", "lỗi có cấu trúc", "cấm khai báo loại văn bản", "đổi tên nguyên tử", "số dòng + mã băm"),
           """Phong bì XML cùng tệp mô tả cho hợp đồng chặt và lỗi có cấu trúc, còn bộ phân tích phải cấm khai báo loại văn bản. Với tệp lô, đổi tên nguyên tử tránh đọc tệp dở, số dòng và mã băm bắt tệp thiếu hay sai."""),
        st("""<div class='box key'><b>Tư duy:</b> kênh mã hoá bảo vệ đường truyền, <b>không</b> bảo đảm nội dung. Tệp nhận về phải <b>tự chứng minh</b> được là đủ (mã băm cùng tệp chỉ bắt lỗi ngẫu nhiên; chống giả mạo cần chữ ký), và chỉ được đọc khi đã xong.
Hệ cũ vẫn sống vì hợp đồng chặt; trả giá bằng độ nặng và bằng việc phải cấu hình bộ phân tích cho an toàn.</div>""",
           """Kênh mã hoá bảo vệ đường truyền chứ không bảo đảm nội dung, nên tệp nhận về phải tự chứng minh là đủ."""),
        st(table(["Nếu bị hỏi về dòng này trên CV", "ý trả lời"],
                 [["SOAP/WSDL: vì sao còn dùng, so với REST?", "hợp đồng chặt (WSDL), lỗi có cấu trúc (Fault), hệ cũ sẵn có; đổi lại nặng hơn JSON (đo: ≈10 lần ở ví dụ nhỏ, cùng cách viết liền) và phải cấu hình bộ phân tích chống XXE"],
                  ["Truyền tệp lô qua SFTP: bạn bảo đảm thế nào?", "kênh mã hoá chỉ bảo vệ đường truyền; đổi tên nguyên tử để không đọc tệp dở; dòng cuối có số dòng + sha256; đọc/băm theo luồng; ghi nhận tệp đã xử lý để không xử lý hai lần"],
                  ["Bạn xử lý thế nào khi tệp lô thiếu hoặc sai?", "từ chối, ghi nhật ký mã băm, báo bên gửi gửi lại; không sửa tay dữ liệu; đối soát số dòng/tổng tiền với bên gửi"]]),
           """Người phỏng vấn thường hỏi ba câu về dòng này: vì sao còn dùng giao thức phong bì, tệp lô bảo đảm thế nào, và khi tệp thiếu hoặc sai thì làm gì. Câu trả lời ngắn nằm sẵn trên bảng.""", clear=True),
        st("""<p>Bài sau: <b>MongoDB, MySQL, PostgreSQL</b> so với Oracle và SQL Server: mô hình dữ liệu, khoá, và khi nào chọn gì.</p>""",
           """Ở bài hai mươi tám, ta so sánh cơ sở dữ liệu quan hệ và loại lưu văn bản JSON với hai hệ đã học, về mô hình dữ liệu và khi nào chọn cái nào.""",
           forward_ref=True),
    ], checks=["alg.bnx_l27_batch_check(1000, 1000, True) == 'OK'"])
    scenes = _spoken([hook, pre, sym, intu, form, ex, chk, quymo, pit, quiz, lab_pr, rec])
    return lesson("L27", "soap_wsdl_sftp",
                  "Bài 27 — SOAP/WSDL và SFTP: tích hợp hệ cũ và đối soát tệp lô",
                  "curriculum/bnx.yaml L27; audit/bnx/verify_bnx.py L27; audit/bnx/sources_l27.md: OWASP XML External Entity Prevention Cheat Sheet, "
                  "man sftp(1) của OpenBSD (đọc 2026-11-13); SOAP/WSDL của W3C KHÔNG đọc được nguyên văn (máy chủ w3.org chặn): bài chỉ nói điều đo ở máy chủ thử JDK 21; SFTP là mô phỏng",
                  ["Đọc một phong bì XML và chỉ ra phần thân và phần lỗi",
                   "Đọc kết quả chạy thật của một dịch vụ phong bì tối giản bằng JDK: mã trạng thái 200, 500 và 400",
                   "So sánh kích thước đã đo của phong bì với JSON tương đương",
                   "Đọc một tệp mô tả dịch vụ và đếm thông điệp, thao tác, ràng buộc và dịch vụ",
                   "Kiểm toàn vẹn tệp lô bằng số dòng và mã băm ở dòng cuối",
                   "Tính số byte và số khối phải đọc khi tệp lô lớn gấp 1 000 lần",
                   "Chặn yêu cầu có khai báo loại văn bản bằng cấu hình bộ phân tích XML"],
                  scenes, assumes=["bnx_nguyen_tu", "bnx_ma_bam"],
                  covers=[(1, "formula"), (2, "example"), (3, "example"), (4, "example"), (5, "check"), (6, "quymo"), (7, "formula")])
