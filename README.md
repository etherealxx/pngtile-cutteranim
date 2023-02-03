# pngtile-cutteranim

Say you have a huge png with 2048x3072 resolution, which actually is a tile of 16 images with 512x768 resolution each. <br/>
***Put that image into a folder, and drag and drop the folder into the .bat file**, and the tool will works.<br/><br/>
This tool (by default) will split that huge png into 4 horizontal image, each with 2048x768 resolution. And each horizontal image will be:

- Cutted to 512x768 image each
- Compressed with `pngnq-s9`
- Given different text for each image with `Open Sans Condensed Bold` font
- Combined into an apng using `apngasm` 

And the final result will be 4 apng images, each containing 4 images animated with 2 seconds duration for each frame.

## Prerequisite

- Download `apngasm64.exe` from [here](https://sourceforge.net/projects/apngasm/files/2.91/apngasm-2.91-bin-win64.zip/download) and copy the executable to `C:\Windows`
- Download `pngnq-s9.exe` from [here](https://sourceforge.net/projects/pngnqs9/files/pngnq-s9-2.0.2.zip/download), extract the file, and copy the executable to `C:\Windows`
- Download `OpenSans-CondensedBold.ttf` from [here](https://github.com/googlefonts/opensans/raw/main/fonts/ttf/OpenSans-CondensedBold.ttf), rename it to `OpenSansCondensed-Bold.ttf` and install it for all user

## Customizables

You will notice these on the top of the python file

```python
splitted_width = 512
splitted_height = 768
number_of_splits = 4
text_on_the_left = True
texts = ["Macross Anime", "Anything v3", "Aphrodite RealGirls", "Art and Eros Prune-Fix"] #
textfont = "OpenSansCondensed-Bold.ttf"
textsize = 50
x_pos_of_text = [205, 270, 130, 70] #ignore this if text_on_the_left is true
```

Those things can be customized yo your likings. Most of it are self-explanatory.

`textfont` are the filename of the `.ttf` file located on `C:\Windows\Fonts`.

`text_on_the_left` will set the x position of the text to `10` for every images.

If you add the `number_of_splits` to more than 4, then you need to add more text to write on `texts` to match it.

#### Additional Note

The `.bat` file will runs whatever `.py` file with the same name of it. In addition, it will convert any file/folder that is drag-and-dropped into it into its path as string variable, and will send that variable into the `.py` file as first argument. And the `.py` file can catch that argument and convert it into a variable again with `path = sys.argv[1]`.
