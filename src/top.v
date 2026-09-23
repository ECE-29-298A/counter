module top (
    input  wire       clk,
    input  wire       rst_n,
    output wire [7:0] count_out
);

    counter u_counter (
        .clk      (clk),
        .rst_n    (rst_n),
        .countval (count_out)
    );

endmodule
