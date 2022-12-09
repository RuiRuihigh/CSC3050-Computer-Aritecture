module ControlUnit(CLK,Op,Funct,Control,ALUcontrol);
//利用一个instruction中的op和funct来决定执行的control，jumpcontrol和alucontrol。
    input CLK;
    input[5:0] Op,Funct;
    output wire[10:0] Control;
    /*7:RegWrite  
    6:MemtoReg
    5:MemWrite
    4:Branch
    3:ALUSrcA
    2:ALUSrcB
    1:RegDst
    0:SignExtention
    */
    /*
    2 : Jump, 
    1 : JumpReg,                      
    0 : JumpLink 
    */
    output reg[3:0] ALUcontrol;
    reg[7:0] control;
    reg[2:0] jumpcontrol;

    assign Control = {control[7:0],jumpcontrol[2:0]};
    initial 
    begin
        control <=8'b0;
        jumpcontrol <= 3'b0;
        ALUcontrol <= 4'b0;
    end
    always @(negedge CLK)
    begin
        if (Op == 6'b000000 & Funct == 6'b1000_00) //add
        begin
            ALUcontrol <= 4'b0010;
            control <= 8'b1000_0010;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b000000 & Funct == 6'b1000_01) //addu
        begin
            ALUcontrol <= 4'b0010;
            control <= 8'b1000_0010;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b000000 & Funct == 6'b1000_10) //sub
        begin
            ALUcontrol <= 4'b0110;
            control <= 8'b1000_0010;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b000000 & Funct == 6'b1000_11) //subu
        begin
            ALUcontrol <= 4'b0110;
            control <= 8'b1000_0010;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b000000 & Funct == 6'b1001_00) //and
        begin
            ALUcontrol <= 4'b0000;
            control <= 8'b1000_0010;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b000000 & Funct == 6'b1001_01) //or
        begin
            ALUcontrol <= 4'b0001;
            control <= 8'b1000_0010;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b000000 & Funct == 6'b1001_10) //xor
        begin
            ALUcontrol <= 4'b1100;
            control <= 8'b1000_0010;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b000000 & Funct == 6'b1001_11) //nor
        begin
            ALUcontrol <= 4'b1101;
            control <= 8'b1000_0010;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b000000 & Funct == 6'b0000_00) //sll
        begin
            ALUcontrol <= 4'b0100;
            control <= 8'b100_0101_0;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b000000 & Funct == 6'b0000_10) //srl
        begin
            ALUcontrol <= 4'b0011;
            control <= 8'b100_0101_0;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b000000 & Funct == 6'b0000_11) //sra
        begin
            ALUcontrol <= 4'b0101;
            control <= 8'b100_0101_0;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b000000 & Funct == 6'b0001_00) //sllv
        begin
            ALUcontrol <= 4'b0100;
            control <= 8'b100_0001_0;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b000000 & Funct == 6'b0001_10) //srlv
        begin
            ALUcontrol <= 4'b0011;
            control <= 8'b100_0001_0;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b000000 & Funct == 6'b0001_11) //srav
        begin
            ALUcontrol <= 4'b0101;
            control <= 8'b100_0001_0;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b000000 & Funct == 6'b0010_00) //jr
        begin
            ALUcontrol <= 4'b0101;
            control <= 8'b000_0000_0;
            jumpcontrol <= 3'b110;
        end
        else if (Op == 6'b000000 & Funct == 6'b1010_10) //slt
        begin
            ALUcontrol <= 4'b0111;
            control <= 8'b100_0001_0;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b0000_10)//j
        begin
            ALUcontrol <= 4'b0000;
            control <= 8'b000_0000_0;
            jumpcontrol <= 3'b100;
        end
        else if (Op == 6'b0000_11)//jal
        begin
            ALUcontrol <= 4'b0000;
            control <= 8'b100_0000_0;
            jumpcontrol <= 3'b101;
        end
        else if (Op == 6'b0001_00)//beq
        begin
            ALUcontrol <= 4'b1011;
            control <= 8'b000_1000_1;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b0001_01)//bne
        begin
            ALUcontrol <= 4'b1010;
            control <= 8'b000_1000_1;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b0010_00)//addi
        begin
            ALUcontrol <= 4'b0010;
            control <= 8'b100_0010_1;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b0010_01)//addiu
        begin
            ALUcontrol <= 4'b0010;
            control <= 8'b100_0010_1;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b0011_00)//andi
        begin
            ALUcontrol <= 4'b0000;
            control <= 8'b100_0010_0;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b0011_01)//ori
        begin
            ALUcontrol <= 4'b0001;
            control <= 8'b100_0010_0;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b0011_10)//xori
        begin
            ALUcontrol <= 4'b1100;
            control <= 8'b100_0010_0;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b1000_11)//lw
        begin
            //11000101
            //$display("lw");
            ALUcontrol <= 4'b0010;
            control <= 8'b110_0010_1;
            jumpcontrol <= 3'b000;
        end
        else if (Op == 6'b1010_11)//sw
        begin
            //$display("sw");
            ALUcontrol <= 4'b0010;
            control <= 8'b001_0010_1;
            jumpcontrol <= 3'b000;
        end
    end



endmodule