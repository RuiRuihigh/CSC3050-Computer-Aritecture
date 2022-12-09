module ID(CLK, RegWrite,Instr, Result, WriteReg,
Controlout, Jump,ALUcontrol,
RD1, RD2,SignImmD, JumpAddress,
Rs,Rt, Rd, Shamt,PCPlus4);
    input CLK, RegWrite;
    input[31:0] Instr, Result;
    input[4:0] WriteReg;
    output[7:0] Controlout;
    /*     7 : RegWrite, 6: MemtoReg, 5 : MemWrite, 
         4 : Branch,   3 : ALUSrcA,       2 : ALUSrcB,  
         1 : RegDst,     0 : JumpLink        
         Jump/JumpAddress/SignExtention 已经在这个阶段使用，不用传到下一个阶段
    */
    output Jump;
    output[3:0] ALUcontrol;
    output[31:0] RD1, RD2, SignImmD;
    output [31:0] JumpAddress;
    output[4:0] Rs,Rt, Rd, Shamt;//Shamt 32bit
    inout[31:0] PCPlus4;

    wire[31:0] SignImm, UnsignImm;
    wire[25:0] part_jump;
    wire[4:0] rs, rt, rd, shamt;
    wire[10:0] Control;
    wire SignExtend;
    wire JumpSrc;

    wire[5:0] opcopde;
    wire[5:0] functioncode;
    wire[4:0] Rtmid;
    wire[31:0] JumpAddressmid;
    wire[31:0] f_ja,p_ja;

    Registers regs(CLK, RegWrite, rs, rt, WriteReg, Result, RD1, RD2);
    ControlUnit conunit(CLK, opcopde, functioncode, Control, ALUcontrol);
    IDWire idwire(Instr,opcopde,functioncode,rs,rt,rd,shamt,SignImm,UnsignImm,part_jump);

    //控制信号导出
    assign Controlout[7:1] = Control[10:4];
    assign Controlout[0] = Control[0];
    assign SignExtention = Control[3];
    assign Jump = Control[2];
    assign JumpSrc = Control[1];

    //导出的寄存器值
    assign Rt = Rtmid; 
    assign Rtmid = Control[0] == 1'b1 ? 5'b11111 : rt; 
    assign Rd = rd;
    assign Rs = rs;

    //jump的决定
    assign Shamt = {27'h0000000, shamt[4:0]};
    assign JumpAddress = JumpAddressmid;
    assign JumpAddressmid = JumpSrc == 1'b1 ? f_ja : p_ja;
    assign f_ja = RD1;
    assign p_ja = {PCPlus4[31:28], part_jump[25:0], 2'b00};


    assign SignImmD = SignExtention == 1'b1 ? SignImm : UnsignImm;

    
endmodule