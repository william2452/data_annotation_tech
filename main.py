import requests
from bs4 import BeautifulSoup

#The main function where the url is defined and passed to the visualize_url_html() function
def main():
    url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
    visualize_url_html(url)
    
#The bulk of the work happens in this function. Getting HTML data, parsing it, and assigning/printing the final result
def visualize_url_html(url):
    #Grab the raw html data from the provided url
    try:
        data = requests.get(url)
        data.raise_for_status()
        html_content = data.text
    except requests.exceptions.RequestException as e:
        print(f"Unable to reach URL: {url}")
        html_content = None

    #If there is content, use BeautifulSoup library to parse the content and find the table tags
    if html_content:
        data = BeautifulSoup(html_content, "html.parser")
        table = data.find("table")

        #Search within the table tag for the row and column tags
        uni_data = []
        x_max = 0
        y_max = 0
        if table:
            #Find instances of tr symbolizing rows. Skip row 1 since it is the header row
            rows = table.find_all("tr")
            for row in rows[1:]:
                #Find instances of td symbolizing columns
                cols = row.find_all("td")
                if len(cols) == 3:
                    x_plot = int(cols[0].get_text(strip=True))
                    if x_plot > x_max:
                        x_max = x_plot
                    uni_val = cols[1].get_text(strip=True)
                    y_plot = int(cols[2].get_text(strip=True))
                    if y_plot > y_max:
                        y_max = y_plot
                    uni_data.append({"uni_val": uni_val, "x_plot": x_plot, "y_plot": y_plot})
                else:
                    print(f"Row {row} does not have enough columns")
        else:
            print("No table data found")

        #Create an empty grid with the max x and y coordinates. Add 1 to the maxes to account for 0 index
        filler = " "
        grid = [[filler for _ in range(x_max+1)] for _ in range(y_max+1)]
            
        #For each item in the uni_data dictionary, grab the coordinates
        for item in uni_data:
            uni_val = item["uni_val"]
            x_plot = item["x_plot"]
            y_plot = item["y_plot"]
            #Make sure x and y coordinates are within the range of 0 and max value +1
            if 0 <= y_plot <= y_max and 0 <= x_plot <= x_max:
                grid[y_plot][x_plot] = uni_val
            else:
                print(f"Unicode '{uni_val}' at ({x_plot}, {y_plot}) is out of range")
        #Print out the now replaced and filled in grid. Use .join to remove all the unnecessary quotations and commas
        for row in range(0, y_max+1):
            print("".join(grid[row]))

if __name__ == "__main__":
    main()