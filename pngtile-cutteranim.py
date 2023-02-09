#https://github.com/etherealxx
import os, sys, shutil
from PIL import Image, ImageFont, ImageDraw
Image.MAX_IMAGE_PIXELS = None

#customizable
splitted_width = 512
splitted_height = 768
number_of_splits = 4
texts = ["Macross Anime", "Anything v3", "Aphrodite RealGirls", "Art and Eros Prune-Fix"] #be sure to add text to this when you add more number of splits
x_pos_of_text = [205, 270, 130, 70] #ignore this if text_on_the_left is true
textfont = "OpenSansCondensed-Bold.ttf" #name of the font located on C:\Windows\Font
text_on_the_left = True #if true, all text will get x=10 from the left
textsize = 50
#customizable

chunk_size = (splitted_width * number_of_splits, splitted_height)

def text_checker(my_list, index):
    if index >= 0 and index < len(my_list):
        return my_list[index]
    else:
        return "(empty)"

def split_image(image_path, chunk_size):

    img = Image.open(image_path)
    width, height = img.size
    chunks = height // chunk_size[1]

    for i in range(chunks):
        box = (0, i*chunk_size[1], width, (i+1)*chunk_size[1])
        yield img.crop(box)

def renamer(number, path, filename):
    txtfile = os.path.join(path, filename + ".txt")
    if os.path.exists(txtfile):
        with open(txtfile, "r") as file:
            lines = file.readlines()
            return lines[number].strip()
    else:
        print(F"txt file of {filename} not found")
        return 0

