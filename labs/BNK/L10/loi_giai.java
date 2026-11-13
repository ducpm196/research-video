import java.util.*;
public class GhepPhanHoi {
    public static void main(String[] args) {
        Map<String, String> cho = new HashMap<>();
        for (int i = 0; i < 6; i++) cho.put("M" + i, "chuyen " + (i + 1) * 100);
        String[] ve = { "M3", "M5", "M0", "M1", "M4", "M2" };    // mã tương quan, theo thứ tự phản hồi về
        int dung = 0;
        for (int k = 0; k < ve.length; k++) {
            System.out.println("phan hoi " + k + ": " + ve[k] + " -> " + cho.get(ve[k]));
            if (ve[k].equals("M" + k)) dung++;
        }
        System.out.println("dung neu ghep theo thu tu: " + dung + "/6");
    }
}
