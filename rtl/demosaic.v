module demosaic(
    input  wire [7:0] pixel_in,
    input  wire [5:0] x,
    input  wire [3:0] y,

    output reg [7:0] r_out,
    output reg [7:0] g_out,
    output reg [7:0] b_out
);

always @(*) begin
    r_out = 0;
    g_out = 0;
    b_out = 0;

    // RGGB Bayer pattern
    if ((y % 2 == 0) && (x % 2 == 0)) begin
        r_out = pixel_in;
        g_out = pixel_in >> 1;
        b_out = pixel_in >> 2;
    end
    else if ((y % 2 == 0) && (x % 2 == 1)) begin
        r_out = pixel_in >> 1;
        g_out = pixel_in;
        b_out = pixel_in >> 1;
    end
    else if ((y % 2 == 1) && (x % 2 == 0)) begin
        r_out = pixel_in >> 1;
        g_out = pixel_in;
        b_out = pixel_in >> 1;
    end
    else begin
        r_out = pixel_in >> 2;
        g_out = pixel_in >> 1;
        b_out = pixel_in;
    end
end

endmodule