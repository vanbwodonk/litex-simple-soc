## Folder Structure

```bash
spartan6-riscv-soc
├── build                 # build folder from litex
├── firmware              # firmware 
├── readme.md             # this readme
├── soc.py                # python file to create SOC
├── spartan6_board.py     # python for board pinout and family
└── spartan6_board.ucf    # ucf from dit, for 
```

## How To Build

```bash
python soc.py --cpu-type serv --build # you can change cpu-type (picorv, vexriscv, etc).
```
 if build complete without error. Go to firmware folder. 
 Build firware with `make`. We need firmware.bin to build into bitstream.

 build SOC again with integrated rom:
 ```bash
python soc.py --cpu-type serv --build
```
