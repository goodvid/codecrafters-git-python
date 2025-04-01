user_data = """AP/AR Interface
ATI Options
GL Interface
MM Interface
Other/Miscellaneous
Periodic Processing
TPDs/Coupons"""

names = user_data.split("\n")
output_lines = []

for name in names:
    string = f"case '{name}':\n\tconfigItem = 'iSeries/AS400 Finance - {name}';\nbreak;"
    output_lines.append(string)

# Write to a file
with open('test.txt', 'w') as f:
    f.write("\n".join(output_lines))

# Print output if needed
print(output_lines)
