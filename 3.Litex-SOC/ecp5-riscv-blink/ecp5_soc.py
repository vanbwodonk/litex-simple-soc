from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex.gen import *

import ecp5card

from litex.soc.cores.clock import *
from litex.soc.integration.soc_core import *
from litex.soc.cores.led import LedChaser
from litex.soc.integration.builder import *
from litex.soc.cores.gpio import GPIOOut

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

        # Clk / Rst
        clk = platform.request("clk16")
        rst_n = platform.request("user_btn", 0)
        clk_freq = 16e6

        # PLL
        self.pll = pll = ECP5PLL()
        self.comb += pll.reset.eq(~rst_n | self.rst)
        pll.register_clkin(clk, clk_freq)
        pll.create_clkout(self.cd_sys, sys_clk_freq)

# BaseSoC ------------------------------------------------------------------------------------------
class BaseSoC(SoCCore):
    def __init__(self, sys_clk_freq=100e6, toolchain="trellis", **kwargs):
        platform = ecp5card.Platform(toolchain=toolchain)

        # CRG --------------------------------------------------------------------------------------
        self.crg = _CRG(platform, sys_clk_freq,  with_rst = True)

        # SoCCore ----------------------------------------------------------------------------------
        # SOC disable internal ROM
        # kwargs["integrated_rom_size"] = 0
        SoCCore.__init__(self, platform, int(sys_clk_freq), ident="LiteX SoC on Custom ECP5", **kwargs)    

        # RAM for BootLoader -----------------------------------------------------------------------
        BASE_MEM1_ORIGIN        = 0x60000000
        self.add_ram(name="mem1", origin=BASE_MEM1_ORIGIN, size=10*kB)        

        # SPI Flash4x ------------------------------------------------------------------------------
        # from litespi.modules import W25Q128JV
        # from litespi.opcodes import SpiNorFlashOpCodes as Codes
        # self.mem_map["spiflash"] = 0x0000000
        # self.add_spi_flash(mode="4x", module=W25Q128JV(Codes.READ_1_1_4), rate="1:1", with_master=True)

        # Add ROM linker region --------------------------------------------------------------------
        # self.bus.add_region("rom", SoCRegion(
        #     origin = self.bus.regions["spiflash"].origin + 0x800000,
        #     size   = 64 * KILOBYTE,
        #     linker = True)
        # )
        # self.cpu.set_reset_address(self.bus.regions["rom"].origin)

        ### UART -----------------------------------------------------------------------------------
        # Secara default, SoC ini menggunakan UART. Namun, jika SoC dibangun dengan opsi --no-uart, 
        # maka UART tidak akan diaktifkan secara otomatis. Dalam kondisi ini, 
        # Anda dapat mengaktifkan kembali UART secara manual menggunakan kode berikut:
        
        # self.add_uart(name="uart", uart_name="serial", baudrate=115200, fifo_depth=16, with_dynamic_baudrate=False)


        # Leds -------------------------------------------------------------------------------------
        # Hardware LED
        # self.submodules.leds = LedChaser(
        #     pads=platform.request_all("user_led"),
        #     sys_clk_freq=sys_clk_freq,
        #     period=0.5
        # )

        # GPIO LED
        # GPIO -------------------------------------------------------------------------------------
        user_leds = platform.request_all("user_led")
        self.gpio = GPIOOut(user_leds)
        self.add_csr("gpio")

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
    # builder = Builder(soc, **parser.builder_argdict)
    builder = Builder(soc, compile_gateware=True, compile_software=True)

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