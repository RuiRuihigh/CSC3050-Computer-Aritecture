module IFID(CLK,JumpD,PCSrcM,
InstrF,PCPlus4F,
InstrFD,PCPlus4FD);
    input CLK,JumpD,PCSrcM;
    input[31:0] InstrF,PCPlus4F;
    output reg[31:0] InstrFD,PCPlus4FD;

    initial begin
        InstrFD <= 32'b0;
        PCPlus4FD <= 32'b0;
    end
    

    always @(posedge CLK) begin
    if (JumpD === 1'b1) begin
        InstrFD <= 32'b0;
        PCPlus4FD <= 32'b0;
    end
    else if (PCSrcM === 1'b1) begin
        //$display("right");
        InstrFD <= 32'b0;
        PCPlus4FD <= 32'b0;
    end
    else begin
        InstrFD <= InstrF;
        PCPlus4FD <= PCPlus4F;
    end
    end


endmodule


module IDEX(CLK,JumpD,PCSrcM,
ControlDout,ALUcontrolD,RD1D,RD2D,ShamtD,SignImmD,PCPlus4D,RsD,RtD,RdD,
ControlDE,ALUcontrolDE,RD1DE,RD2DE,ShamtDE,SignImmDE,PCPlus4DE,RsDE,RtDE,RdDE);
    input CLK,JumpD,PCSrcM;
    input[7:0] ControlDout;
    input[3:0] ALUcontrolD;
    input[31:0] RD1D,RD2D,ShamtD,SignImmD,PCPlus4D;
    input[4:0] RsD,RtD,RdD;
    output reg[7:0] ControlDE;
    output reg[3:0] ALUcontrolDE;
    output reg[31:0] RD1DE, RD2DE, ShamtDE, PCPlus4DE,SignImmDE;
    output reg[4:0] RsDE,RtDE, RdDE;

    initial begin
        RsDE <= 5'b0;
        RtDE <= 5'b0;
        RdDE <= 5'b0;
        PCPlus4DE <= 32'b0;
        RD1DE <= 32'b0;
        RD2DE <= 32'b0;
        ShamtDE <= 32'b0;
        SignImmDE <= 32'b0;
        ControlDE <= 7'b0;
        ALUcontrolDE <= 4'b0;
    end

    always @(posedge CLK) begin
        if (PCSrcM === 1'b1) begin
            //$display("right");
            ShamtDE <= 32'b0;
            SignImmDE <= 32'b0;
            PCPlus4DE <= 32'b0;
            RsDE <= 5'b0;
            RtDE <= 5'b0;
            RdDE <= 5'b0;
            ControlDE <= 7'b0;
            ALUcontrolDE <= 4'b0;
            RD1DE <= 32'b0;
            RD2DE <= 32'b0;
            //$display(PCPlus4DE);

        end
        else begin
        
        SignImmDE <= SignImmD;
        RsDE <= RsD;
        RtDE <= RtD;
        RdDE <= RdD;
        PCPlus4DE <= PCPlus4D;
        ControlDE <= ControlDout;
        ALUcontrolDE <= ALUcontrolD;
        RD1DE <= RD1D;
        RD2DE <= RD2D;
        ShamtDE <= ShamtD;
        end
    end


endmodule

module EXMEM(CLK,JumpD,PCSrcM,
ControlEout,ZeroE,ALUOutE,WriteDataE,PCBranchE,WriteRegE,
ControlEM,ZeroEM,ALUOutEM,WriteDataEM,PCBranchEM,WriteRegEM);
    input CLK,JumpD,PCSrcM;
    input[31:0] ALUOutE,WriteDataE,PCBranchE;
    input [3:0] ControlEout;
    input ZeroE;
    input[4:0] WriteRegE;
    output reg[3:0] ControlEM;
    output reg ZeroEM;
    output reg[31:0] ALUOutEM, WriteDataEM, PCBranchEM;
    output reg[4:0] WriteRegEM;

    initial begin
        WriteDataEM <= 32'b0;
        PCBranchEM <= 32'b0;
        WriteRegEM <= 5'b0;
        ControlEM <= 4'b0;
        ZeroEM <= 1'b0;
        ALUOutEM <= 32'b0;

    end
    always @(posedge CLK) begin
        if (PCSrcM === 1'b1) begin
            //$display("right");
            WriteDataEM <= 32'b0;
            PCBranchEM <= 32'b0;
            WriteRegEM <= 5'b0;
            ControlEM <= 4'b0;
            ZeroEM <= 1'b0;
            ALUOutEM <= 32'b0;
        end
        else begin
        ControlEM <= ControlEout;
        ZeroEM <= ZeroE;
        WriteDataEM <= WriteDataE;
        PCBranchEM <= PCBranchE;
        WriteRegEM <= WriteRegE;
        ALUOutEM <= ALUOutE;
        end
    end

endmodule


module MEMWB(CLK,JumpD,PCSrcM,
ControlMout,ALUOutM,ReadDataM,WriteRegM,
ControlMW,ALUOutMW,ReadDataMW,WriteRegMW);

    input CLK,JumpD,PCSrcM;
    input[1:0] ControlMout;
    input[31:0] ALUOutM,ReadDataM;
    input[4:0] WriteRegM;
    output reg[1:0] ControlMW;
    output reg[31:0] ALUOutMW, ReadDataMW;
    output reg[4:0] WriteRegMW;

    initial begin
        ControlMW <= 2'b0;
        ALUOutMW <= 32'b0;
        ReadDataMW <= 32'b0;
        WriteRegMW <= 5'b0;
    end
    always @(posedge CLK) begin
        ControlMW <= ControlMout;
        ALUOutMW <= ALUOutM;
        ReadDataMW <= ReadDataM;
        WriteRegMW <= WriteRegM;
        //$display("-----");
        //$display("%h",ReadDataMW);
        //$display("------");
    end           
endmodule
/*
    always@(posedge CLK) begin
        $display("-----");
        $display("%h",RD);
        $display(WriteReg);
        $display("%h",Result);
        $display("------");
    end
    */