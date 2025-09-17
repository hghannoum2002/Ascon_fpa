`timescale 1ns / 1ps
module ASCON_TOP(
      input logic clock_i,
   input logic reset_i,
   
    input logic start_i,
    input logic [63:0] data_i,
    input logic [127:0]key_i,
    input logic [127:0] nonce_i,

    output logic [63:0] cipher_o,
   
    output logic [127:0]tag_o,
    output logic end_o,
	
   output logic cipher_valid_o,
    output logic init_register_o,
    output logic enable_register_o,
    output logic [4:0] cpt_o
);
     
//compteur

logic en_s,init_a_s;
logic [4 : 0] cpt_s;
//fsm
logic init_ascon_s;
logic associate_data_s;
logic finalisation_s;
logic data_valid_s;
logic end_ascon_s;
// fsm output
logic end_associate_s;
logic end_initialisation_s;
logic end_cipher_s;

 assign cpt_o=cpt_s;
  ascon A (
    // inputs
    .clock_i(clock_i),
    .reset_i(reset_i),
    .init_i(init_ascon_s),//fsm
   .associate_data_i(associate_data_s),//fsm
    .finalisation_i(finalisation_s),//fsm
    .data_i(data_i),
    .data_valid_i(data_valid_s),//fsm
    .key_i(key_i),
    .nonce_i(nonce_i),
    // outputs
    .end_associate_o(end_associate_s),//fsm
    .cipher_o(cipher_o),
    .cipher_valid_o(cipher_valid_o),
    .tag_o(tag_o),
    .end_tag_o(end_ascon_s),
    .end_initialisation_o(end_initialisation_s),//fsm
    .end_cipher_o(end_cipher_s)//fsm
);
     compteur cmpt
   (
    .clock_i(clock_i),
   .resetb_i(reset_i),
 .en_i(en_s),
  .init_a_i(init_a_s),
   .cpt_o(cpt_s)      
    ) ;
  fsm FSM_ASCON(
	.clock_i(clock_i),
	.reset_i(reset_i),
	.start_i(start_i),
//init ascon
	.init_ascon_o(init_ascon_s),
//end init
	.end_initialisation_i(end_initialisation_s),
//start donneee associees
	.associate_data_o(associate_data_s),

//data valid
	.data_valid_o(data_valid_s),
// receive end associate 
	.end_associate_i(end_associate_s),
//data valid + plain text

//counter 
	.en_counter_o(en_s),
	.init_a_o(init_a_s),
	.cpt_i(cpt_s),
// receive end cipher  for 23 blocks
	.end_cipher_i(end_cipher_s),
// start finalisation
	.finalisation_o(finalisation_s),

 	
// receive end_tag
	.end_ascon_i(end_ascon_s),
	.end_o(end_o)	,
	.init_register_o(init_register_o),
	.enable_register_o(enable_register_o)
	
);
endmodule:ASCON_TOP
