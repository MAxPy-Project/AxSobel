// ysba 2022-07-20

module sobel_gradient(a1, a2, b1, b2, c1, c2, grad);
    input [7:0] a1, a2, b1, b2, c1, c2;
    output [10:0] grad;
    wire signed [8:0] g1, g2, g3;
    wire signed [9:0] g13, g22;
    wire signed [10:0] g;
    assign g1 = {1'b0, a1} - {1'b0, a2};
    assign g2 = {1'b0, b1} - {1'b0, b2};
    assign g3 = {1'b0, c1} - {1'b0, c2};
    assign g13 = g1 + g3;
    assign g22 = g2 * 9'd2;
    assign g = g13 + g22;
    assign grad = g[10] ? ~g+11'd1 : g;
endmodule

module sobel(p0, p1, p2, p3, p5, p6, p7, p8, threshold, edge_out);
    input [7:0] p0,p1,p2,p3,p5,p6,p7,p8;
    input [7:0] threshold;
    output edge_out;
    wire [10:0] gx, gy;
    wire [11:0] grad;
    sobel_gradient grad_x(p2, p0, p5, p3, p8, p6, gx);
    sobel_gradient grad_y(p0, p6, p1, p7, p2, p8, gy);
    assign grad = gx + gy;
    assign edge_out = grad > {4'd0, threshold} ? 1'b1 : 1'b0;
endmodule
