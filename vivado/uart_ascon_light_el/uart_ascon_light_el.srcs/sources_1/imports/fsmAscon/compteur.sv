`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 14.03.2025 13:34:19
// Design Name: 
// Module Name: compteur
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module compteur(
    input logic     clock_i,
    input logic     resetb_i,
    input logic     en_i,
    input logic     init_a_i,
    output logic [4 : 0] cpt_o      
    ) ;

   logic [4 : 0] cpt_s;
   
   always_ff @(posedge clock_i or negedge resetb_i)
     begin
    if (resetb_i == 1'b0) begin
       cpt_s <= 0;
    end
    else begin
       if (en_i == 1'b1)
         begin
        if (init_a_i==1'b1) begin
           cpt_s<=0;
        end
        else cpt_s <= cpt_s+1;
         end
    end
     end

   assign cpt_o = cpt_s;
   
endmodule: compteur
 
