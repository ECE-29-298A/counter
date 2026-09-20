module tristate (
    input wire in,
    input wire tricont,
    output wire out
);

assign out = (tricont) ? in : 1'bz;
    
endmodule