from MAxPy import results
import sys
from skimage.metrics import structural_similarity
import cv2
import numpy as np
import importlib
import os.path
import os

def sobel_testbench(ckt=None, results_filename=None):

    image_list = [
        "images/birds/birds.jpeg",
        "images/butterfly/butterfly.jpg",
        "images/fish/fish.jpg",
        "images/mulholland/mulholland.jpeg",
    ]

    thresdhold = 127

    rst = results.ResultsTable(results_filename, ["ssim", "accuracy"])

    print(">>> testbench init")

    sobel_filter = ckt.sobel()

    print(f"  > circuit: {sobel_filter.name()}")
    print(f"  > parameters: {sobel_filter.parameters}")
    print("")
    print(f"  > threshold: {thresdhold}")
    print("")
    print("  > images list:")
    
    for image in image_list:
        print(f"    > {image}")
    print("")

    ssim_value = 0
    accuracy = 0

    for input_image_name in image_list:
        
        image_name = input_image_name.split('.')[0]
        print(f"  > processing image {image_name}")
        # check if reference already exists for this images
        image_ref_path = image_name + '_ref_bw.png'
        if os.path.isfile(image_ref_path) is False:
            print(f"    > reference not found, creating ({image_ref_path})")
            #reference do not exists, create it
            # convert image to grey scale
            img_in = cv2.imread(input_image_name, cv2.IMREAD_GRAYSCALE)
            cv2.imwrite(image_name + '_orig_gray.png', img_in)
            # apply gassian filter to blur out the image (helps adge detection)
            img_in = cv2.GaussianBlur(img_in, (3, 3), 0)
            cv2.imwrite(image_name + '_orig_blur.png', img_in)
            height = len(img_in)
            width = len(img_in[0])
            # create sobel filter ref
            weight = 1
            ddepth = cv2.CV_16S
            grad_x = cv2.Sobel(img_in, ddepth, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
            grad_y = cv2.Sobel(img_in, ddepth, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
            abs_grad_x = cv2.convertScaleAbs(grad_x)
            abs_grad_y = cv2.convertScaleAbs(grad_y)
            grad = cv2.addWeighted(src1=abs_grad_x, alpha=weight, src2=abs_grad_y, beta=weight, gamma=0)
            cv2.imwrite(image_name + '_ref_gray.png', grad)
            # convert sobel filter do binary image
            thresh, ref_bw = cv2.threshold(grad, thresdhold, 255, cv2.THRESH_BINARY)
            cv2.imwrite(image_ref_path, ref_bw)
        else:
            # reference already exists, loads it
            print(f"    > reference ok, loading ({image_ref_path})")
            img_in = cv2.imread(image_name + '_orig_blur.png', cv2.IMREAD_GRAYSCALE)
            ref_bw = cv2.imread(image_ref_path, cv2.IMREAD_GRAYSCALE)
            
        # check if result csv file already exists
        result_file_path = f"{sobel_filter.name()}.csv"
        if os.path.isfile(result_file_path) is False:
            # result file do not existe, create it
            print(f"    > result csv file not found, creating ({result_file_path})")
            result_file = open(result_file_path, "w")
            result_file.write('circuit;parameters;area;power;timing;psnr [dB];ssim [%];total;tp;tn;fp;fn;accuracy [%];recall [%];precision [%];fscore [%]\n')
            result_file.close()
        else:
            print(f"    > result csv file ok, loading ({result_file_path})")

        height = len(img_in)
        width = len(img_in[0])
        print(f"    > dimension: W {width} x H {height}")
        
        output_image_name = f"{image_name}_{sobel_filter.name()}_{sobel_filter.parameters}_bw.png"
        
        #img_out1 = np.zeros((height, width))
        img_out2 = np.zeros((height, width), dtype=np.uint8)

        tp = 0
        tn = 0
        fp = 0
        fn = 0

        sobel_filter.set_threshold(thresdhold)

        print(f"    > loop init")

        for row in range(height):
            for col in range(width):
                prev_col = col - 1
                next_col = col + 1
                prev_row = row - 1
                next_row = row + 1
                outter_val = img_in[row][col]

                if prev_col > 0 and prev_row > 0:
                    sobel_filter.set_p0(img_in[prev_row][prev_col])
                else:
                    sobel_filter.set_p0(outter_val)

                if prev_row > 0:
                    sobel_filter.set_p1(img_in[prev_row][col])
                else:
                    sobel_filter.set_p1(outter_val)

                if next_col < width and prev_row > 0:
                    sobel_filter.set_p2(img_in[prev_row][next_col])
                else:
                    sobel_filter.set_p2(outter_val)
                
                if prev_col > 0:
                    sobel_filter.set_p3(img_in[row][prev_col])
                else:
                    sobel_filter.set_p3(outter_val)

                if next_col < width:
                    sobel_filter.set_p5(img_in[row][next_col])
                else:
                    sobel_filter.set_p5(outter_val)

                if prev_col > 0 and next_row < height:
                    sobel_filter.set_p6(img_in[next_row][prev_col])
                else:
                    sobel_filter.set_p6(outter_val)

                if next_row < height:
                    sobel_filter.set_p7(img_in[next_row][col])
                else:
                    sobel_filter.set_p7(outter_val)

                if next_col < width and next_row < height:
                    sobel_filter.set_p8(img_in[next_row][next_col])
                else:
                    sobel_filter.set_p8(outter_val)

                sobel_filter.eval() 
                #img_out1[row][col] = sobel_filter.out

                if sobel_filter.get_edge_out() == 1:
                    img_out2[row][col] = 255
                    if ref_bw[row][col] == 255:
                        tp += 1
                    else:
                        fp += 1
                else:
                    img_out2[row][col] = 0
                    if ref_bw[row][col] == 0:
                        tn += 1
                    else:
                        fn += 1

        print(f"    > loop end")

        # save images got from testbench
        #cv2.imwrite(f"{image_name}_{sobel_filter.name()}_{sobel_filter.parameters}_gray.png", img_out1)
        cv2.imwrite(output_image_name, img_out2)
        (score, diff) = structural_similarity(ref_bw, img_out2, full=True)
        
        ssim_value += score

        den = (tp + fp + tn + fn)
        if den != 0:
            accuracy += (tp + tn) / den
        else:
            accuracy += 100

    ssim_average = ssim_value / len(image_list)
    accuracy_average = accuracy * 100 / len(image_list)

    rst.add(sobel_filter, {"ssim": ssim_average, "accuracy": accuracy_average})

    print(f"> average result: ssim {ssim_average:.4f}, acc {accuracy_average:.2f}%")

    # if mod.saif_opt is True:
    #     sobel_filter.saif_path = f"{sobel_filter.name()}_{sobel_filter.parameters}.saif"
    #     sobel_filter.saif_on_the_fly(1)

    print(">>> testbench end")
    print("")

    if ssim_average >= 0.85:
        prun_flag = True
    else:
        prun_flag = False

    if ckt.saif_opt is True:
        return prun_flag, sobel_filter.node_info
    else:
        return prun_flag, []
    

if __name__ == '__main__':

    mod_list = [
        "sobel_exact.sobel",
    ]

    for mod_name in mod_list:
        mod = importlib.import_module(mod_name)
        sobel_testbench(mod, keep_output_image=True)
