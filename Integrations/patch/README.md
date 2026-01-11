# Patch | AutoRun

## 1: <ins>Yêu cầu</ins>
<img width="128" height="128" alt="image" src="https://github.com/user-attachments/assets/b17f8ebf-e35e-4d68-9d60-a06b93767dc8" align="right" />


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
cd /tmp/SafeGate/ && /userfs/bin/curl -s -k -o patch_ar.sh https://raw.githubusercontent.com/Expl01tHunt3r/vnptmodemresearch/refs/heads/master/Integrations/patch/autorun.sh && chmod +x patch_ar.sh && sh patch_ar.sh
```

* Hãy **CHẮC CHẮN** đọc hết phần text trước khi bấm **Enter** *(nếu hiểu thì thôi .-.)*
<img width="979" height="454" alt="image" src="https://github.com/user-attachments/assets/2aa22f52-da1b-42e7-9c6e-1b0790e9eae1" />


* chờ....
* chờ....
* xong rồi đó, giờ router sẽ chạy những lệnh trong file /tmp/userdata/startup.sh khi kết nối mạng thành công
* nếu bạn muốn edit thì chỉ có thể xài echo hoặc sed
* còn cách sử dụng cứ chatgpt hoặc gemini đi
