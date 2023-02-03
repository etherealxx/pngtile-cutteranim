#https://github.com/etherealxx
import os, sys, shutil
from PIL import Image, ImageFont, ImageDraw
Image.MAX_IMAGE_PIXELS = None

#customizable
splitted_width = 512
splitted_height = 768
number_of_splits = 4
text_on_the_left = True
texts = ["Macross Anime", "Anything v3", "Aphrodite RealGirls", "Art and Eros Prune-Fix"] #
x_pos_of_text = [205, 270, 130, 70] #ignore this if text_on_the_left is true
#customizable

chunk_size = (splitted_width * number_of_splits, splitted_height)
def split_image(image_path, chunk_size):

    img = Image.open(image_path)
    width, height = img.size
    chunks = height // chunk_size[1]

    for i in range(chunks):
        box = (0, i*chunk_size[1], width, (i+1)*chunk_size[1])
        yield img.crop(box)

if __name__ == "__main__":
    input_folder = sys.argv[1]
    if input_folder == '':
        print("You need to drag and drop the desired folder that contains all the image you want to convert to the bat file")
        os.system('pause')
        exit()

    print("Working directory is: " + input_folder)
    print()

    

    for file in os.listdir(input_folder):
        if file.endswith(".png"):
            file_path = os.path.join(input_folder, file)
            path = os.path.dirname(file_path)
            filename = os.path.splitext(os.path.basename(file_path))[0]
            print('splitting image ' + filename)
            count = 1

            for idx, chunk in enumerate(split_image(file_path, chunk_size)):
                chunk.save(f"{path}/{filename}_{idx}.png")
                print('image ' + filename + ' splitted part ' + str(count))
                count += 1

            image_hugedonepath = os.path.join(input_folder + "\\raw_huge_image")    
            if not os.path.exists(image_hugedonepath):
                os.makedirs(image_hugedonepath)
            # move the processed image to that folder
            shutil.move(os.path.join(input_folder, filename + ".png"), image_hugedonepath)
            print("Moved " + filename + " into 'raw_huge_image' folder")
            print()

    image_list = [f for f in os.listdir(input_folder) if f.endswith(".png") and not f.endswith("_anim.png")]
    for x in range (1, number_of_splits + 1):
        exec(f"output{x} = ''")

    # Iterate through the list of images
    for image_name in image_list:
        # Open the input image
        image = Image.open(os.path.join(input_folder, image_name))
        print("Working on: " + image_name)

        # Get the width and height of the image
        width, height = image.size

        # Create the output images
        for x in range (1, number_of_splits + 1):
            topright = x * splitted_width
            topleft = topright - splitted_width
            exec(f"output{x} = image.crop(({topleft}, 0, {topright}, {splitted_height}))")

        # Get the base name of the image (without the file extension)
        base_name = os.path.splitext(image_name)[0]

        # Save the output images
        for x in range (1, number_of_splits + 1):
            exec(f'output{x}.save(os.path.join(input_folder, base_name + "_temp{x}.png"))')

        print(f'Cropped "{image_name}" into {number_of_splits} temporary images')

        # Write text on all four tempfiles
        for x in range (1, number_of_splits + 1):
            img = Image.open(os.path.join(input_folder, base_name + "_temp" + str(x) + ".png"))

            # Create an ImageDraw object
            draw = ImageDraw.Draw(img)

            # Set the font and size of the text
            font = ImageFont.truetype("OpenSansCondensed-Bold.ttf", 50)

            # Set the position and the text itself
            currenttext = texts[x-1]
            if text_on_the_left == True:
                text_pos = (10, 0)
            else:
                text_pos = x_pos_of_text[x-1]
            
            # Add the drop shadow
            shadow_color = (0, 0, 0)
            shadow_offset = (3, 3)
            draw.text((text_pos[0]+shadow_offset[0], text_pos[1]+shadow_offset[1]), currenttext, font=font, fill=shadow_color)

            # Add the text to the image
            draw.text(text_pos, currenttext, font=font, fill=(255,255,255))

            # Save the image
            saveaftertext = os.path.join(input_folder, base_name + "_temp" + str(x) + ".png")
            img.save(saveaftertext)
            print("Saved image " + image_name + " with text " + currenttext + " for apng later")
            os.system(f'pngnq-s9 -s 1 "{saveaftertext}"')
            print("Compressed " + image_name + " with pngnq-s9")
            os.remove(saveaftertext)
            os.rename(os.path.join(input_folder, base_name + "_temp" + str(x) + "-nq8.png"), saveaftertext)

        # Save the animation as an APNG
        print("Saving the apng of " + image_name + "...")
        #image1.save(os.path.join(input_folder, base_name + "_anim.png"), save_all=True, append_images=images[1:], duration=durations, loop=0)
        os.system('apngasm64 "{}" "{}_temp*.png" 3 2'.format(os.path.join(input_folder, base_name + "_anim.png"), os.path.join(input_folder, base_name)))
        print()
        print("Apng saved as " + base_name + "_anim.png")

        # make a folder to contain the processed image
        image_donepath = os.path.join(input_folder + "\\raw_splitted_image")
        image_finalpath = os.path.join(input_folder + "\\processed_apngs")
        image_texted = os.path.join(input_folder + "\\texted_pngs")
        #image_texted_current = os.path.join(image_texted, image_name)
        if not os.path.exists(image_donepath):
            os.makedirs(image_donepath)
        if not os.path.exists(image_finalpath):
            os.makedirs(image_finalpath)
        if not os.path.exists(image_texted):
            os.makedirs(image_texted)
        #if not os.path.exists(image_texted_current):
        #    os.makedirs(image_texted_current)
        
        # move every temp file to the texted png folder
        for x in range (1, number_of_splits + 1):
            temp_move = os.path.join(input_folder, base_name + "_temp" + str(x) + ".png")
            #shutil.move(temp_move, image_texted_current)
            shutil.move(temp_move, image_texted)
        print("Temp file of " + image_name + " moved to the 'texted_pngs' folder")
        
        # move the processed image to that folder
        shutil.move(os.path.join(input_folder, image_name), image_donepath)
        print("Moved raw image of" + image_name + " into 'raw_splitted_image' folder")

        final_name = os.path.join(input_folder, base_name + ".png")
        os.rename(os.path.join(input_folder, base_name + "_anim.png"), final_name)
        shutil.move(final_name, image_finalpath)
        print("Moved processed apng of" + image_name + " into 'processed_apngs' folder")
        print()

print()
print("Batch job done.")
print()
#os.system("pause")
