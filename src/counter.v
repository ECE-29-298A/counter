module counter (
    input  wire       clk,
    input  wire       rst_n,
    output reg  [7:0] countval
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            countval <= 8'b0;
        else
            countval <= countval + 1'b1;
    end
endmodule
