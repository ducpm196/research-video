public class BacLai {
    public static void main(String[] args) {
        long soTien = args.length > 0 ? Long.parseLong(args[0]) : 10000000;   // số tiền gửi (số minh hoạ)
        long suat;                                  // lãi suất theo phần nghìn mỗi tháng (số minh hoạ)
        if (soTien < 10000000) {
            suat = 3;
        } else if (soTien < 100000000) {
            suat = 4;
        } else {
            suat = 5;
        }
        System.out.println(soTien + " -> suat " + suat + ", lai thang: " + soTien * suat / 1000);
    }
}
