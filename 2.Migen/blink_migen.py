from migen import *

class Blink(Module):
    def __init__(self):
        self.button = Signal()      # input
        self.led1   = Signal()      # output

        cntr = Signal(26, reset=0)

        # Synchronous logic
        self.sync += [
            If(~self.button,
                cntr.eq(0)
            ).Else(
                cntr.eq(cntr + 1)
            )
        ]

        # Combinatorial assignments
        self.comb += [
            self.led1.eq(~cntr[24]),
        ]

# Generate Verilog
if __name__ == "__main__":
    blink = Blink()
    from migen.fhdl import verilog
    print(verilog.convert(
        blink,
        ios={blink.button, blink.led1}
    ))