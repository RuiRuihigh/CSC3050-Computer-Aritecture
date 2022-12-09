module WB(CLK,Controlin,ALUOut,RD,WriteReg,RegWrite,Result);
    input CLK;
    inout[4:0] WriteReg;
    input[1:0] Controlin;
    input[31:0] ALUOut,RD;

    output RegWrite;
    output[31:0] Result;

    wire MemtoReg;

    WBWire wbwire(Controlin,RD,ALUOut,RegWrite,MemtoReg,Result);

endmodule