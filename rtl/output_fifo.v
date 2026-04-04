module output_fifo #(
    parameter DATA_WIDTH = 24,
    parameter DEPTH = 16
)(
    input  wire                   clk,
    input  wire                   rst_n,

    input  wire [DATA_WIDTH-1:0]  data_in,
    input  wire                   valid_in,
    output wire                   ready_out,

    output wire [DATA_WIDTH-1:0]  data_out,
    output wire                   valid_out,
    input  wire                   ready_in,

    output wire                   fifo_full,
    output wire                   fifo_empty
);

    reg [DATA_WIDTH-1:0] fifo_mem [0:DEPTH-1];

    reg [$clog2(DEPTH):0] wr_ptr;
    reg [$clog2(DEPTH):0] rd_ptr;
    reg [$clog2(DEPTH+1)-1:0] fifo_count;

    assign fifo_full  = (fifo_count == DEPTH);
    assign fifo_empty = (fifo_count == 0);

    assign ready_out = ~fifo_full;
    assign valid_out = ~fifo_empty;

    assign data_out = fifo_mem[rd_ptr[$clog2(DEPTH)-1:0]];

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wr_ptr <= 0;
            rd_ptr <= 0;
            fifo_count <= 0;
        end
        else begin

            // Write only
            if (valid_in && ready_out && !(valid_out && ready_in)) begin
                fifo_mem[wr_ptr[$clog2(DEPTH)-1:0]] <= data_in;
                wr_ptr <= wr_ptr + 1;
                fifo_count <= fifo_count + 1;
            end

            // Read only
            else if (!(valid_in && ready_out) && valid_out && ready_in) begin
                rd_ptr <= rd_ptr + 1;
                fifo_count <= fifo_count - 1;
            end

            // Simultaneous read and write
            else if (valid_in && ready_out && valid_out && ready_in) begin
                fifo_mem[wr_ptr[$clog2(DEPTH)-1:0]] <= data_in;
                wr_ptr <= wr_ptr + 1;
                rd_ptr <= rd_ptr + 1;
            end
        end
    end

endmodule