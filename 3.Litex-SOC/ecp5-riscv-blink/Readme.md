## 📖 Deskripsi
Membuat Litex SOC (Vexriscv) pada Spartan 6.
1. Default Bios.
2. Litex Baremetal Demo.
3. Upload Menggunakan litex_term.
---

## ⚙️ Penggunaan
- Untuk build dan generate document
    ```bash
    python ECP5_soc.py --build --doc
    ```
- Untuk load program (.bit) dan generate document
    ```bash
    python ECP5_soc.py --build --load --doc
    ```
- Untuk flash program (.bit) dan generate document
    ```bash
    python ECP5_soc.py --build --flash --doc
    ```

# 1. Default Bios
- Setelah di-flash/load buka litex_term
    ```bash
    litex_term /dev/ttyUSB0
    ```
- Reset board atau ketikkan reboot, akan muncul seperti berikut:

    ![BIOS_DEFAULT](bios_default.png)

    Note: ketik 'help' untuk melihat menu lainnya.

# 2. Litex Baremetal Demo
- Lakukan command berikut:
    ```bash
    litex_bare_metal_demo --build-path build/ecp5card
    ```
    Akan menghasilkan file demo.bin dan folder demo.
    
    "--build-path" mandatory command.

- Flash/load file demo.bin pada rom (biasanya digunakan untuk production level):
    ```bash
    python ECP5_soc.py --integrated-rom-init demo.bin --build --flash
    ```
- Buka kembali litex_term.

    ![BIOS_BARE](bios_baremetal.png)    


# 3. Upload Menggunakan litex_term
- Tutup litex_term

- Lakukan command berikut:
    ```bash
    litex_term /dev/ttyUSB0 --kernel demo.bin --safe
    ```
- Reset board menggunakan tomobl atau ketik "reboot" setelah command diatas

    ![UPLOAD](upload.png) 


    Note:
    - /dev/ttyXXXX bisa bermacam-macam, contoh ttyUSB0, ttyUSB1, ttyACM0, dll. 
    - opsi --safe diperlukan karena terdapat CRC error pada litex_term versi 2025.4.
    - Default address upload litex_term adalah 0x40000000 (bisa dirubah dengan menambahkan --kernel-adr=0xXXXXXXXX).
    - Pastikan memory untuk upload program ada dan bisa diwrite menggunakan wishbone (litex_cli/wishbone-tools) atau command bios (mem_write).
    Contoh memory yang tidak bisa diwrite:
        1. ROM
        2. flash/spiflash
        3. tambahan rom pada soc (self.add_rom)
---