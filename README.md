# MammothGPT-V2

Requirements Doc: https://netorg11913131-my.sharepoint.com/:w:/g/personal/blazes_mfc_us/EWWE5urn-CBEs4RNBbuAzXYB0653E0Ax9myeykR0UaeOSg?e=FDkS4d

Freeform Diagram: www.icloud.com/freeform/0d4YLxc4fq2_r01Ww78MH94gg#MammothGPT_Flow_Chart 

Current AI GUI: http://mgpt.pagekite.me 

Current AI Server: ssh://jupiter@mgpt.ddns.net  


In order to optimize MammothGPT we will define THREE different Hugging Face Datasets and determine which creates the best AI system. Please see the .csv files in the "DatasetConfiguration" directory to see which data points should be included in each Hugging Face Dataset. A "2" in a .csv row means that data point should be put in Hugging Face Dataset #2. A "0" means the point data should NOT be included in a Hugging Face Dataset. A "-1" in the "id" column of a .csv row means that the rest of row is example data to display how info is normally defined.  
1) Hugging Face Dataset #1 (Largest with minimal data removed from the web scraping and API inputs) 
2) Hugging Face Dataset #2 (Focused on physical property and location data)
3) Hugging Face Dataset #3 (Focused on previous owner, sales, and value data)


DatasetDocumentation.numbers (and its export to DatasetDocumentation.xls) should act as the final documentation of python code, and NOT how code initially defined. See the .csv files in the "DatasetConfiguration" directory for how code should be defined.
