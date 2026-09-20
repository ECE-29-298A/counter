module top (
    input wire clk,
    input wire rst_n,
    input wire [7:0] config_out,
    output wire [7:0] count_out
);

wire [7:0] count_val;

genvar i;
generate 
for (i = 0; i < 8; i++) begin 
    tristate u_tristate(
        .in(count_val[i]),
        .tricont(config_out[i]),
        .out(count_out[i])
    );
end
endgenerate

counter u_counter(
    .clk(clk),
    .rst_n(rst_n),
    .countval(count_val)
);

endmodule