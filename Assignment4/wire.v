module IFWire(PCF,PCPlus4,FETCH_ADDRESS);
    input[31:0] PCF;
    output[31:0] PCPlus4,FETCH_ADDRESS;

    wire[31:0] PCPlus4_mid,FETCH_ADDRESS_mid;

    assign PCPlus4 = PCPlus4_mid;
    assign PCPlus4_mid = PCF + 4;
    assign FETCH_ADDRESS = FETCH_ADDRESS_mid;
    assign FETCH_ADDRESS_mid = PCF / 4;
endmodule


module IDWire(Instr,opcopde,functioncode,rs,rt,rd,shamt,SignImm,UnsignImm,part_jump);
    input[31:0] Instr;
    output[5:0] opcopde,functioncode;
    output[4:0] rs,rt,rd,shamt;
    output[31:0] SignImm,UnsignImm;
    output[25:0] part_jump;

    wire[5:0] opmid;
    wire[5:0] rsmid,rtmid,rdmid,shamtmid;
    wire[31:0] n_im,p_im;



    assign opcopde = opmid;
    assign opmid = Instr[31:26];
    assign functioncode = Instr[5:0];

    assign rs = rsmid;
    assign rsmid = Instr[25:21];
    assign rt = rtmid;
    assign rtmid = Instr[20:16];
    assign rd = rdmid;
    assign rdmid = Instr[15:11];
    assign shamt = shamtmid;
    assign shamtmid = Instr[10:6];

    assign SignImm = Instr[15] == 1'b1 ? n_im: p_im;
    assign n_im = {16'hffff, Instr[15:0]};
    assign p_im = {16'h0000, Instr[15:0]};
    assign UnsignImm = {16'h0000, Instr[15:0]};

    assign part_jump = Instr[25:0];

endmodule

module EXWire(LinkE,PCPlus4,ALUOut,RD2,Rd,Rt,RegDstE,SignImm,ALUOutE,WriteData,WriteRegE,PCBranch);
    input LinkE,RegDstE;
    input[31:0] PCPlus4,ALUOut,RD2;
    input[4:0] Rd,Rt;
    input[31:0] SignImm;
    output[31:0] ALUOutE;
    output[31:0] WriteData,PCBranch;
    output[4:0] WriteRegE;

    wire[31:0] f_aluout,s_aluout; 
    wire[4:0] f_WriteReg, s_WriteReg; 
    wire[31:0] sign_shaft;

    assign ALUOutE = LinkE == 1'b1 ? f_aluout : s_aluout;
    assign f_aluout = PCPlus4;
    assign s_aluout  = ALUOut;
     
    assign WriteData = RD2;

    assign WriteRegE = RegDstE == 1'b1 ? f_WriteReg : s_WriteReg;
    assign f_WriteReg = Rd;
    assign s_WriteReg = Rt;

    assign PCBranch = PCPlus4 +sign_shaft;
    assign sign_shaft = SignImm << 2;

endmodule


module MEMWire(Controlin,ALUOut,MemWrite,Branch,RegWriteM,Controlout,FETCH_ADDRESS);
    input[3:0] Controlin;
    input[31:0] ALUOut;
    output MemWrite,Branch,RegWriteM;
    output[1:0] Controlout;
    output[31:0] FETCH_ADDRESS;

    wire[31:0] nor_add;

    assign MemWrite = Controlin[1];
    assign Branch = Controlin[0];
    assign Controlout = Controlin[3:2];
    assign RegWriteM = Controlin[3];

    assign nor_add = ALUOut/4;
    assign FETCH_ADDRESS = nor_add;

endmodule

module WBWire(Controlin,RD,ALUOut,RegWrite,MemtoReg,Result);
    input[1:0] Controlin;
    input[31:0] RD,ALUOut;
    output[31:0] Result;
    output RegWrite,MemtoReg;

    wire[31:0] f_re,s_re;

    assign RegWrite = Controlin[1];
    assign MemtoReg = Controlin[0];

    assign f_re = RD;
    assign s_re = ALUOut;
    assign Result = MemtoReg == 1'b1 ? f_re : s_re;
endmodule