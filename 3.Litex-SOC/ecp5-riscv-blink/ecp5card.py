#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2020 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.lattice import LatticeECP5Platform
from litex.build.openfpgaloader import OpenFPGALoader

# IOs ---------------------------------------------------------------------------------------------
_io = [
    # Clk
    ("clk16", 0, Pins("A7"), IOStandard("LVCMOS33")),

    # Led
    ("user_led", 0, Pins("N4"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("N3"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("M4"), IOStandard("LVCMOS33")),

    # Button
    ("user_btn", 0, Pins("L3"), IOStandard("LVCMOS33")),
    ("user_btn", 1, Pins("N6"), IOStandard("LVCMOS33")),

    # Serial
    ("serial", 0,
        Subsignal("tx", Pins("H2")),
        Subsignal("rx", Pins("G1")),
        IOStandard("LVCMOS33")
    ),

    # Serial
    ("serial_debug", 0,
        Subsignal("tx", Pins("G2")),
        Subsignal("rx", Pins("F1")),
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
    ("spiflash4x", 0,  # clock needs to be accessed through STARTUPE2
        Subsignal("cs_n", Pins("N8")),
        Subsignal("dq",   Pins("T8 T7 M7 N7")),
        IOStandard("LVCMOS33")
    ),

    # SDRAM (IS42S16160B (32MB))
    ("sdram_clock", 0, Pins("R15"), IOStandard("LVCMOS33")),
    ("sdram", 0,
        Subsignal("a", Pins(
            "H15 B13 B12 J16 J15 R12 K16 R13",
            "T13 K15 A13 R14 T14")),
        Subsignal("dq", Pins(
            "F16 E15 F15 D14 E16 C15 D16 B15",
            "R16 P16 P15 N16 N14 M16 M15 L15")),
        Subsignal("we_n",  Pins("A15")),
        Subsignal("ras_n", Pins("B16")),
        Subsignal("cas_n", Pins("G16")),
        Subsignal("cs_n", Pins("A14")),
        Subsignal("cke",  Pins("L16")),
        Subsignal("ba",    Pins("G15 B14")),
        Subsignal("dm",   Pins("C16 T15")),
        IOStandard("LVCMOS33"),
        Misc("SLEWRATE=FAST")
    ),


    # PWM
    ("pwm", 0, Pins("A12"), IOStandard("LVCMOS33")),
    ("pwm", 1, Pins("A11"), IOStandard("LVCMOS33")),

]

# Connectors -------------------------------------------------------------------------------
_connectors = [
    ("J1",  #3V3 3V3",
            #GND GND",
            "A12 A11",
            "N16 P15",
            "M16 M15",
            "L16 L15",
            "K16 K15",
            "J16 J15",
            "H15 G16",
            "G15 F16",
            "E16 F15",
            "E15 D16",
            "C16 C15",
            "B16 B15",
            "A15 B14",
            "A14 A13"),
    ("J2",  #3V3 3V3",
            #GND GND",
            "T3 R3",
            "T2 R2",
            "R1 P1",
            "P2 N1",
            "M2 M1",
            "L2 L1",
            "K2 K1",
            "J2 J1",
            "G1 H2",
            "G2 F1",
            "F2 E1",
            "E2 D1",
            "C2 C1",
            "B2 B1"),
]

# Platform -----------------------------------------------------------------------------------------

class Platform(LatticeECP5Platform):
    default_clk_name   = "clk16"
    default_clk_freq = 16e6
    default_clk_period = 1e9/default_clk_freq
    def __init__(self, toolchain="trellis", **kwargs):
        self.clk_name   = "clk16"
        self.clk_freq   = 16e6
        self.clk_period = 1e9/self.clk_freq
        LatticeECP5Platform.__init__(self, "LFE5U-25F-6BG256C", _io, _connectors, toolchain=toolchain)

    def create_programmer(self, kit="openfpgaloader"):
        return OpenFPGALoader(cable="dirtyJtag")

    def do_finalize(self, fragment):
        LatticeECP5Platform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request(self.clk_name, loose=True), self.clk_period)
