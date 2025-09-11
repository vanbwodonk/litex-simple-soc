# Migen & Litex Instalation

1. Install Python 3.6+ and FPGA vendor's development tools (oss-cad-suite, vivado, etc) 
    ```bash
    sudo pacman -S oss-cad-suite-bin
    ```
2. Install Migen/LiteX with Python Virtual Environtment:
    
    Setting Virtual Environtment :
     ```bash
    cd && mkdir Litex
    cd litex && mkdir Litex/LITEX_VENV
    python -m venv Litex/LITEX_VENV
    source ~/Litex/LITEX_VENV/bin/activate
    ```
    Install litex in Virtual Environtment :
    ```bash
    wget https://raw.githubusercontent.com/enjoy-digital/litex/master/litex_setup.py
    chmod +x litex_setup.py
    ./litex_setup.py --init --install
    ```

3. Clone this Project:
    ```bash
    git clone https://github.com/vanbwodonk/litex-simple-soc.git
    ```
