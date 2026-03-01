with open("gdp_with_continent_filled.json", "r") as f:
    content = f.read()

content = content.replace("NaN", "null")
content = content.replace("#@$!\\", "null")

with open("gdp_with_continent_filled_cleaned.json", "w") as f:
    f.write(content)

print("Cleaned file created.")