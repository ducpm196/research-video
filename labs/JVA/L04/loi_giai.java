public class TietKiem {
    public static void main(String[] args) {
        long soDu = 50000000;                       // gửi 50 triệu đồng (số minh hoạ)
        int thangVuot = 0;                          // 0 nghĩa là chưa tháng nào vượt
        for (int thang = 1; thang <= 6; thang++) {
            long lai = soDu * 6 / 1000;             // 0,6% mỗi tháng
            soDu += lai;
            System.out.println("Thang " + thang + ": lai " + lai + ", so du " + soDu);
            if (thangVuot == 0 && soDu > 51000000) {
                thangVuot = thang;                  // chỉ ghi nhận lần đầu
            }
        }
        System.out.println("Thang dau tien vuot 51 trieu: " + thangVuot);
    }
}
