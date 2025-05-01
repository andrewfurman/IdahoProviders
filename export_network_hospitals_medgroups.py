# this python function will export all the hospitals, medical groups, and networks to a CSV file.  It will use the hospital, medical group, and network models to query the database and then write the results to a CSV file.  The CSV file will have

# for networks export only ID, Code, Name

# for network hospital relationships export only hospital ID, network ID

# for hospitals export only ID, Name

# for medical group hospital relationships export only medical group ID, hospital ID

# for medical groups export only ID, Name, address_line

# return the text in a markdown style table that can be preinted to the command line

