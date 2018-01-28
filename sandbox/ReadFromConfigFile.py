
file = open("config.txt","r")
line1 = file.readline().strip()
print("Line ", line1)
line2 = file.readline().strip()
print("Line ", line2)
line3 = file.readline().strip()
print("Line ", line3)
file.close()