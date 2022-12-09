module HazardUnit(CLK,RegWriteEM,RegWriteMW,Rt,Rs,RdEM,RdMW,FA,FB);
    input[4:0] Rt,Rs,RdEM,RdMW;
    input CLK,RegWriteEM,RegWriteMW;
    output[1:0] FA,FB;

    reg r_FA,r_FB;
    initial begin
        r_FA <= 2'b0;
        r_FB <= 2'b0;
    end
    
    //根据情况的forward处理
    always@(RegWriteMW,RegWriteEM,RdMW,RdEM,Rs,Rt) begin
        r_FA = 2'b0;
        r_FB = 2'b0;
        if ((RegWriteMW == 1) & (RdMW != 0) & (RdMW == Rs)) begin
            r_FA = 2'b00;//01
            r_FB = 2'b00;
            //$display("1");
        end
        if ((RegWriteMW == 1) & (RdMW != 0) & (RdMW == Rt)) begin
            r_FB = 2'b00;//01
            r_FA = 2'b00;
            //$display("2");
        end
        if ((RegWriteEM == 1) & (RdEM != 0) & (RdEM == Rs)) begin
            r_FB = 2'b00;
            r_FA = 2'b00;//10
            //$display("3");
        end
        if ((RegWriteEM == 1) & (RdEM != 0) & (RdEM == Rt)) begin
            r_FB = 2'b00;//10
            r_FA = 2'b00;
            //$display("4");
        end 
        //$display("%b",r_FA);
        //$display("%b",r_FB);
        //$display("---------");
    end

/*
    always@(posedge CLK) begin
        if ((RegWriteEM == 1) & (RdEM != 0) & (RdEM == Rs)) begin
            r_FB <= 2'b00;
            r_FA <= 2'b10;//10
        end 
        else if ((RegWriteEM == 1) & (RdEM != 0) & (RdEM == Rt)) begin
            r_FB <= 2'b10;//10
            r_FA <= 2'b00;
        end   
        else if ((RegWriteMW == 1) & (RdMW != 0) & (RdMW == Rt)) begin
            r_FB <= 2'b01;//01
            r_FA <= 2'b00;
        end     
        else if ((RegWriteMW == 1) & (RdMW != 0) & (RdMW == Rs)) begin
            r_FA <= 2'b01;//01
            r_FB <= 2'b00;
        end  
        else begin
            r_FA <= 2'b00;
            r_FB <= 2'b00;
        end 
    end
*/
    assign FA = r_FA;
    assign FB = r_FB;
endmodule