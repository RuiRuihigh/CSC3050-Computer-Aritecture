module EX(CLK,Controlin, ALUcontrol, RD1, RD2, Rs,Rt, Rd, Shamt,
 SignImm, PCPlus4, 
 Zero, ALUOutE, WriteData, PCBranch, Controlout, WriteRegE,
 RegWriteM,RegWriteW,WRiteRegM,WriteRegW,ALUOutM,ResultW);
    input[31:0] ALUOutM,ResultW;
    input RegWriteM,RegWriteW;
    input[4:0] WRiteRegM,WriteRegW;
    input CLK;
    input[7:0] Controlin;
    /*     3 : RegWrite, 2 : MemtoReg, 1 : MemWrite,  0 : Branch,  */  
    output[3:0] Controlout;
    input[3:0] ALUcontrol;
    input[31:0] RD1, RD2;
    input[4:0] Rs,Rt, Rd, Shamt;//ShamtE 32 bit
    input[31:0] SignImm;
    input[31:0]  PCPlus4;
    output Zero;
    output[31:0] ALUOutE, WriteData;
    output[31:0] PCBranch;
    output[4:0] WriteRegE;

    wire ALUSrcAE, ALUSrcBE, RegDstE, SignExtendE, LinkE;
    wire[31:0] ExtendImmE, ALUOut;//SrcBE
    wire[31:0] SrcAE, SrcBE;
    //reg[31:0] SrcAE, SrcBE;
    wire[1:0] FA,FB;
    wire FA_1,FB_1;

    //模块的连接
    ALU alu(SrcAE, SrcBE, ALUcontrol, Zero, ALUOut);
    HazardUnit hu(CLK,RegWriteM,RegWriteW,Rt,Rs,WRiteRegM,WriteRegW,FA,FB);
    EXWire exwire(LinkE,PCPlus4,ALUOut,RD2,Rd,Rt,RegDstE,SignImm,ALUOutE,WriteData,WriteRegE,PCBranch);

    //控制信号的导出
    assign Controlout[3:0] = Controlin[7:4];
    assign ALUSrcAE = Controlin[3];
    assign ALUSrcBE = Controlin[2];
    assign RegDstE = Controlin[1];
    assign LinkE = Controlin[0];

    //进入alu的内容选择
    assign FA_1 = FA[1];
    assign FB_1 = FB[1];
    assign SrcAE = FA == 2'b00 ? (ALUSrcAE == 1'b1 ? Shamt : RD1) : (FA_1 == 1'b1 ? ALUOutM:ResultW);
    assign SrcBE = FB == 2'b00 ? (ALUSrcBE == 1'b1 ? SignImm : RD2) : (FB_1 == 1'b1 ? ALUOutM:ResultW);
/*
    always @ (posedge CLK) begin
        SrcAE <= FA == 2'b00 ? (ALUSrcAE == 1'b1 ? Shamt : RD1) : (FA_1 == 1'b1 ? ALUOutM:ResultW);
        SrcBE <= FB == 2'b00 ? (ALUSrcBE == 1'b1 ? SignImm : RD2) : (FB_1 == 1'b1 ? ALUOutM:ResultW);
    end
*/
endmodule