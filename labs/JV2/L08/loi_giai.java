import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

public class LaiTheoNgay {
    public static void main(String[] args) {
        LocalDate gui = LocalDate.of(2026, 1, 15);
        LocalDate den = LocalDate.of(2026, 4, 20);
        long soNgay = ChronoUnit.DAYS.between(gui, den);
        BigDecimal goc = new BigDecimal("120000000");
        BigDecimal lai = goc.multiply(new BigDecimal("0.06")).multiply(BigDecimal.valueOf(soNgay))
                .divide(BigDecimal.valueOf(365), 0, RoundingMode.HALF_UP);
        System.out.println("So ngay: " + soNgay);
        System.out.println("Lai: " + lai);
        System.out.println("Tong: " + goc.add(lai));
        System.out.println("Dao han la: " + den.getDayOfWeek());
    }
}
