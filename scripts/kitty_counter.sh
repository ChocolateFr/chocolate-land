#!/bin/bash

# Count the number of kitty processes
kitty_count=$(pgrep -c kitty)

echo $kitty_count
