package shop;

import shop.kho.Hang;

public class Main {
    public static void main(String[] args) {
        Hang h = new Hang(12);
        h.ban(5);
        System.out.println("ban 5 cai, con " + h.con());
        if (!h.ban(9)) {
            System.out.println("ban 9 cai: tu choi, con " + h.con());
        }
    }
}
