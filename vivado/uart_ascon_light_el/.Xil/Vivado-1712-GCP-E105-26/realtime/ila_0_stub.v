// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2024 Advanced Micro Devices, Inc. All Rights Reserved.

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
(* X_CORE_INFO = "ila,Vivado 2024.1" *)
module ila_0(clk, probe0, probe1, probe2, probe3);
  input clk /* synthesis syn_isclock = 1 */;
  input [0:0]probe0;
  input [127:0]probe1;
  input [127:0]probe2;
  input [63:0]probe3;
endmodule
