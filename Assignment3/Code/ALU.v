module alu(instruction, regA, regB, result, flags);
input[31:0] instruction;
input[31:0] regA;
input[31:0] regB;
output reg[31:0] result;
output reg[2:0] flags;

// 0:regA  1:regB

reg[5:0] opcode;
reg[5:0] funcode;
reg[5:0] usereg;
reg[31:0] temp;
reg[31:0] rev;
always @(instruction,regA,regB)
begin
    opcode = instruction[31:26];
    funcode = instruction[5:0];
    usereg = instruction[25:21];
    if (opcode == 0 && funcode == 32)
        begin //add
        temp = regA + regB;
        result = temp;
        flags[2] = (result == 0);
        flags[1] = 0;
        flags[0] = (regA[31] & regB[31] & (~temp[31])) | ((~regA[31]) & (~regB[31]) & temp[31]);
        end
    else if (opcode == 8)    
        begin //addi
        if (usereg == 0)
        begin
        temp = $signed((instruction[15:0]));
        result = regA + temp;
        flags[2] = (result == 0);
        flags[1] = 0;
        flags[0] = (regA[31] & temp[31]& (~result[31])) | ((~regA[31]) & (~temp[31]) & result[31]);
        end
        else
        begin
        temp = $signed((instruction[15:0]));
        result = regB + temp;
        flags[2] = (result == 0);
        flags[1] = 0;
        flags[0] = (regB[31] & temp[31]& (~result[31])) | ((~regB[31]) & (~temp[31]) & result[31]);
        end
        end
    else if (opcode == 0 && funcode == 33)
        begin //addu
        temp = regA + regB;
        result = temp[31:0];
        flags[2] = (result == 0);
        flags[1] = 0;
        flags[0] = 0;
        end
    else if (opcode == 9)
        begin //addiu
        if (usereg == 0)
        begin
        temp = (instruction[15:0]);
        result = regA + temp;
        flags[2] = (result == 0);
        flags[1] = 0;
        flags[0] = 0;
        end
        else
        begin
        temp = (instruction[15:0]);
        result = regB + temp;
        flags[2] = (result == 0);
        flags[1] = 0;
        flags[0] = 0;
        end
        end
    else if (opcode == 0 && funcode == 34)
        begin //sub
        if (usereg == 1)
        begin
        rev = (~regA) + 1;
        temp = regB + rev;
        result = temp[31:0];
        flags[2] = (result == 0);
        flags[1] = 0;
        flags[0] = (rev[31] & regB[31]& (~temp[31])) | ((~rev[31]) & (~regB[31]) & temp[31]);
        end
        else
        begin
        rev = (~regB) + 1;
        temp = regA + rev;
        result = temp[31:0];
        flags[2] = (result == 0);
        flags[1] = 0;
        flags[0] = (rev[31] & regA[31]& (~temp[31])) | ((~rev[31]) & (~regA[31]) & temp[31]);
        end
        end
    else if (opcode == 0 && funcode == 35)
        begin //subu
        if (usereg == 1)
        begin
        rev = (~regA) + 1;
        temp = regB + rev;
        result = temp[31:0];
        flags[2] = (result == 0);
        flags[1] = 0;
        flags[0] = 0;
        end
        else
        begin
        rev= (~regB) + 1;
        temp = regA + rev;
        result = temp[31:0];
        flags[2] = (result == 0);
        flags[1] = 0;
        flags[0] = 0;
        end
        end
    else if (opcode == 0 && funcode == 36)
        begin //and
        temp = regA & regB;
        result = temp;
        flags[2] = 0;
        flags[1] = 0;
        flags[0] = 0;
        end
    else if (opcode == 12)
        begin //andi
        temp = $signed(instruction[15:0]);
        if (usereg == 0)
        begin
        result = regA & temp;
        flags = 3'b000;
        end
        else
        begin
        result = regB & temp;
        flags = 3'b000;
        end
        end
    else if (opcode == 0 && funcode == 39)
        begin //nor
        result = ~(regA | regB);
        flags = 3'b000;
        end
    else if (opcode == 0 && funcode == 37)
        begin //or
        result = (regA | regB);
        flags = 3'b000;
        end
    else if (opcode == 13)
        begin //ori
        temp = $signed(instruction[15:0]);
        if (usereg == 0)
        begin 
        result = (regA | temp);
        end
        else
        begin 
        result = (regB | temp);
        end
        flags = 3'b000;
        end
    else if (opcode == 0 && funcode == 38)
        begin //xor
        result = (regA ^ regB);
        flags = 3'b000;
        end
    else if (opcode == 14)
        begin //xori
        temp = $signed(instruction[15:0]);
        if (usereg == 0)
        begin
        result = regA ^temp;
        end
        else
        begin
        result = regB ^ temp;
        end
        flags = 3'b000;
        end
    else if (opcode == 4)
        begin //beq
        result = 0;
        flags[2] = (regA == regB);
        flags[1:0] = 0;
        end
    else if (opcode == 5)
        begin //bne
        result = 0;
        flags[2] = (regA != regB);
        flags[1:0] = 0;
        end
    else if (opcode == 0 && funcode == 42)
        begin //slt
        result = 0;
        flags[2] = 0;
        flags[0] = 0;
        if (usereg == 1)
        begin
        flags[1] = ($signed(regB) < $signed(regA));
        end
        else
        begin
        flags[1] = ($signed(regA) < $signed(regB));
        end
        end
    else if (opcode == 10)
        begin //slti
        result = 0;
        temp = $signed(instruction[15:0]) ;
        flags[2] = 0;
        flags[0] = 0;
        if (usereg == 1)
        begin
        flags[1] = ($signed(regA) < temp);
        end
        else
        begin
        flags[1] = ($signed(regB) < temp);
        end
        end
    else if (opcode == 0 && funcode == 43)
        begin //sltu
        result = 0;
        flags[2] = 0;
        flags[0] = 0;
        if (usereg == 1)
        begin
        flags[1] = (regB < regA);
        end
        else
        begin
        flags[1] = (regA < regB);
        end
        end
    else if (opcode == 11)
        begin //sltiu
        result = 0;
        temp = instruction[15:0];
        flags[2] = 0;
        flags[0] = 0;
        if (usereg == 1)
        begin
        flags[1] = ($signed(regA) < temp);
        end
        else
        begin
        flags[1] = ($signed(regB) < temp);
        end
        end
    else if (opcode == 35)
        begin //lw
        if (usereg == 1)
        begin
        temp = $signed(instruction[15:0]);
        result = regB + temp;
        end
        else
        begin
        temp = $signed(instruction[15:0]);
        result = regA + temp;
        end
        flags = 3'b000;
        end
    else if (opcode == 43)
        begin //sw
        if (usereg == 1)
        begin
        temp = $signed(instruction[15:0]);
        result = regB + temp;
        end
        else
        begin
        temp = $signed(instruction[15:0]);
        result = regA + temp;
        end
        flags = 3'b000;
        end
    else if (opcode == 0 && funcode == 0)
        begin //sll
        if (instruction[20:16] == 1)
        begin
        result = regB << instruction[10:6];
        flags = 3'b000;
        end
        else
        begin
        result = regA << instruction[10:6];
        flags = 3'b000;
        end
        end
    else if (opcode == 0 && funcode == 4)
        begin //sllv
        if (usereg== 1)
        begin
        result = regA << regB;
        flags = 3'b000;
        end
        else
        begin
        result = regB << regA;
        flags = 3'b000;
        end
        end
    else if (opcode == 0 && funcode == 3)
        begin //sra
        if (instruction[20:16] == 1)
        begin
        result = $signed(regB) >>> instruction[10:6];
        flags = 3'b000;
        end
        else
        begin
        result = $signed(regA) >>> instruction[10:6];
        flags = 3'b000;
        end
        end
    else if (opcode == 0 && funcode == 7)
        begin //srav
        if (usereg == 1)
        begin
        result = $signed(regA) >>> regB;
        flags = 3'b000;
        end
        else
        begin
        result = $signed(regB) >>> regA;
        flags = 3'b000;
        end
        end
    else if(opcode == 0 && funcode == 2)
        begin //srl
        if (instruction[20:16] == 1)
        begin
        result = regB >> instruction[10:6];
        flags = 3'b000;
        end
        else
        begin
        result = regA >> instruction[10:6];
        flags = 3'b000;
        end
        end  
    else if (opcode == 0 && funcode == 6)
        begin //srlv
        if (usereg == 1)
        begin
        result = regA >> regB;
        flags = 3'b000;
        end
        else
        begin
        result = regB >> regA;
        flags = 3'b000;
        end
        end
end
endmodule       




