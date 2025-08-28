from litex.build.xilinx import *
from litex.build.generic_platform import *
from litex.build.xilinx import XilinxSpartan6Platform
from litex.build.openfpgaloader import OpenFPGALoader

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk100", 0, Pins("M9"), IOStandard("LVCMOS33")),

    # Leds
    # ("user_led", 0, Pins("P119"), IOStandard("LVCMOS33"), Drive("8"), Misc("SLEW = FAST"), Misc("PULLUP")),
    # ("user_led", 1, Pins("P118"), IOStandard("LVCMOS33"), Drive("8"), Misc("SLEW = FAST"), Misc("PULLUP")),   
    
    # Button
    ("user_btn", 0, Pins("B14"), IOStandard("LVCMOS33"), Drive("8"), Misc("SLEW = FAST"), Misc("PULLUP")),  
    # ("user_btn", 1, Pins("P123"), IOStandard("LVCMOS33"), Drive("8"), Misc("SLEW = FAST"), Misc("PULLUP")),  

    # Serial
    ("serial", 0,
        Subsignal("tx", Pins("D16")),
        Subsignal("rx", Pins("E15")),
        IOStandard("LVCMOS33")
    ),

    # SPIFlash (W25Q128JV)
    # ("spiflash", 0,
    #     Subsignal("cs_n", Pins("N8"), IOStandard("LVCMOS33")),
    #     #Subsignal("clk",  Pins("N9"), IOStandard("LVCMOS33")),
    #     Subsignal("miso", Pins("T8"), IOStandard("LVCMOS33")),
    #     Subsignal("mosi", Pins("T7"), IOStandard("LVCMOS33")),
    # ),

    # SPIFlash4x (W25Q128JV)
    # ("spiflash4x", 0,  # clock needs to be accessed through STARTUPE2
    #     Subsignal("cs_n", Pins("N8")),
    #     Subsignal("dq",   Pins("T8 T7 M7 N7")),
    #     IOStandard("LVCMOS33")
    # ),

    #I2C
    ("i2c", 0,
        Subsignal("scl", Pins("A11"), IOStandard("LVCMOS33")),
        Subsignal("sda", Pins("B12"), IOStandard("LVCMOS33"))
    ),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(XilinxSpartan6Platform):
    default_clk_name   = "clk100"
    default_clk_period = 1e9/100e6

    def __init__(self, toolchain="ise", **kwargs):
        XilinxSpartan6Platform.__init__(self, "xc6slx25-2-ftg256", _io, toolchain=toolchain)
        self.toolchain.additional_commands = ["write_bitstream -force -bin_file {build_name}"]

    def create_programmer(self, kit="openfpgaloader"):
        return OpenFPGALoader(cable="dirtyJtag")

    def do_finalize(self, fragment):
        XilinxSpartan6Platform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk100", loose=True), 1e9/100e6)
