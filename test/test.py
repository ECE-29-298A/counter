# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, ReadOnly
from random import randint

def config_outen(dut, confval):
    dut.ui_in.value = confval & 0b1111_1111


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.ui_in.value = 20
    dut.uio_in.value = 30

    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 1)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:


    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.

    #assert reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 4)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    # test output
    config_outen(dut, 0xFF)
    expected = -1
    previous = -1
    await RisingEdge(dut.clk)

    for _ in range(300):
        dut._log.info(f"uo_out = {dut.uo_out.value}")
        observed = dut.uo_out.value
        
        if (expected != 255):
            expected = expected + 1
        else:
            expected = 0

        assert observed == expected, (f"Expected {expected}, got {observed}; previous value was {previous}")

        previous = observed
        await RisingEdge(dut.clk)


    # reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 4)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)


    expected = -1
    previous = -1

    # it works but semeantics causes it to break on post GDS since highZ isnt well represented.
    
    # # test highz
    # for _ in range(300):
    #     outen = randint(0, 255)
    #     config_outen(dut, outen)
    #     await RisingEdge(dut.clk)
    #     expected = (expected +1) & 0xFF

    #     expected_str = ""
    #     for i in range(7, -1, -1):
    #         if ((outen >> i) & 1) == 0:
    #             expected_str += "Z"
    #         else:
    #             expected_str += str((expected >> i) & 1)

    #     observed = str(dut.uo_out.value)

    #     dut._log.info(
    #         f"config value={outen:08b}, expected={expected_str}, observed={observed}"
    #     )
    #     assert observed == expected_str, (
    #         f"config value={outen:08b}: expected {expected_str}, got {observed}"
    #     )
        

        

    