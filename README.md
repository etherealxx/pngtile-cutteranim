# pngtile-cutteranim
Say you have a huge png with 2048x3072 resolution, which actually is a tile of 16 images with 512x768 resolution each. This tool will split that huge png into 4 horizontal image, each with 2048x768 resolution. And and each horizontal image:
- will be cutted to 512x768 image each
- will be compressed with `pngnq-s9`
- will be given different text for each image
- will be combined into an apng using `apngasm` 

And the final result will be 4 apng images, each containing 4 images animated with 2 seconds duration for each frame.

## Prerequisite
- Download `apngasm64.exe` from [here](https://sourceforge.net/projects/apngasm/files/2.91/apngasm-2.91-bin-win64.zip/download) and copy the executable to `C:\Windows`
- Download `pngnq-s9.exe` from [here](https://sourceforge.net/projects/pngnqs9/files/pngnq-s9-2.0.2.zip/download), extract the file, and copy the executable to `C:\Windows`
- Download `OpenSans-CondensedBold.ttf` from [here](https://github.com/googlefonts/opensans/raw/main/fonts/ttf/OpenSans-CondensedBold.ttf), rename it to `OpenSansCondensed-Bold.ttf` and install it for all user
