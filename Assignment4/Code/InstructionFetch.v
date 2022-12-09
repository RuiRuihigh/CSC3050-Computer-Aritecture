module IF(CLK,reset,EN,PCSrc,Jump,PCBranch,JumpAddress,RD,PCPlus4);
    input CLK;
    input reset,EN;
    input PCSrc;
    input Jump;
    input[31:0] PCBranch;
    input[31:0] JumpAddress;
    output[31:0] RD, PCPlus4;

    reg[31:0] PCF;
    wire[31:0] FETCH_ADDRESS; 

    InstructionRAM IR(CLK, reset, EN,FETCH_ADDRESS,RD);
    IFWire ifwire(PCF,PCPlus4,FETCH_ADDRESS);

    initial
    begin
        PCF <= -32'b0100;
    end

    reg[31:0] PCF_mid;

    always@(posedge CLK)
    begin
        if (Jump==1'b1)begin
            PCF <= JumpAddress;
        end
        else begin
            if (PCSrc == 1'b1) begin
                PCF <= PCBranch;
            end
            else begin
                PCF <= PCPlus4;
            end
        end
    end
endmodule