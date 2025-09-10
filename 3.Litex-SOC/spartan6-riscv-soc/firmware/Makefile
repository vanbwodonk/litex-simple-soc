BUILD_DIR ?= ../build/spartan6_board
	
include $(BUILD_DIR)/software/include/generated/variables.mak
include $(SOC_DIRECTORY)/software/common.mak

S_SOURCES = $(wildcard *.S)
C_SOURCES = $(wildcard *.c)
OBJECTS   = $(patsubst %.S, %.o, $(S_SOURCES)) $(patsubst %.c, %.o, $(C_SOURCES))

all: $(notdir $(CURDIR)).bin
	$(PYTHON) -m litex.soc.software.memusage $(notdir $(CURDIR)).elf $(BUILD_DIR)/software/include/generated/regions.ld $(TRIPLE)

%.bin: %.elf
	$(OBJCOPY) -O binary $< $@
ifneq ($(OS),Windows_NT)
	chmod -x $@
endif	
ifeq ($(CPUENDIANNESS),little)
	$(PYTHON) -m litex.soc.software.crcfbigen $(notdir $(CURDIR)).bin -o $(notdir $(CURDIR)).fbi --fbi --little
else
	$(PYTHON) -m litex.soc.software.crcfbigen $@
endif

$(notdir $(CURDIR)).elf: $(OBJECTS)
	$(CC) $(LDFLAGS) -T linker.ld -N -o $@ \
		$(OBJECTS) \
		$(PACKAGES:%=-L$(BUILD_DIR)/software/%) \
		-Wl,--whole-archive \
		-Wl,--gc-sections \
		-Wl,-Map,$@.map \
		$(LIBS:lib%=-l%)

ifneq ($(OS),Windows_NT)
	chmod -x $@
endif

# pull in dependency info for *existing* .o files
-include $(OBJECTS:.o=.d)

%.o: %.c
	$(compile)

%.o: %.S
	$(assemble)

clean:
	$(RM) *.o *.d *.bin *.elf *.map *.fbi

path:
	@echo $(PICOLIBC_DIRECTORY)/newlib/libc/tinystdio
	@echo $(PICOLIBC_DIRECTORY)/newlib/libc/include
	@echo $(LIBBASE_DIRECTORY)
	@echo $(SOC_DIRECTORY)/software/include
	@echo $(SOC_DIRECTORY)/software
	@echo $(BUILDINC_DIRECTORY)
	@echo $(BUILDINC_DIRECTORY)/../libc
	@echo $(CPU_DIRECTORY)

.PHONY: all clean