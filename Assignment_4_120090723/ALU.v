//这个部分用controlunit得到的4位的控制码来调动alu执行特定的工作
module ALU (SrcRegA,SrcRegB,ALUcontrol,zero,result);
    input[31:0] SrcRegA, SrcRegB;
    input[3:0] ALUcontrol;
    output reg zero;
    output reg[31:0] result;


    always @(SrcRegA,SrcRegB,ALUcontrol)
        begin
            if (ALUcontrol == 4'b0000)// and
                begin
                    result = SrcRegA & SrcRegB;
                    zero = (result == 0);
                end
            else if (ALUcontrol == 4'b0001)// or
                begin
                    result = SrcRegA | SrcRegB;
                    zero = (result == 0);
                end
            else if (ALUcontrol == 4'b0010)// add
                begin
                    result = SrcRegA + SrcRegB;
                    zero = (result == 0);
                    //$display(result);
                end
            else if (ALUcontrol == 4'b0100)// sll 
                begin
                    result = SrcRegB << SrcRegA;
                    zero = (result == 0);
                end
            else if (ALUcontrol == 4'b0011)// srl 
                begin
                    result =  SrcRegB >> SrcRegA;
                    zero = (result == 0);
                end                
            else if (ALUcontrol == 4'b0101)// sra
                begin
                    result =  $signed(SrcRegB) >>> SrcRegA;
                    zero = (result == 0);
                end
            else if (ALUcontrol == 4'b0110)// sub
                begin
                    result = SrcRegA - SrcRegB;
                    zero = (result == 0);
                end
            else if (ALUcontrol == 4'b0111)// slt
                begin
                    result = $signed(SrcRegA) < $signed(SrcRegB) ? 1'b1 : 1'b0; 
                    zero = (result == 0);
                    //$display(result);
                end
            else if (ALUcontrol == 4'b1011)// beq 
                begin
                    result = 0;
                    zero = (SrcRegA == SrcRegB ? 1'b1 : 1'b0);
                    //$display(zero);
                end
            else if (ALUcontrol == 4'b1010)// bne 
                begin
                    result = 0;
                    zero = (SrcRegA == SrcRegB ? 1'b0 : 1'b1);
                    //$display("happen");
                end
            else if (ALUcontrol == 4'b1101)// nor 
                begin
                    result = (~SrcRegA) & (~SrcRegB) ;
                    zero = (result == 0);
                end
            else if (ALUcontrol == 4'b1100)// xor 
                begin
                    result = SrcRegA ^ SrcRegB;
                    zero = (result == 0);
                end
        end
endmodule