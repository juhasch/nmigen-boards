import os
import subprocess

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .resources import *


__all__ = ["ICEZeroPlatform"]


class ICEZeroPlatform(LatticeICE40Platform):
    device      = "iCE40HX4K"
    package     = "TQ144"
    default_clk = "clk100"
    resources   = [
        Resource("clk100", 0, Pins("49", dir="i"),
                 Clock(100e6), Attrs(GLOBAL=True, IO_STANDARD="SB_LVCMOS")),

        *LEDResources(pins="110 93 94", attrs=Attrs(IO_STANDARD="SB_LVCMOS")),

        *ButtonResources(
            pins="63", invert=True,
            attrs=Attrs(IO_STANDARD="SB_LVCMOS")),

       SRAMResource(0,
            cs="24", oe="76", we="11",
            a="34 33 32 31 25 10 9 4 3 2 107 106 105 104 102 62 60 61 98",
            d="23 22 19 18 17 16 15 12 97 96 95 91 84 82 83 80",
            dm="75 81",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS"),
        ),

    ]
    connectors  = [
        Connector("pmod", 0, "141 138 136 134 - - 139 137 135 130 - -"),  # PMOD1
        Connector("pmod", 1, "55 47 44 42 - - 56 48 45 43 - -"),  # PMOD2
        Connector("pmod", 2, "41 39 38 37 - - 26 29 28 52 - -"),  # PMOD3
        Connector("pmod", 3, "1 144 143 142 - - 21 20 26 27 - -"),  # PMOD4

    ]

    def toolchain_program(self, products, name):
        iceprog = os.environ.get("ICEZPROG", "icezprog")
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call([iceprog, bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import *
    ICEStickPlatform().build(Blinky(), do_program=True)
