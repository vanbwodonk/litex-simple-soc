from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex.gen import *
from litei2c import LiteI2C
from litex.soc.cores.clock import *
from litex.soc.cores.gpio import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.led import LedChaser

from litex.build.parser import LiteXArgumentParser

import spartan6_board

kB = 1024
mB = 1024*kB


# CRG ----------------------------------------------------------------------------------------------
class CRG(Module):
    def __init__(self, platform, sys_clk_freq):
        self.clock_domains.cd_sys = ClockDomain()

        clk = platform.request("clk100")
        rst_n = platform.request("user_btn", 0) # Menjadikan button0 sebagai reset

        self.comb += self.cd_sys.clk.eq(clk)
        self.specials += AsyncResetSynchronizer(self.cd_sys, ~rst_n)

# Create a led blinker module
class Blink(Module):
    def __init__(self, led):
        self.counter = Signal(25)
        
        # combinatorial assignment
        self.comb += [
            led.eq(self.counter[24])
        ]
        
        # synchronous assignment
        self.sync += self.counter.eq(self.counter + 1)


# BaseSoC ------------------------------------------------------------------------------------------
class BaseSoC(SoCCore):
    def __init__(self, sys_clk_freq=int(50e6), toolchain="ise", **kwargs):

        platform = spartan6_board.Platform(toolchain=toolchain)

        SoCCore.__init__(self, platform, sys_clk_freq,      
            ident                   = "LiteX SoC on Spartan6.",
            **kwargs
        )

        self.submodules.crg = CRG(platform, sys_clk_freq)

        # ledsanim = LedsAnim(pads=platform.request_all("user_led"), sys_clk_freq=sys_clk_freq, period=0.03)
        # self.submodules.ledsanim = ledsanim
        # self.add_csr("ledsanim")
        
        # uartbone
        #self.add_uartbone(uart_name="serial", baudrate=115200) 

        #i2c
        pad_i2c = platform.request("i2c", 0)
        self.submodules.i2c = LiteI2C(pads=pad_i2c, sys_clk_freq=sys_clk_freq)

        #blink led
        led1 = platform.request("user_led", 0)
        self.submodules.blink = Blink(led1)
                 

# Build --------------------------------------------------------------------------------------------
def main():    
    parser = LiteXArgumentParser(platform=spartan6_board.Platform, description="LiteX SoC on Spartan6.")
    parser.add_target_argument("--flash",           action="store_true",    help="Flash bitstream")
    parser.add_target_argument("--sys-clk-freq",    default=50e6,          help="System clock frequency.")
    args = parser.parse_args()

    soc = BaseSoC(
        toolchain           = args.toolchain,
        sys_clk_freq        = args.sys_clk_freq,
        **parser.soc_argdict
    )
    # builder = Builder(soc, **parser.builder_argdict)
    builder = Builder(soc, compile_gateware=True, compile_software=False)

    if args.build:
        builder.build(**parser.toolchain_argdict)
    
    if args.load:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram", ext=".bit"))

    if args.flash:
        prog = soc.platform.create_programmer()
        prog.flash(0, builder.get_bitstream_filename(mode="flash", ext=".bit"), fpga_part="xc6slx25ftg256")

if __name__ == "__main__":
    main()
