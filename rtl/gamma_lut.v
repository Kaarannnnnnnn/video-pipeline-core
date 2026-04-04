module gamma_lut(
    input  wire [7:0] r_in,
    input  wire [7:0] g_in,
    input  wire [7:0] b_in,

    output reg [7:0] r_out,
    output reg [7:0] g_out,
    output reg [7:0] b_out
);

always @(*) begin
    r_out = (r_in > 200) ? 255 : (r_in + (r_in >> 2));
    g_out = (g_in > 200) ? 255 : (g_in + (g_in >> 3));
    b_out = (b_in > 200) ? 255 : (b_in + (b_in >> 2));
end

endmodule