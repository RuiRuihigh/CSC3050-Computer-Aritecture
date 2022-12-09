`timescale 100fs/100fs
//将五个stages连接在一起的topmodule。
module CPU(CLK,reset,EN);
/*
    initial
    begin            
        $dumpfile("wave.vcd");        //生成的vcd文件名称
        $dumpvars(0, CPU);    //tb模块名称
    end
*/
    input CLK;
    input reset,EN;
    //IF
    wire PCSrcM;
    wire JumpD;
    wire[31:0] InstrF,JumpAddressD, PCPlus4F, PCBranchM;
    IF InF(CLK,reset,EN, PCSrcM,JumpD, PCBranchM, JumpAddressD, InstrF, PCPlus4F);

    //IF/ID
    wire[31:0] InstrFD, PCPlus4FD;
    IFID ifid(CLK,JumpD,PCSrcM,InstrF,PCPlus4F,InstrFD,PCPlus4FD);
    assign InstrD = InstrFD;
    assign PCPlus4D = PCPlus4FD;


    //ID  
    wire[7:0] ControlDout;
    wire[4:0] RsD,RtD, RdD, ShamtD,WriteRegW;
    wire[31:0] ResultW, SignImmD,InstrD,PCPlus4D,RD1D, RD2D;   
    wire[3:0] ALUcontrolD;
    wire RegWriteW;
    ID InD(CLK, RegWriteW, InstrD, ResultW, WriteRegW, ControlDout, JumpD, ALUcontrolD, RD1D, RD2D,  SignImmD,JumpAddressD, RsD,RtD, RdD, ShamtD,PCPlus4D);

    //ID/EX
    wire[7:0] ControlDE;
    wire[3:0] ALUcontrolDE;
    wire[31:0] RD1DE, RD2DE, ShamtDE, PCPlus4DE,SignImmDE;
    wire[4:0] RsDE,RtDE, RdDE;
    IDEX idex(CLK,JumpD,PCSrcM,ControlDout,ALUcontrolD,RD1D,RD2D,ShamtD,SignImmD,PCPlus4D,RsD,RtD,RdD,ControlDE,ALUcontrolDE,RD1DE,RD2DE,ShamtDE,SignImmDE,PCPlus4DE,RsDE,RtDE,RdDE);
    assign ControlEin = ControlDE;
    assign ALUcontrolE = ALUcontrolDE;
    assign RD1E = RD1DE;
    assign RD2E = RD2DE;
    assign RsE = RsDE;
    assign RtE = RtDE;
    assign RdE = RdDE;
    assign ShamtE = ShamtDE;
    assign SignImmE = SignImmDE;
    assign PCPlus4E = PCPlus4DE;


    //EX
    wire[7:0] ControlEin;
    wire[4:0] RsE,RtE, RdE, ShamtE, WriteRegE;
    wire[31:0] PCPlus4E,ALUOutE,RD1E, RD2E,SignImmE, WriteDataE, PCBranchE;
    wire[3:0] ControlEout,ALUcontrolE;
    wire ZeroE;
    wire[4:0] WRiteRegM;
    EX ex(CLK,ControlEin, ALUcontrolE, RD1E, RD2E, RsE,RtE, RdE, ShamtE, SignImmE, PCPlus4E, ZeroE, ALUOutE, WriteDataE, PCBranchE, ControlEout, WriteRegE,
    RegWriteM,RegWriteW,WRiteRegM,WriteRegW,ALUOutM,ResultW);

    //EX/MEM
    wire[3:0] ControlEM;
    wire ZeroEM;
    wire[31:0] ALUOutEM, WriteDataEM, PCBranchEM;
    wire[4:0] WriteRegEM;
    EXMEM exem(CLK,JumpD,PCSrcM,ControlEout,ZeroE,ALUOutE,WriteDataE,PCBranchE,WriteRegE,ControlEM,ZeroEM,ALUOutEM,WriteDataEM,PCBranchEM,WriteRegEM);
    assign ControlMin = ControlEM;
    assign ZeroM = ZeroEM;
    assign WriteDataM = WriteDataEM;
    assign PCBranchM = PCBranchEM;
    assign ALUOutM = ALUOutEM;
    assign WriteRegM = WriteRegEM;


    //MEM
    wire[4:0] WriteRegM;
    wire[3:0] ControlMin;
    wire[31:0] WriteDataM,ReadDataM,ALUOutM;
    wire[1:0] ControlMout;
    wire ZeroM;
    wire RegWriteM;
    MEM mem(CLK,reset,EN, ControlMin, ZeroM, ALUOutM, PCBranchM, WriteDataM, WriteRegM, ControlMout, PCSrcM, ReadDataM,RegWriteM);

    //MEM/WB
    wire[1:0] ControlMW;
    wire[31:0] ALUOutMW, ReadDataMW;
    wire[4:0] WriteRegMW;
    MEMWB memwb(CLK,JumpD,PCSrcM,ControlMout,ALUOutM,ReadDataM,WriteRegM,ControlMW,ALUOutMW,ReadDataMW,WriteRegMW);
    assign ReadDataW = ReadDataMW;
    assign WriteRegW = WriteRegMW;
    assign ControlWin = ControlMW;
    assign ALUOutW = ALUOutMW;

    //WB
    wire[31:0] ALUOutW, ReadDataW;
    wire[1:0] ControlWin;
    WB wb(CLK,ControlWin, ALUOutW, ReadDataW, WriteRegW, RegWriteW, ResultW);
endmodule