#!/bin/bash

# Get CPU usage
cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
cpu_usage=$(printf "%.2f" "$cpu_usage")

# Get Memory usage
memory_usage=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
memory_usage=$(printf "%.2f" "$memory_usage")

# Get Disk read/write usage

# Get Internet bandwidth usage (Download/Upload in ms)

# Get system temperature (assuming your system supports the thermal_zone0 path)
temperature=$(cat /sys/class/thermal/thermal_zone0/temp)
temperature=$((temperature / 1000))  # Convert to Celsius
if [[ $temperature -le 69 ]];then
temperature=" $temperature"
else
temperature=" $temperature"
fi
#process_count=$(ps aux --no-headers | wc -l)
#proccess_count='alot'
# Format the output

cd ~/.config/scripts/
echo " $cpu_usage%  󱩵 $memory_usage%   $(bash kitty_counter.sh)  $temperature°C "
