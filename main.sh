
#!/bin/bash

PT_I='/home/chipdelmal/Documents/OneWheel/img/%08d.png'
PT_O='/home/chipdelmal/Documents/OneWheel/img/OUTPUT.mp4'

# python main.py
ffmpeg -start_number 1 -r 30 -f image2 -s 1920x1080 -i $PT_I -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -preset veryslow -crf 15 -pix_fmt yuv420p $PT_O