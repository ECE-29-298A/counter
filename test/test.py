# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, ReadOnly, RisingEdge, Timer


@cocotb.test()
async def test_project(dut):
    # The input buses are unused. Drive non-zero values to confirm they do not
    # gate or otherwise change the counter output.
    dut.ena.value = 1
    dut.ui_in.value = 0xA5
    dut.uio_in.value = 0x5A
    dut.rst_n.value = 0

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Hold reset through multiple clock edges and verify all outputs.
    await ClockCycles(dut.clk, 2)
    await ReadOnly()
    assert int(dut.uo_out.value) == 0
    assert int(dut.uio_out.value) == 0
    assert int(dut.uio_oe.value) == 0

    # Leave the read-only phase before driving reset.
    await Timer(1, unit="ns")
    dut.rst_n.value = 1

    # Check every value in a complete 8-bit cycle, including wraparound.
    for cycle in range(256):
        await RisingEdge(dut.clk)
        await ReadOnly()
        expected = (cycle + 1) & 0xFF
        observed = int(dut.uo_out.value)
        assert observed == expected, (
            f"Cycle {cycle + 1}: expected {expected}, got {observed}"
        )

    # Move away from the sampled edge, count up again, then verify that the
    # active-low asynchronous reset clears the counter before another edge.
    await Timer(1, unit="ns")
    for expected in range(1, 6):
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert int(dut.uo_out.value) == expected
        await Timer(1, unit="ns")

    dut.rst_n.value = 0
    await Timer(1, unit="ns")
    await ReadOnly()
    assert int(dut.uo_out.value) == 0
