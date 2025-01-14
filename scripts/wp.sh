cd ~/.config/scripts/
for a in ~/Pictures/Wallpapers/*; do 
    filename=$(basename "$a") 
    echo -en "$filename\0icon\x1f$a\n"
done | rofi -dmenu -theme 'temp.rasi' | xargs -I{} bash -c 'swww img "$(find ~/Pictures/Wallpapers/ -name "{}")" -t wave'