if __name__ == "__main__":
    input_folder = sys.argv[1]
    if input_folder == "":
        print("You need to drag and drop the desired folder that contains all the image you want to convert to the bat file")
        os.system("pause")
        exit()

    print("Working directory is: " + input_folder)
    print()

    for file in os.listdir(input_folder):
        if file.endswith(".png"):
            file_path = os.path.join(input_folder, file)
            path = os.path.dirname(file_path)
            filename = os.path.splitext(os.path.basename(file_path))[0]
            print("splitting image " + filename)
            count = 1

            for idx, chunk in enumerate(split_image(file_path, chunk_size)):
                chunk.save(f"{path}\\{filename}_{idx}.png")
                print("image " + filename + " splitted part " + str(count))
                torename = renamer(idx, path, filename)
                if not torename == 0:
                    os.rename(f"{path}\\{filename}_{idx}.png", os.path.join(path, torename + ".png"))
                    print(f'renamed {filename}_{idx} to "{torename}"')
                count += 1

            image_hugedonepath = os.path.join(input_folder + "\\raw_huge_image")    
            if not os.path.exists(image_hugedonepath):
                os.makedirs(image_hugedonepath)
            # move the processed image to that folder
            shutil.move(os.path.join(input_folder, filename + ".png"), image_hugedonepath)
            txtpath2 = os.path.join(input_folder, filename + ".txt")
            if os.path.exists(txtpath2):
                shutil.move(txtpath2, image_hugedonepath)
            print("Moved " + filename + " into 'raw_huge_image' folder")
            print()

    image_list = [f for f in os.listdir(input_folder) if f.endswith(".png") and not f.endswith("_anim.png")]
    for x in range (1, number_of_splits + 1):
        exec(f"output{x} = ''")

    # Iterate through the list of images
    for image_name in image_list:
        # Open the input image
        img = Image.open(os.path.join(input_folder, image_name))
        print("Working on: " + image_name)

        # Get the base name of the image (without the file extension)
        base_name = os.path.splitext(image_name)[0]

        # Create an ImageDraw object
        draw = ImageDraw.Draw(img)

        # Set the font and size of the text
        font = ImageFont.truetype(textfont, textsize)
        # Write text on all four tempfiles
        for x in range (1, number_of_splits + 1):

            # Set the position and the text itself
            currenttext = text_checker(texts, x-1)
            if text_on_the_left == True:
                text_pos = (((x - 1) * splitted_width) + 10, 0)
            else:
                text_pos = x_pos_of_text[x-1]
            
            # Add the drop shadow
            shadow_color = (0, 0, 0)
            shadow_offset = (3, 3)
            draw.text((text_pos[0]+shadow_offset[0], text_pos[1]+shadow_offset[1]), currenttext, font=font, fill=shadow_color)

            # Add the text to the image
            draw.text(text_pos, currenttext, font=font, fill=(255,255,255))

        # Save the image
        saveaftertext = os.path.join(input_folder, base_name + "_texted.png")
        img.save(saveaftertext)
        print("Saved image '" + image_name + "' with text to be cutted later")

        image = Image.open(saveaftertext)

        width, height = image.size

        # Create the output images
        for x in range (1, number_of_splits + 1):
            topright = x * splitted_width
            topleft = topright - splitted_width
            exec(f"output{x} = image.crop(({topleft}, 0, {topright}, {splitted_height}))")

        # Save the output images
        for x in range (1, number_of_splits + 1):
            splittemp = os.path.join(input_folder, base_name + f"_temp{x}.png")
            exec(f"output{x}.save(os.path.join(input_folder, base_name + \"_temp{x}.png\"))")
            os.system(f'pngnq-s9 -s 1 "{splittemp}"')
            print("Compressed '" + base_name + f"_temp{x}.png' with pngnq-s9")
            os.remove(splittemp)
            os.rename(os.path.join(input_folder, base_name + "_temp" + str(x) + "-nq8.png"), splittemp)
            # Saving the jpg thumbnail
            if x ==1:
                print("Saving the first frame of " + image_name + " as compressed jpg")
                print()
                os.system(f'gm convert -verbose -quality 70 "{splittemp}" "' + os.path.join(input_folder, base_name + ".preview.jpg") +'"')
                print()

        print(f"Cropped \"{image_name}\" into {number_of_splits} temporary images")

        # Save the animation as an APNG
        print()
        print("Saving the apng of '" + image_name + "'...")
        #image1.save(os.path.join(input_folder, base_name + "_anim.png"), save_all=True, append_images=images[1:], duration=durations, loop=0)
        os.system("apngasm64 \"{}\" \"{}_temp*.png\" 3 2".format(os.path.join(input_folder, base_name + "_anim.png"), os.path.join(input_folder, base_name)))
        print()
        print("Apng saved as '" + base_name + "_anim.png'")

        # make a folder to contain the processed image
        image_donepath = os.path.join(input_folder + "\\splitted_texted_image")
        image_finalpath = os.path.join(input_folder + "\\processed_apngs")
        image_jpg = os.path.join(input_folder + "\\jpg_thumbnails")
        image_texted = os.path.join(input_folder + "\\individual_texted_pngs")
        #image_texted_current = os.path.join(image_texted, image_name)
        if not os.path.exists(image_donepath):
            os.makedirs(image_donepath)
        if not os.path.exists(image_finalpath):
            os.makedirs(image_finalpath)
        if not os.path.exists(image_texted):
            os.makedirs(image_texted)
        if not os.path.exists(image_jpg):
            os.makedirs(image_jpg)
        #if not os.path.exists(image_texted_current):
        #    os.makedirs(image_texted_current)
        
        # move every temp file to the texted png folder
        for x in range (1, number_of_splits + 1):
            #print(f"debug {x} input_folder: {input_folder}")
            #print(f"debug {x} base_name: {base_name}")
            temp_name = os.path.join(input_folder, base_name + "_temp" + str(x) + ".png")
            #print(f"debug {x} temp_name: {temp_name}")
            temp_rename = os.path.join(input_folder, base_name + "_" + str(x) + ".png")
            #print(f"debug {x} temp_rename: {temp_rename}")
            #shutil.move(temp_move, image_texted_current)
            #os.remove(temp_move)
            os.rename(temp_name, temp_rename)
            shutil.move(temp_rename, image_texted)
        
        print("Temp file of " + image_name + " moved to the 'individual_texted_pngs' folder")
        
        # move the processed image to that folder
        #shutil.move(os.path.join(input_folder, image_name), image_donepath)
        os.remove(os.path.join(input_folder, image_name))
        shutil.move(saveaftertext, image_donepath)
        print("Moved splitted texted image of " + image_name + " into 'splitted_texted_image' folder")

        final_name = os.path.join(input_folder, base_name + ".preview.png")
        os.rename(os.path.join(input_folder, base_name + "_anim.png"), final_name)
        shutil.move(final_name, image_finalpath)
        print("Moved processed apng of " + image_name + " into 'processed_apngs' folder")

        final_name = os.path.join(input_folder, base_name + ".preview.jpg")
        shutil.move(final_name, image_jpg)
        print("Moved jpg thumbnail of " + image_name + " into 'jpg_thumbnails' folder")
        print()

print()
print("Batch job done.")
print()
#os.system("pause")
