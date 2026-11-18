import jakarta.persistence.*;
import java.util.*;
@Entity
public class Khach {
  @Id Long id;
  String ten;
  @OneToMany(mappedBy = "khach")
  List<TaiKhoan> tk = new ArrayList<>();
}
