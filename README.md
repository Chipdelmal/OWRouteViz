# onewheelViz


```
ffmpeg -start_number 1 -r 35 -f image2 -s 1920x1080 -i %08d.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -preset veryslow -crf 15 -pix_fmt yuv420p OUTPUT_PATH.mp4 
```