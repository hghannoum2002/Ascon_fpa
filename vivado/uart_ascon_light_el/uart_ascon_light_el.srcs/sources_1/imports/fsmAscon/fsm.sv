`timescale 1ns / 1ps

  module fsm (
	input logic clock_i,
	input logic reset_i,
	input logic start_i,
//init ascon
	output logic init_ascon_o,
//end init
	input logic end_initialisation_i,
//start donneee associees
	output logic associate_data_o,

//data valid
	output logic data_valid_o,
// receive end associate 
	input logic end_associate_i,
//data valid + plain text

//counter 
	output logic en_counter_o,
	output logic init_a_o,
	input logic [4:0] cpt_i,
// receive end cipher  for 23 blocks
	input logic end_cipher_i,
// start finalisation
	output logic finalisation_o,

 	
// receive end_tag
	input logic end_ascon_i,
	output logic end_o,
	output logic init_register_o,
	output logic enable_register_o
	
);
    
    typedef enum {
	idle, 
	INIT,
	END_INIT,
	ASSOCIATE_DATA, 
	END_ASSOCIATE_DATA, 
	START_CIPHER, 
	CIPHER,  
	END_CIPHER,
	START_FINALIZATION,
	FINALIZATION, 
        ADD,
	END_FINALIZATION, 
	END_global
	} state_t;
    
    
    state_t state, next_state;
    

    //squential process 
    always_ff @(posedge clock_i or  negedge reset_i) begin: seq_0
        if(reset_i ==1'b0)
            state <= idle;
        else
            state <= next_state;
    end : seq_0

    
    
 
    always_comb begin : comb_0
        case(state)
            idle:
		if(start_i==1'b1)    next_state=INIT;
		else next_state=idle;
            INIT:                       
                if(end_initialisation_i == 1'b0)
                    next_state=INIT;
                else
                    next_state=END_INIT;
	    END_INIT:
		next_state=ASSOCIATE_DATA;

            ASSOCIATE_DATA:
           
            next_state=END_ASSOCIATE_DATA;
           
                
                
            END_ASSOCIATE_DATA:
                if(end_associate_i == 1'b0)
                    next_state=END_ASSOCIATE_DATA;
                else
                    next_state=START_CIPHER;
                    
                    
            START_CIPHER:
        
                   next_state=CIPHER;
                    
                    
                    
            CIPHER:
                if(end_cipher_i == 1'b0)
                    next_state=CIPHER;
                else
                    next_state= END_CIPHER;
                    
                    
             END_CIPHER:
                if(cpt_i == 5'b10100)
                    next_state=START_FINALIZATION;
                else
                    next_state=START_CIPHER;
                    
             START_FINALIZATION:
		 next_state=FINALIZATION;
            FINALIZATION:
 
                next_state=END_FINALIZATION;
             
                
            END_FINALIZATION:
                if(end_ascon_i == 1'b0)
                    next_state=END_FINALIZATION;
                else
                    next_state=END_global;
                    
                    
            END_global:
                next_state=idle;
            default:
                next_state=idle;
        endcase
    end : comb_0

     always_comb begin : comb_1
	init_ascon_o=0;
	associate_data_o=0;
	data_valid_o=0;
	en_counter_o=0;
	init_a_o=0;
	finalisation_o=0;
	end_o=0;
	init_register_o=0;
	enable_register_o=0;
        case(state)
            idle:
               begin
		init_ascon_o=0;
		associate_data_o=0;
		data_valid_o=0;
		en_counter_o=0;
		init_a_o=1;
		finalisation_o=0;
		end_o=0;
		init_register_o=1;
		enable_register_o=0;
               end
            INIT:
                begin
		init_ascon_o=1;
		associate_data_o=0;
		data_valid_o=0;
		en_counter_o=0;
		init_a_o=0;
		finalisation_o=0;
		end_o=0;
		init_register_o=0;
		enable_register_o=0;
                end
	    END_INIT:
		begin
		init_ascon_o=0;
		associate_data_o=1;
		data_valid_o=0;
		en_counter_o=0;
		init_a_o=0;
		finalisation_o=0;
		end_o=0;
		init_register_o=0;
		enable_register_o=0;
                end
            ASSOCIATE_DATA:
                begin
		init_ascon_o=0;
		associate_data_o=1;
		data_valid_o=1;
		en_counter_o=0;
		init_a_o=0;
		finalisation_o=0;
		end_o=0;
		init_register_o=0;
		enable_register_o=0;
                end
            END_ASSOCIATE_DATA:
                begin
		init_ascon_o=0;
		associate_data_o=0;
		data_valid_o=0;
		en_counter_o=0;
		init_a_o=0;
		finalisation_o=0;
		end_o=0;
		init_register_o=0;
		enable_register_o=0;
                end
            
           START_CIPHER:
                begin
		init_ascon_o=0;
		associate_data_o=0;
		data_valid_o=1;
		en_counter_o=0;
		init_a_o=0;
		finalisation_o=0;
		end_o=0;
		init_register_o=0;
		enable_register_o=0;
                end
            CIPHER:
		begin
		init_ascon_o=0;
		associate_data_o=0;
		data_valid_o=1;
		en_counter_o=0;
		init_a_o=0;
		finalisation_o=0;
		end_o=0;
		init_register_o=0;
		enable_register_o=0;
                end
            END_CIPHER:
                begin
		init_ascon_o=0;
		associate_data_o=0;
		data_valid_o=0;
		en_counter_o=1;
		init_a_o=0;
		finalisation_o=0;
		end_o=0;
		init_register_o=0;
		enable_register_o=1;
                end
	    START_FINALIZATION:
		          
                begin
		init_ascon_o=0;
		associate_data_o=0;
		data_valid_o=0;
		en_counter_o=1;
		init_a_o=0;
		finalisation_o=0;
		end_o=0;
		init_register_o=0;
		enable_register_o=0;
                end
            FINALIZATION:
                begin
		init_ascon_o=0;
		associate_data_o=0;
		data_valid_o=0;
		en_counter_o=0;
		init_a_o=0;
		finalisation_o=0;
		end_o=0;
		init_register_o=0;
		enable_register_o=0;
                end


             
            END_FINALIZATION:
                begin
		init_ascon_o=0;
		associate_data_o=0;
		data_valid_o=1;
		en_counter_o=0;
		init_a_o=0;
		finalisation_o=1;
		end_o=0;
		init_register_o=0;
		enable_register_o=0;
                end
            END_global:
               begin
		init_ascon_o=0;
		associate_data_o=0;
		data_valid_o=0;
		en_counter_o=0;
		init_a_o=0;
		finalisation_o=0;
		end_o=1;
		init_register_o=0;
		enable_register_o=0;
                end
        endcase
    end: comb_1
endmodule : fsm

