module white_balance(
    input  wire [7:0] r_in,
    input  wire [7:0] g_in,
    input  wire [7:0] b_in,

    output reg [7:0] r_out,
    output reg [7:0] g_out,
    output reg [7:0] b_out
);

reg [15:0] r_temp;
reg [15:0] g_temp;
reg [15:0] b_temp;

always @(*) begin
    r_temp = (r_in * 280) >> 8;
    g_temp = (g_in * 256) >> 8;
    b_temp = (b_in * 300) >> 8;

    r_out = (r_temp > 255) ? 255 : r_temp[7:0];
    g_out = (g_temp > 255) ? 255 : g_temp[7:0];
    b_out = (b_temp > 255) ? 255 : b_temp[7:0];
end

endmodule