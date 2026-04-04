module tnr(
    input  wire clk,
    input  wire rst,
    input  wire valid_in,
    input  wire [7:0] r_in,
    input  wire [7:0] g_in,
    input  wire [7:0] b_in,

    output reg [7:0] r_out,
    output reg [7:0] g_out,
    output reg [7:0] b_out
);

reg [7:0] prev_r;
reg [7:0] prev_g;
reg [7:0] prev_b;

wire [7:0] diff_r;
wire [7:0] diff_g;
wire [7:0] diff_b;

assign diff_r = (r_in > prev_r) ? (r_in - prev_r) : (prev_r - r_in);
assign diff_g = (g_in > prev_g) ? (g_in - prev_g) : (prev_g - g_in);
assign diff_b = (b_in > prev_b) ? (b_in - prev_b) : (prev_b - b_in);

always @(posedge clk or posedge rst) begin
    if (rst) begin
        prev_r <= 0;
        prev_g <= 0;
        prev_b <= 0;
        r_out <= 0;
        g_out <= 0;
        b_out <= 0;
    end
    else if (valid_in) begin
        if ((diff_r > 20) || (diff_g > 20) || (diff_b > 20)) begin
            r_out <= r_in;
            g_out <= g_in;
            b_out <= b_in;
        end
        else begin
            r_out <= (r_in + prev_r) >> 1;
            g_out <= (g_in + prev_g) >> 1;
            b_out <= (b_in + prev_b) >> 1;
        end

        prev_r <= r_in;
        prev_g <= g_in;
        prev_b <= b_in;
    end
end

endmodule