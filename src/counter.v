module counter (
    input wire clk,
    input wire rst_n,
    output wire [7:0] countval
);

reg [7:0] counter;
reg [1:0] rsync;

always@(posedge clk or negedge rst_n) begin 
    if (!rst_n) begin 
        rsync <= 2'b00;
    end else begin 
        rsync <= {rsync[0], 1'b1};
    end
end

always@(posedge clk or negedge rst_n) begin 
    if (!rst_n) begin 
        counter <= 8'h00;
    end 
    else if (!rsync[1]) begin 
        counter <= 8'h00;
    end 
    else begin 
        if (counter != 8'hFF) begin 
            counter <= counter + 1;
        end else begin 
            counter <= 8'h00;
        end
    end
end

assign countval = counter;
    
endmodule