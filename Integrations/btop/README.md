<div align="center">
<img width="349" height="98" alt="image" src="https://github.com/user-attachments/assets/678652c5-d011-4e3b-9bb7-037ffa8b979a" />
</div>
<h4 align="center">nhưng là cho dòng 4 chữ~</h4>
<img width="27" height="27" alt="image" align="right" src="https://github.com/user-attachments/assets/de8413fe-b942-487b-a6d8-3f5111d292c9" />

> [!NOTE]
> Chúng mình không phải dev trong project btop  
> Nên tất cả các assets (ảnh, file, ...) liên quan đều được đánh bản quyền bởi các dev của btop

## 1: <ins>Yêu cầu</ins>


* Mở được Telnet/SSH trên router đã đề cập ở [ngoài kia](https://github.com/Expl01tHunt3r/vnptmodemresearch?tab=readme-ov-file#3-shell-v%C3%A0-nh%E1%BB%AFng-ng%C6%B0%E1%BB%9Di-b%E1%BA%A1n-tty-ssh-)

> [!CAUTION]
> **Bạn sẽ tự chịu hết các hậu quả đi kèm nếu làm theo!!!**  
> **Và chúng mình KHÔNG CHỊU TRÁCH NHIỆM nếu bị lỗi trên router nhà bạn**  
> *đã nhắc rồi nhé.*

> [!WARNING]
> Hiện tại chỉ có dòng [GW040-NS](https://www.vnpt-technology.vn/vi/product_detail/gpon-ont-igate-gw040-ns) đã confirm chạy okay  
> Còn dòng -H có lỗi reboot sau khi chạy script, chúng mình vẫn đang nấu vụ đó, mà ai có dòng -H có thể liên hệ [Discord](https://discordapp.com/users/1086149348414464041) để góp vui :)

## 2: <ins>Cài Đặt</ins>
* SSH/Telnet vào router
<img width="469" height="146" alt="image" src="https://github.com/user-attachments/assets/cde8d9f6-be70-44d9-86bd-41d13cd54da5" />

* Paste lệnh dưới vào shell
```sh
cd /tmp/userdata/ && /userfs/bin/curl -s -k -o AdGuard.sh https://raw.githubusercontent.com/Expl01tHunt3r/vnptmodemresearch/refs/heads/main/AdGuard/install-ns.sh && chmod +x AdGuard.sh && sh AdGuard.sh
```

* Hãy **CHẮC CHẮN** đọc hết phần text trước khi bấm **Enter** *(nếu hiểu thì thôi .-.)*
<img width="982" height="512" alt="image" src="https://github.com/user-attachments/assets/ca525647-5626-486e-a237-7425d160a51f" />


## 6: <ins>FAQs</ins>
* **?: Tại sao phải chạy lại script sau mất điện?**
  * Tất cả các file (trừ config) đều lưu tại `/tmp/SafeGate`, mà nó lại là `tmpfs` nên sau khi reboot (mất điện) thì nó trắng bóc, không còn cái gì cả nên chạy lại để nó tự cài lại cho  
<h4 align="center">The End</h4>
<h6 align="right">AppleSang With 🍎</h6>









