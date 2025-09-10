all: build/blink.svf build/blink.bit

YOSYS_BIN = /opt/oss-cad-suite/bin
SYNTH_SRCS=blink_migen.v
SIM_SRCS=blink_tb.v blink.v 
PACKAGE=CABGA256
LFP=ecp5.lpf

build/blink.json: $(SYNTH_SRCS)
	mkdir -p build
	$(YOSYS_BIN)/yosys -p 'read_verilog $(SYNTH_SRCS); synth_ecp5 -top top -abc9 -json $@'

build/blink.config: build/blink.json $(LPF)
	$(YOSYS_BIN)/nextpnr-ecp5 --25k --package $(PACKAGE) --speed 6 --lpf $(LFP) --json build/blink.json --textcfg build/blink.config --freq 25

build/blink.svf: build/blink.config
	$(YOSYS_BIN)/ecppack --compress --input $< --svf $@

build/blink.bit: build/blink.config
	$(YOSYS_BIN)/ecppack --compress --input $< --bit $@

build/blink_tb: $(SIM_SRCS)
	$(YOSYS_BIN)/iverilog -I `yosys-config --datdir/ecp5/` `yosys-config --datdir/ecp5/cells_sim.v` $(SIM_SRCS) -o $@

build/blink_tb.vcd: build/blink_tb
	build/blink_tb

prog: build/blink.bit
	$(YOSYS_BIN)/ecpprog -S  $<

flash: build/blink.bit
	# ERASES THE DEFAULT CONTENTS OF THE SPI FLASH!
	$(YOSYS_BIN)/openFPGALoader --cable dirtyJtag -f build/blink.bit

flash_backup:
	$(YOSYS_BIN)/ecpprog -R 2M colorlight_backup.bit

clean:
	rm -f build/*


