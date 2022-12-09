module MEM(CLK, reset,En,Controlin,Zero,ALUOut,PCBranch,WriteData,
WriteReg,Controlout,PCSrc,RD,RegWriteM);
    input CLK,Zero;
    input reset,En;
    input[3:0] Controlin;

    inout[31:0] ALUOut,PCBranch;
    inout[4:0] WriteReg;

    input[31:0] WriteData;
    output PCSrc;
    output[1:0] Controlout;
    output[31:0] RD;
    output RegWriteM;

    wire[64:0] serial;
    wire[31:0] FETCH_ADDRESS;
    wire MemWrite,Branch;

    MainMemory datamem(CLK,reset,En,FETCH_ADDRESS,serial,RD);
    MEMWire memwire(Controlin,ALUOut,MemWrite,Branch,RegWriteM,Controlout,FETCH_ADDRESS);

    assign serial = {MemWrite,FETCH_ADDRESS,WriteData};
    assign PCSrc = Branch & Zero;


endmodule