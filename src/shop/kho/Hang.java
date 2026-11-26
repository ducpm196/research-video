package shop.kho;

public class Hang {
    private int soLuong;

    public Hang(int soLuong) {
        this.soLuong = soLuong;
    }

    public boolean ban(int n) {
        if (n > soLuong) {
            return false;
        }
        soLuong -= n;
        return true;
    }

    public int con() {
        return soLuong;
    }
}
