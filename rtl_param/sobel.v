// ysba 2022-07-20

module sobel_gradient(a1, a2, b1, b2, c1, c2, ag);
    input [7:0] a1, a2, b1, b2, c1, c2;
    output [15:0] ag;
    wire signed [15:0] g1, g2, g3;
    wire signed [15:0] g13, g22;
    wire signed [15:0] g;
    [[PARAM_ADD1]] #(16, [[PARAM_K1]]) sub1x ({8'b00000000, a1}, {8'b11111111, ~a2}, g1);
    [[PARAM_ADD1]] #(16, [[PARAM_K1]]) sub2x ({8'b00000000, b1}, {8'b11111111, ~b2}, g2);
    [[PARAM_ADD1]] #(16, [[PARAM_K1]]) sub3x ({8'b00000000, c1}, {8'b11111111, ~c2}, g3);
    [[PARAM_ADD1]] #(16, [[PARAM_K2]]) sum1(g1, g3, g13);
    assign g22 = g2 * 2;
    [[PARAM_ADD1]] #(16, [[PARAM_K3]]) sum2(g13, g22, g);
    assign ag = g < 0 ? ~g : g;
endmodule

module sobel(p0, p1, p2, p3, p5, p6, p7, p8, threshold, edge_out);
    input [7:0] p0,p1,p2,p3,p5,p6,p7,p8;
    input [7:0] threshold;
    output edge_out;
    wire [15:0] ax, ay;
    wire [15:0] grad;
    sobel_gradient grad_x(p2, p0, p5, p3, p8, p6, ax);
    sobel_gradient grad_y(p0, p6, p1, p7, p2, p8, ay);     
    [[PARAM_ADD1]] #(16, [[PARAM_K4]]) sum_final(ax, ay, grad);
    assign edge_out = grad > threshold ? 1'b1 : 1'b0;
endmodule
