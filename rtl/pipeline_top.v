module pipeline_top #(
    parameter FRAME_WIDTH  = 32,
    parameter FRAME_HEIGHT = 8,
    parameter PIXEL_WIDTH  = 8
)(
    input  wire clk,
    input  wire rst,
    input  wire valid_in,
    input  wire [PIXEL_WIDTH-1:0] pixel_in,
    input  wire [5:0] x,
    input  wire [3:0] y,

    output wire valid_out,
    output wire [7:0] r_out,
    output wire [7:0] g_out,
    output wire [7:0] b_out
);

wire [7:0] r_demo;
wire [7:0] g_demo;
wire [7:0] b_demo;

wire [7:0] r_wb;
wire [7:0] g_wb;
wire [7:0] b_wb;

wire [7:0] r_gamma;
wire [7:0] g_gamma;
wire [7:0] b_gamma;

wire [7:0] r_tnr;
wire [7:0] g_tnr;
wire [7:0] b_tnr;

// FIFO signals
wire [23:0] fifo_data_in;
wire [23:0] fifo_data_out;

wire fifo_valid_in;
wire fifo_ready_out;
wire fifo_valid_out;
wire fifo_ready_in;

wire fifo_full;
wire fifo_empty;

demosaic demosaic_inst (
    .pixel_in(pixel_in),
    .x(x),
    .y(y),
    .r_out(r_demo),
    .g_out(g_demo),
    .b_out(b_demo)
);

white_balance wb_inst (
    .r_in(r_demo),
    .g_in(g_demo),
    .b_in(b_demo),
    .r_out(r_wb),
    .g_out(g_wb),
    .b_out(b_wb)
);

gamma_lut gamma_inst (
    .r_in(r_wb),
    .g_in(g_wb),
    .b_in(b_wb),
    .r_out(r_gamma),
    .g_out(g_gamma),
    .b_out(b_gamma)
);

tnr tnr_inst (
    .clk(clk),
    .rst(rst),
    .valid_in(valid_in),
    .r_in(r_gamma),
    .g_in(g_gamma),
    .b_in(b_gamma),
    .r_out(r_tnr),
    .g_out(g_tnr),
    .b_out(b_tnr)
);

// Pack RGB into FIFO input
assign fifo_data_in  = {r_tnr, g_tnr, b_tnr};
assign fifo_valid_in = valid_in;
assign fifo_ready_in = 1'b1;

// FIFO instance
output_fifo #(
    .DATA_WIDTH(24),
    .DEPTH(16)
) fifo_inst (
    .clk(clk),
    .rst_n(~rst),

    .data_in(fifo_data_in),
    .valid_in(fifo_valid_in),
    .ready_out(fifo_ready_out),

    .data_out(fifo_data_out),
    .valid_out(fifo_valid_out),
    .ready_in(fifo_ready_in),

    .fifo_full(fifo_full),
    .fifo_empty(fifo_empty)
);

// Final outputs from FIFO
assign r_out = fifo_data_out[23:16];
assign g_out = fifo_data_out[15:8];
assign b_out = fifo_data_out[7:0];

assign valid_out = fifo_valid_out;

endmodule