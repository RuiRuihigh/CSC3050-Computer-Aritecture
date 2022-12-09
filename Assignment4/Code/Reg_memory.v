module Registers(CLK,WE3,reg1,reg2,reg3,WriteData,ReadData1,ReadData2);
    input CLK,WE3;
    input [4:0] reg1,reg2,reg3;
    input [31:0] WriteData;
    output [31:0] ReadData1,ReadData2;
    reg[31:0] Regcontent[31:0];
    reg[31:0] rs, rt;
    integer i;
    assign ReadData1 = rs;
    assign ReadData2 = rt;
    initial begin
        for (i = 0; i <= 31; i = i + 1)
            begin
                Regcontent[i] = 32'b0;
            end
    end

    always @(negedge CLK) begin
        if (WE3 == 1)begin
                Regcontent[reg3] = WriteData;
                //$display(reg3,"---","%h",WriteData);
            end
        rs = Regcontent[reg1];
        rt = Regcontent[reg2];
    end
endmodule