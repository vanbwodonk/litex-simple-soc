/* Machine-generated using Migen */
module top(
	input button,
	output led1,
	input sys_clk,
	input sys_rst
);

reg [25:0] cntr = 26'd0;

// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign led1 = (~cntr[24]);

always @(posedge sys_clk) begin
	if ((~button)) begin
		cntr <= 1'd0;
	end else begin
		cntr <= (cntr + 1'd1);
	end
	if (sys_rst) begin
		cntr <= 26'd0;
	end
end

endmodule


