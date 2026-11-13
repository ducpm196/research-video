class HetHanMuc extends Exception {
    HetHanMuc(String thongBao) {
        super(thongBao);
    }
}

class The {
    private long daRut = 0;
    private long hanMuc = 2000000;                   // hạn mức mỗi ngày (số minh hoạ)

    void rut(long tien) throws HetHanMuc {
        if (daRut + tien > hanMuc) {
            throw new HetHanMuc("Vuot han muc, da rut " + daRut + ", xin rut " + tien);
        }
        daRut += tien;
    }

    long laySoDaRut() {
        return daRut;
    }
}

public class RutHanMuc {
    public static void main(String[] args) {
        The the = new The();
        try {
            the.rut(800000);
            System.out.println("Rut 800000 xong");
            the.rut(900000);
            System.out.println("Rut 900000 xong");
            the.rut(500000);
            System.out.println("Rut 500000 xong");
        } catch (HetHanMuc e) {
            System.out.println("Tu choi: " + e.getMessage());
        } finally {
            System.out.println("Da rut hom nay: " + the.laySoDaRut());
        }
    }
}
