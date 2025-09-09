from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex.gen import *

import ecp5card

from litex.soc.cores.clock import *
from litex.soc.integration.soc_core import *
from litex.soc.cores.led import LedChaser
from litex.soc.integration.builder import *

from litex.build.io import DDROutput
from litedram.modules import IS42S16160 # Compatible with EM638325-6H.
from litedram.phy import GENSDRPHY, HalfRateGENSDRPHY
from litespi.modules import W25Q128JV
from litespi.opcodes import SpiNorFlashOpCodes as Codes

from litex.soc.integration.soc import SoCRegion

from litex.build.parser import LiteXArgumentParser

kB = 1024
mB = 1024*kB

# CRG ----------------------------------------------------------------------------------------------
class _CRG(LiteXModule):
    def __init__(self, platform, sys_clk_freq, with_rst=True, sdram_rate="1:1"):
        self.rst    = Signal()
        self.cd_sys = ClockDomain()
        if sdram_rate == "1:2":
            self.cd_sys2x    = ClockDomain()
            self.cd_sys2x_ps = ClockDomain()
        else:
            self.cd_sys_ps = ClockDomain()

        # # #
        # Clk / Rst
        clk = platform.request("clk16")
        rst_n = platform.request("user_btn", 0)
        clk_freq = 16e6

        # PLL
        self.pll = pll = ECP5PLL()
        self.comb += pll.reset.eq(~rst_n | self.rst)
        pll.register_clkin(clk, clk_freq)
        pll.create_clkout(self.cd_sys,    sys_clk_freq)
        if sdram_rate == "1:2":
            pll.create_clkout(self.cd_sys2x,    2*sys_clk_freq)
            pll.create_clkout(self.cd_sys2x_ps, 2*sys_clk_freq, phase=180) # Idealy 90° but needs to be increased.
        else:
           pll.create_clkout(self.cd_sys_ps, sys_clk_freq, phase=180) # Idealy 90° but needs to be increased.

        # SDRAM clock
        sdram_clk = ClockSignal("sys2x_ps" if sdram_rate == "1:2" else "sys_ps")
        self.specials += DDROutput(1, 0, platform.request("sdram_clock"), sdram_clk)      

# BaseSoC ------------------------------------------------------------------------------------------
class BaseSoC(SoCCore):
    def __init__(self, sys_clk_freq=64e6, toolchain="trellis", sdram_rate="1:1",
        **kwargs):
        platform = ecp5card.Platform(toolchain=toolchain)

        # CRG --------------------------------------------------------------------------------------
        self.crg = _CRG(platform, sys_clk_freq,  with_rst = True)

        # SoCCore ----------------------------------------------------------------------------------
        SoCCore.__init__(self, platform, int(sys_clk_freq), ident="LiteX SoC on Custom ECP5", **kwargs)            

        # SDR SDRAM --------------------------------------------------------------------------------
        # BASE_SDRAM_ORIGIN          = 0x40000000
        # sdrphy_cls = HalfRateGENSDRPHY if sdram_rate == "1:2" else GENSDRPHY
        # self.sdrphy = sdrphy_cls(platform.request("sdram"))
        # self.add_sdram("sdram",
        #     origin          = BASE_SDRAM_ORIGIN,
        #     phy             = self.sdrphy,
        #     module          = IS42S16160(sys_clk_freq, sdram_rate),
        #     l2_cache_size   = kwargs.get("l2_size", 8192)
        # )

        # MEM1 --------------------------------------------------------------------------------------
        BASE_MEM1_ORIGIN        = 0x40000000
        self.add_ram(name="ram", origin=BASE_MEM1_ORIGIN, size=10*kB)

        # SPI Flash4x ------------------------------------------------------------------------------
        BASE_SPIFLASH_ORIGIN       = 0x20000000
        self.mem_map["spiflash"] = BASE_SPIFLASH_ORIGIN
        self.add_spi_flash(mode="4x", module=W25Q128JV(Codes.READ_1_1_4),
                           rate="1:1", with_master=True
        )
        
        # self.bus.add_region("rom", SoCRegion(
        #     origin = self.bus.regions["spiflash"].origin + 0x800000,
        #     size   = 16 * kB,
        #     mode    ="rwx",
        #     linker = True)
        # )       
        
        # Leds -------------------------------------------------------------------------------------
        self.submodules.leds = LedChaser(
            pads=platform.request_all("user_led"),
            sys_clk_freq=sys_clk_freq,
            period=0.5
        )

        # uartbone
        # self.add_uartbone(uart_name="serial_debug", baudrate=115200)           

# Build --------------------------------------------------------------------------------------------
def main():    
    parser = LiteXArgumentParser(platform=ecp5card.Platform, description="LiteX SoC on Custom ECP5.")
    parser.add_target_argument("--flash",                action="store_true",      help="Flash Bitstream.")
    parser.add_target_argument("--sys-clk-freq",         default=100e6,             help="System clock frequency.")
    args = parser.parse_args()

    soc = BaseSoC(
        toolchain           = args.toolchain,
        sys_clk_freq        = args.sys_clk_freq,
        **parser.soc_argdict
    )
    builder = Builder(soc, **parser.builder_argdict)

    if args.build:
        builder.build(**parser.toolchain_argdict)

    if args.load:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram", ext=".svf"))
    
    if args.flash:
        prog = soc.platform.create_programmer()
        prog.flash(0, builder.get_bitstream_filename(mode="flash", ext=".bit"))

if __name__ == "__main__":
    main()