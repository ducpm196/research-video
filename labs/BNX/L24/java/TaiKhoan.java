import jakarta.persistence.*;
@Entity
public class TaiKhoan {
  @Id Long id;
  @ManyToOne(fetch = FetchType.LAZY)
  Khach khach;
  long soDu;
}
