`default_nettype none

module blink(
    input  wire         clk,
    input  wire         button,
    output wire         led1,
    output wire         rstn
);

    reg [25:0] cntr = 0;

    always @(posedge clk)
    begin
        cntr    <= cntr + 1;
        if (!button) begin
            cntr    <= 0;
        end 
    end

    assign led1 = ~cntr[24];
    assign rstn = 1'b1;

endmodule
