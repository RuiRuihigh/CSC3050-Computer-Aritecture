//`include "alu.v"
module  testbench();
reg[31:0] a,b,i;          
wire [31:0] r;
wire [2:0] f;
alu test(i,a,b,r,f);
initial begin
   i = 32'h00000020; // addtest 
   a = 32'h00000001; b = 32'h00000010; #10;
   if (r !== 32'h00000011 | f !== 3'b000) $display("add test failed."); else $display("add test succeeded"); 
   a = 32'h80000000; b = 32'h80000001; #10;
   if (r !== 32'h00000001 | f !== 3'b001) $display("add(n-overflow) test failed."); else $display("add(n-overflow) test succeeded"); 
   a = 32'h40000000; b = 32'h40000000; #10;
   if (r !== 32'h80000000 | f !== 3'b001) $display("add(p-overflow) test failed."); else $display("add(p-overflow) test succeeded");
   a = 32'h00000000; b = 32'h00000000; #10;
   if (r !== 32'h00000000 | f !== 3'b100) $display("add(zero test test failed)"); else $display("add(zero test) test succeeded");
   a = 32'h80000000; b = 32'h80000000; #10;
   if (r !== 32'h00000000 | f !== 3'b101) $display("add(zero&overflow test failed)"); else $display("add(zero&overflow test) test succeeded");
   $display("----------add-test-over----------");
   
   // addi test
   i = 32'b001000_00000_00001_0000000000000010; 
   a = 32'h00000002; b = 32'h00000000; #10;
   if (r !== 32'h00000004 | f != 3'b000) $display("addi test failed."); else $display("addi test succeeded");
   i = 32'b001000_00000_00001_1111111111111111; 
   a = 32'h00000002; b = 32'h00000000; #10;
   if (r !== 32'h00000001 | f != 3'b000) $display("addi(negative) test failed."); else $display("addi(negative) test succeeded");
   i = 32'b001000_00000_00001_0000000000000010; 
   a = 32'h7fff_ffff; b = 32'h00000000; #10;
   if (r !== 32'h80000001 | f != 3'b001) $display("addi(overflow) test failed."); else $display("addi(overflow) test succeeded");
   i = 32'b001000_00001_00000_0000000000000010; 
   b = 32'h00000002; a = 32'h00000000; #10;
   if (r !== 32'h00000004 | f != 3'b000) $display("addi(reverse order) test failed."); else $display("addi reverse order test succeeded");
   i = 32'b001000_00001_00000_1111111111111111; 
   b = 32'h00000002; a = 32'h00000000; #10;
   if (r !== 32'h00000001 | f != 3'b000) $display("addi(r-negative) test failed."); else $display("addi(r-negative) test succeeded");
   i = 32'b001000_00001_00000_0000000000000010; 
   b = 32'h7fff_ffff; a = 32'h00000000; #10;
   if (r !== 32'h80000001 | f != 3'b001) $display("addi(r-overflow) test failed."); else $display("addi(r-overflow) test succeeded");
   i = 32'b001000_00001_00000_0000000000000000; 
   b = 32'h0000_0000; a = 32'h00000000; #10;
   if (r !== 32'h00000000 | f != 3'b100) $display("addi(zero) test failed."); else $display("addi(zero) test succeeded");
   $display("----------addi-test-over----------");
   
   i = 32'h00000021; //addutest
   a = 32'h00000011; b = 32'h00000100; #10;
   if (r !== 32'h00000111 | f !== 3'b000) $display("addu test failed."); else $display("addu test succeeded");
   a = 32'h80000000; b = 32'h80000001; #10;
   if (r !== 32'h00000001 | f !== 3'b000) $display("addu(overflow) test failed."); else $display("addu(overflow) test succeeded"); 
   a = 32'h00000000; b = 32'h00000000; #10;
   if (r !== 32'h00000000 | f !== 3'b100) $display("addu(zero test test failed)"); else $display("addu(zero test) test succeeded");
   a = 32'h80000000; b = 32'h80000000; #10;
   if (r !== 32'h00000000 | f !== 3'b100) $display("addu(zero&overflow test failed)"); else $display("addu(zero&overflow test) test succeeded");
   $display("----------addu-test-over----------");

   //addiu test
   i = 32'b001001_00000_00001_0000000000000010; 
   a = 32'h00000002; b = 32'h00000000; #10;
   if (r !== 32'h00000004 | f != 3'b000) $display("addiu test failed."); else $display("addiu test succeeded");
   i = 32'b001000_00000_00001_0111111111111111; 
   a = 32'h00000001; b = 32'h00000000; #10;
   if (r !== 32'h00008000 | f != 3'b000) $display("addiu(negative) test failed."); else $display("addiu(negative) test succeeded");
   i = 32'b001001_00000_00001_0000000000000010; 
   a = 32'h7fff_ffff; b = 32'h00000000; #10;
   if (r !== 32'h80000001 | f != 3'b000) $display("addiu(overflow) test failed."); else $display("addiu(overflow) test succeeded");
   i = 32'b001001_00001_00000_0000000000000010; 
   b = 32'h00000002; a = 32'h00000000; #10;
   if (r !== 32'h00000004 | f != 3'b000) $display("addiu(reverse order) test failed."); else $display("addiu reverse order test succeeded");
   i = 32'b001001_00001_00000_0000000000000000; 
   b = 32'h0000_0000; a = 32'h00000000; #10;
   if (r !== 32'h00000000 | f != 3'b100) $display("addiu(zero) test failed."); else $display("addiu(zero) test succeeded");
   $display("----------addiu-test-over----------");

   i = 32'b000000_00000_00001_00000_00000_100010;
   a = 32'h0000000f; b = 32'h00000001; #10;
   if (r !== 32'h0000000e | f !== 3'b000) $display("sub test failed"); else $display("sub test succeeded");
   a = 32'h80000000; b = 32'h0000001; #10;
   if (r !== 32'h7fff_ffff | f !== 3'b001) $display("sub(overflow) test failed"); else $display("sub(overflow) test succeeded");
   i = 32'b000000_00001_00000_00000_00000_100010;
   a = 32'h00000001; b = 32'h0000000f; #10;
   if (r !== 32'h0000000e | f !== 3'b000) $display("sub(reverse reg order) test failed"); else $display("sub(reverse reg order) test succeeded");
   i = 32'b000000_00001_00000_00000_00000_100010;
   a = 32'hffff_ffff; b = 32'hffff_ffff; #10;
   if (r !== 32'h00000000 | f !== 3'b100) $display("sub(zero) test failed"); else $display("sub(zero) test succeeded");
   $display("----------sub-test-over----------");

   i = 32'b000000_00000_00001_00000_00000_100011;
   a = 32'h0000000f; b = 32'h00000001; #10;
   if (r !== 32'h0000000e | f !== 3'b000) $display("subu test failed"); else $display("subu test succeeded");
   a = 32'h80000000; b = 32'h0000001; #10;
   if (r !== 32'h7fff_ffff | f !== 3'b000) $display("subu(overflow) test failed"); else $display("subu(overflow) test succeeded");
   i = 32'b000000_00001_00000_00000_00000_100011;
   a = 32'h00000001; b = 32'h0000000f; #10;
   if (r !== 32'h0000000e | f !== 3'b000) $display("subu(reverse reg order) test failed"); else $display("subu(reverse reg order) test succeeded");
   i = 32'b000000_00001_00000_00000_00000_100011;
   a = 32'hffff_ffff; b = 32'hffff_ffff; #10;
   if (r !== 32'h00000000 | f !== 3'b100) $display("subu(zero) test failed"); else $display("subu(zero) test succeeded");
   $display("----------subu-test-over----------");

   i = 32'b000000_00000_00001_00000_00000_100100;
   a = 32'h00000000; b = 32'h0000000f; #10;
   if (r !== 32'h00000000 | f !== 3'b000) $display("and1 test failed"); else $display("and1 test succeeded");
   a = 32'h0000000e; b = 32'h00000007; #10;
   if (r !== 32'h00000006 | f !== 3'b000) $display("and2 test failed"); else $display("and2 test succeeded");
   i = 32'b000000_00000_00001_00000_00000_100101;
   a = 32'h00000000; b = 32'h0000000f; #10;
   if (r !== 32'h0000000f | f !== 3'b000) $display("or1 test failed"); else $display("or1 test succeeded");
   a = 32'h0000000e; b = 32'h00000007; #10;
   if (r !== 32'h0000000f | f !== 3'b000) $display("or2 test failed"); else $display("or2 test succeeded");
   i = 32'b000000_00000_00001_00000_00000_100110;
   a = 32'h00000000; b = 32'h0000000f; #10;   
   if (r !== 32'h0000000f | f !== 3'b000) $display("xor1 test failed"); else $display("xor1 test succeeded");
   a = 32'h0000000e; b = 32'h00000007; #10;
   if (r !== 32'h00000009 | f !== 3'b000) $display("xor2 test failed"); else $display("xor2 test succeeded");
   i = 32'b000000_00000_00001_00000_00000_100111;
   a = 32'h00000000; b = 32'h0000000f; #10;   
   if (r !== 32'hffff_fff0 | f !== 3'b000) $display("nor1 test failed"); else $display("nor1 test succeeded");
   a = 32'h0000000e; b = 32'h00000007; #10;
   if (r !== 32'hffff_fff0 | f !==3'b000) $display("nor2 test failed"); else $display("nor2 test succeeded");
   $display("-------and,or,xor,nor test over--------");

   i = 32'b001100_00000_00001_0000000000001111;
   a = 32'h00000000; b = 32'h0000000f; #10;
   if (r !== 32'h00000000 | f !== 3'b000) $display("andi1 test failed"); else $display("andi1 test succeeded");
   i = 32'b001100_00000_00001_1111111111111111;
   a = 32'h0000ffff; b = 32'h0000000f; #10;
   if (r !== 32'h0000ffff | f !== 3'b000) $display("andi2 test failed"); else $display("andi2 test succeeded");
   i = 32'b001100_00001_00000_0000000000001111;
   b = 32'h00000000; a = 32'h0000000f; #10;
   if (r !== 32'h00000000 | f !== 3'b000) $display("andi3 test failed"); else $display("andi3 test succeeded");
   i = 32'b001100_00001_00000_1111111111111111;
   b = 32'h0000ffff; a = 32'h0000000f; #10;
   if (r !== 32'h0000ffff | f !== 3'b000) $display("andi3 test failed"); else $display("andi3 test succeeded");

   i = 32'b001101_00000_00001_0000000000001111;
   a = 32'h00000000; b = 32'h000000ff; #10;
   if (r !== 32'h0000000f | f !== 3'b000) $display("ori1 test failed"); else $display("ori1 test succeeded");
   i = 32'b001101_00000_00001_1111111111111111;
   a = 32'h0000ffff; b = 32'h0000000f; #10;
   if (r !== 32'hffffffff | f !== 3'b000) $display("ori2 test failed"); else $display("ori2 test succeeded");
   i = 32'b001101_00001_00000_0000000000001111;
   b = 32'h00000000; a = 32'h000000ff; #10;
   if (r !== 32'h0000000f | f !== 3'b000) $display("ori3 test failed"); else $display("ori3 test succeeded");
   i = 32'b001101_00001_00000_1111111111111111;
   b = 32'h0000ffff; a = 32'h0000000f; #10;
   if (r !== 32'hffff_ffff | f !== 3'b000) $display("ori4 test failed"); else $display("ori4 test succeeded");

   i = 32'b001110_00000_00001_0000000000001111;
   a = 32'h00000000; b = 32'h000000ff; #10;
   if (r !== 32'h0000000f | f !== 3'b000) $display("xori1 test failed"); else $display("xori1 test succeeded");
   i = 32'b001110_00000_00001_1111111111111111;
   a = 32'h0000ffff; b = 32'h0000000f; #10;
   if (r !== 32'hffff0000 | f !== 3'b000) $display("xori2 test failed"); else $display("xori2 test succeeded");
   i = 32'b001110_00001_00000_0000000000001111;
   b = 32'h00000000; a = 32'h000000ff; #10;
   if (r !== 32'h0000000f | f !== 3'b000) $display("xori3 test failed"); else $display("xori3 test succeeded");
   i = 32'b001110_00001_00000_1111111111111111;
   b = 32'h0000ffff; a = 32'h0000000f; #10;
   if (r !== 32'hffff_0000 | f !== 3'b000) $display("xori4 test failed"); else $display("xori4 test succeeded");
   $display("-------andi,ori,xori,nori test over--------");

   i = 32'b000100_00000_00001_0000111100001111;
   a = 32'h0000ffff; b = 32'h0000000f; #10;
   if (f[2] !== 0) $display("beq (not equal) test failed"); else $display("beq (not equal) test succeeded");
   a = 32'h0000ffff; b = 32'h0000ffff; #10;
   if (f[2] !== 1) $display("beq (equal) test failed"); else $display("beq (equal) test succeeded");
   i = 32'b000101_00000_00001_0000111100001111;
   a = 32'h0000ffff; b = 32'h0000000f; #10;
   if (f[2] !== 1) $display("bne (not equal) test failed"); else $display("bne (not equal) test succeeded");
   a = 32'h0000ffff; b = 32'h0000ffff; #10;
   if (f[2] !== 0) $display("bne (equal) test failed"); else $display("bne (equal) test succeeded");
   $display("-----------bne, beq test over-----------");

   i = 32'b000000_00000_00001_00000_00000_101010;
   a = 32'h0000000f; b = 32'h0000_0001; #10;
   if (f[1] !== 0) $display("slt test failed"); else $display("slt test succeeded");
   i = 32'b000000_00001_00000_00000_00000_101010;
   a = 32'h0000000f; b = 32'h0000001; #10;
   if (f[1] !== 1) $display("slt(reverse order) test failed"); else $display("slt(reverse order) test succeeded");
   a = 32'h00000001; b = 32'h0000001; #10;
   if (f[1] !== 0) $display("slt(equal) test failed"); else $display("slt(equal) test succeeded");
   a = 32'h00000001; b = 32'hf0000001; #10;
   if (f[1] !== 1) $display("slt(negative) test failed"); else $display("slt(negative) test succeeded");
   $display("-------------slt test over-------------");

   i = 32'b001010_00000_00001_0000111100001111;
   a = 32'h00000001; b = 32'h0fff_ffff; #10;
   if (f[1] == 1)$display("slti test failed"); else $display("slti test succeeded");
   i = 32'b001010_00001_00000_0000111100001111; #10;
   if (f[1] == 0)$display("slti(reversed) test failed"); else $display("slti(reversed) test succeeded");
   i = 32'b001010_00000_00001_1000111100001111;
   a = 32'h00000001; b = 32'h0fff_ffff; #10;
   if (f[1] == 0)$display("slti(negative) test failed"); else $display("slti(negative) test succeeded");
   $display("-------------slti test over-------------");

   i = 32'b000000_00000_00001_00000_00000_101011;
   a = 32'h0000000f; b = 32'h0000001; #10;
   if (f[1] !== 0) $display("sltu test failed"); else $display("sltu test succeeded");
   i = 32'b000000_00001_00000_00000_00000_101011;
   a = 32'h0000000f; b = 32'h0000001; #10;
   if (f[1] !== 1) $display("sltu(reverse order) test failed"); else $display("sltu(reverse order) test succeeded");
   a = 32'h00000001; b = 32'h0000001; #10;
   if (f[1] !== 0) $display("sltu(equal) test failed"); else $display("sltu(equal) test succeeded");
   a = 32'h00000001; b = 32'hf0000001; #10;
   if (f[1] !== 0) $display("sltu(negative) test failed"); else $display("sltu(negative) test succeeded");
   $display("-------------sltu test over-------------");

   i = 32'b001011_00000_00001_0000111100001111;
   a = 32'h00000001; b = 32'h0fff_ffff; #10;
   if (f[1] == 1)$display("sltiu test failed"); else $display("sltiu test succeeded");
   i = 32'b001011_00001_00000_0000111100001111; #10;
   if (f[1] == 0)$display("sltiu(reversed) test failed"); else $display("sltiu(reversed) test succeeded");
   i = 32'b001011_00000_00001_1000111100001111;
   a = 32'h00000001; b = 32'h0fff_ffff; #10;
   if (f[1] == 1)$display("sltiu(negative) test failed"); else $display("sltiu(negative) test succeeded");
   $display("-------------sltiu test over-------------");
 
   // lw test
   i = 32'b100011_00000_00001_0000000000000110; 
   a = 32'h00000004; b = 32'h00000000; #10;
   if (r !== 32'h0000000a | f != 3'b000) $display("lw test failed."); else $display("lw test succeeded");
   i = 32'b100011_00000_00001_1111111111111111; 
   a = 32'h00000004; b = 32'h00000000; #10;
   if (r !== 32'h00000003 | f != 3'b000) $display("lw test failed."); else $display("lw test succeeded");
   // sw test
   i = 32'b101011_00001_00000_0000000000000110; 
   b = 32'h00000004; a = 32'h00000000; #10;
   if (r !== 32'h0000000a | f != 3'b000) $display("sw test failed."); else $display("sw test succeeded");
   i = 32'b101011_00000_00001_1111111111111111; 
   a = 32'h00000004; b = 32'h00000000; #10;
   if (r !== 32'h00000003 | f != 3'b000) $display("sw test failed."); else $display("sw test succeeded");
   $display("-------------lw,sw test over-------------");

   //sll 
   i = 32'b000000_00001_00000_00000_00010_000000;
   a = 32'h00000010; b = 32'h00000011; #10;
   if (r !== 32'h00000040 | f != 3'b000) $display("sll test failed."); else $display("sll test succeeded");
   i = 32'b000000_00001_00000_00000_00100_000000;
   a = 32'hffff_ffff; b = 32'h00000011; #10;
   if (r !== 32'hffff_fff0 | f != 3'b000) $display("sll test failed."); else $display("sll test succeeded");
   i = 32'b000000_00000_00001_00000_00010_000000;
   a = 32'h00000010; b = 32'h00000011; #10;
   if (r !== 32'h00000044 | f != 3'b000) $display("sll test failed."); else $display("sll test succeeded");
   //srl
   i = 32'b000000_00001_00000_00000_00010_000010;
   a = 32'h00000040; b = 32'h00000011; #10;
   if (r !== 32'h00000010 | f != 3'b000) $display("srl test failed."); else $display("srl test succeeded");
   i = 32'b000000_00000_00001_00000_00010_000010;
   b = 32'h00000040; a = 32'h00000011; #10;
   if (r !== 32'h00000010 | f != 3'b000) $display("srl test failed."); else $display("srl test succeeded");
   //sra
   i = 32'b000000_00001_00000_00000_00010_000011;
   a = 32'h00000040; b = 32'h00000011; #10;
   if (r !== 32'h00000010 | f != 3'b000) $display("sra test failed."); else $display("sra test succeeded");
   a = 32'hffff_fff4; #10;
   if (r !== 32'hffff_fffd | f != 3'b000) $display("sra(negative) test failed."); else $display("sra(negative) test succeeded");
   $display("-------------sll, srl, sra over-------------");   
   //sllv
   i = 32'b000000_00001_00000_00000_00000_000100;
   a = 32'hffff_ffff; b = 32'h0000_0004; #10;
   if (r !== 32'hffff_fff0 | f != 3'b000) $display("sllv test failed."); else $display("sllv test succeeded");
   i = 32'b000000_00000_00001_00000_00000_000100;
   b = 32'hffff_ffff; a = 32'h0000_0004; #10;
   if (r !== 32'hffff_fff0 | f != 3'b000) $display("sllv(reversed) test failed."); else $display("sllv(reversed) test succeeded");
   //srlv
   i = 32'b000000_00001_00000_00000_00000_000110;
   a = 32'hffff_ffff; b = 32'h0000_0004; #10;
   if (r !== 32'h0fff_ffff | f != 3'b000) $display("srlv test failed."); else $display("srlv test succeeded");
   i = 32'b000000_00000_00001_00000_00000_000110;
   b = 32'hffff_ffff; a = 32'h0000_0004; #10;
   if (r !== 32'h0fff_ffff | f != 3'b000) $display("srlv(reversed) test failed."); else $display("srlv(reversed) test succeeded");
   //srav
   i = 32'b000000_00001_00000_00000_00000_000111;
   a = 32'h0000_000f; b = 32'h00000002; #10;
   if (r !== 32'h0000_0003 | f != 3'b000) $display("srav test failed."); else $display("srav test succeeded");
   i = 32'b000000_00001_00000_00000_00000_000111;
   a = 32'hffff_ffff; b = 32'h0000_0004; #10;
   if (r !== 32'hffff_ffff | f != 3'b000) $display("srav(negative) test failed."); else $display("srav (negative) test succeeded");
   i = 32'b000000_00000_00001_00000_00000_000111;
   b = 32'hffff_ffff; a = 32'h0000_0004; #10;
   if (r !== 32'hffff_ffff | f != 3'b000) $display("srav(reversed) test failed."); else $display("srav(reversed) test succeeded");
   $display("-------------sllv, srlv, srav over-------------");  
   
end
endmodule