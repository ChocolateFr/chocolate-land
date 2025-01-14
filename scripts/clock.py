import jdatetime

# Get the current date and time in the Shamsi calendar
shamsi_date = jdatetime.datetime.now()

# Format the date and time in a human-readable way
formatted_date_time = shamsi_date.strftime('%Y/%m/%d %H:%M:%S')

# Print the date and time in Shamsi
print("󰥔",formatted_date_time)

