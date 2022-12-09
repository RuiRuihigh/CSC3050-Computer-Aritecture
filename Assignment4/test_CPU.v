`timescale 100fs/100fs
module CPU_test;
    //Clock
    parameter CLK_time = 4;
    reg CLK;
    initial CLK = 0;
    always #(CLK_time / 2) CLK = ~CLK;

    reg reset,EN;
    initial begin
        reset <= 1'b0;
        EN <= 1'b1;
    end


    CPU cpu(CLK,reset,EN);
    
    integer i;
    integer poi;
   
    always@(CLK)begin
        if (cpu.InF.RD == 32'hffff_ffff)begin
            #24
            poi=$fopen("Output.txt","w");
            for (i = 0;i <= 511; i = i + 1)begin
                $fwrite(poi,"%b\n",cpu.mem.datamem.DATA_RAM[i]);
            end
            //$display("**********************");
            $display("\n");
            $display("The memory has been dumpped to the Output.txt!!!!!!");
            $display("\n");
            $fclose(poi);
            $stop;
        end
    end
    


endmodule