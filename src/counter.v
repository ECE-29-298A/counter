module counter (
    input clk,
    input reset,
    input tristate,
    output [7:0] count
);

    reg [7:0] counter;
    always@(posedge clk or posedge reset) begin
        if(reset)
            counter <= 8'b0;
        else
            counter <= counter +1;
    end

    assign count = tristate ? 8'bz : counter;
endmodule