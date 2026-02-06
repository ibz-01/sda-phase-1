import pandas as p

def loadFileData(filePath): #loading the file
    try:
        df = p.read_csv(filePath)
    except FileNotFoundError:
        raise Exception("File not found.")
    
    year_columns = list(map(str, range(1960, 2025))) #list containing all years
    
    df_formatted = df.melt( #converting into long format (multiple rows for 1 country)
        
        id_vars= ["Country Name", "Country Code", "Indicator Name", "Indicator Code", "Continent"],
        value_vars=year_columns, #cols to rows
        var_name="Year",
        value_name="Value"
    )

    df["Year"] = p.to_numeric(df["Year"], errors="coerce") #text to num
    df["Value"] = p.to_numeric(df["Value"], errors="coerce")
    
    df_formatted = df_formatted.dropna(subset=["Year", "Value"]) #removing missing GDP rows

    return df_formatted


    

