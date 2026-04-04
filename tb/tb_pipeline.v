`timescale 1ns / 1ps

module tb_pipeline;

parameter FRAME_WIDTH  = 32;
parameter FRAME_HEIGHT = 8;
parameter PIXEL_WIDTH  = 8;

reg clk;
reg rst;
reg valid_in;
reg [PIXEL_WIDTH-1:0] pixel_in;
reg [5:0] x;
reg [3:0] y;

wire valid_out;
wire [7:0] r_out;
wire [7:0] g_out;
wire [7:0] b_out;

integer frame;
integer file_processed;
integer pixel_count;

// Latency measurement
integer cycle_counter;
integer first_input_cycle;
integer first_output_cycle;
integer latency_cycles;
integer input_seen;
integer output_seen;

pipeline_top #(
    .FRAME_WIDTH(FRAME_WIDTH),
    .FRAME_HEIGHT(FRAME_HEIGHT),
    .PIXEL_WIDTH(PIXEL_WIDTH)
) dut (
    .clk(clk),
    .rst(rst),
    .valid_in(valid_in),
    .pixel_in(pixel_in),
    .x(x),
    .y(y),
    .valid_out(valid_out),
    .r_out(r_out),
    .g_out(g_out),
    .b_out(b_out)
);

always #5 clk = ~clk;

// Global cycle counter
always @(posedge clk) begin
    if (rst)
        cycle_counter <= 0;
    else
        cycle_counter <= cycle_counter + 1;
end

// Capture first valid input cycle
always @(posedge clk) begin
    if (!rst && valid_in && !input_seen) begin
        first_input_cycle <= cycle_counter;
        input_seen <= 1;
    end
end

// Capture first valid output cycle
always @(posedge clk) begin
    if (!rst && valid_out && !output_seen) begin
        first_output_cycle <= cycle_counter;
        output_seen <= 1;

        latency_cycles <= cycle_counter - first_input_cycle;

        $display("======================================");
        $display("Pipeline Latency Report");
        $display("First Valid Input Cycle  = %0d", first_input_cycle);
        $display("First Valid Output Cycle = %0d", cycle_counter);
        $display("Pipeline Latency         = %0d cycles", cycle_counter - first_input_cycle);
        $display("======================================");
    end
end

// Write outputs whenever valid_out is high
always @(posedge clk) begin
    if (valid_out) begin
        $fwrite(file_processed, "%0d %0d %0d\n", r_out, g_out, b_out);
        pixel_count = pixel_count + 1;
    end
end

initial begin
    clk = 0;
    rst = 1;
    valid_in = 0;
    pixel_in = 0;
    x = 0;
    y = 0;
    pixel_count = 0;

    cycle_counter = 0;
    first_input_cycle = 0;
    first_output_cycle = 0;
    latency_cycles = 0;
    input_seen = 0;
    output_seen = 0;

    #20;
    rst = 0;

    for (frame = 1; frame <= 3; frame = frame + 1) begin

        pixel_count = 0;

        if (frame == 1)
            file_processed = $fopen("processed_frame_1.txt", "w");
        else if (frame == 2)
            file_processed = $fopen("processed_frame_2.txt", "w");
        else
            file_processed = $fopen("processed_frame_3.txt", "w");

        for (y = 0; y < FRAME_HEIGHT; y = y + 1) begin
            for (x = 0; x < FRAME_WIDTH; x = x + 1) begin

                @(posedge clk);
                valid_in = 1;

                if (x < 2)
                    pixel_in = 0;
                else if (x < 14)
                    pixel_in = (y < 4) ? 220 : 140;
                else if (x < 20)
                    pixel_in = 100 + (x * 3);
                else
                    pixel_in = 160 + ((x + frame) % 2) * 40;
            end
        end

        @(posedge clk);
        valid_in = 0;

        // Allow FIFO to flush remaining pixels
        repeat (20) @(posedge clk);

        $display("Frame %0d complete: %0d pixels written", frame, pixel_count);

        $fclose(file_processed);
    end

    $display("======================================");
    $display("Final Summary");
    $display("Pipeline Latency = %0d cycles", latency_cycles);
    $display("Throughput       = 1 pixel per clock after pipeline fill");
    $display("======================================");

    #50;
    $finish;
end

endmodule