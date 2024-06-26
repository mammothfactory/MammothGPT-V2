# MammothGPT-V2

Requirements Doc: https://netorg11913131-my.sharepoint.com/:w:/g/personal/blazes_mfc_us/EWWE5urn-CBEs4RNBbuAzXYB0653E0Ax9myeykR0UaeOSg?e=FDkS4d

Freeform Diagram: www.icloud.com/freeform/0d4YLxc4fq2_r01Ww78MH94gg#MammothGPT_Flow_Chart 

Current AI GUI: http://mgpt.pagekite.me 

Current AI Server: ssh://jupiter@mgpt.ddns.net  
How to fix [No-IP](https://www.noip.com) should the above dymanic ssh URL stop working: 
 1. Open a terminal inside RealVNC session connected to the Jupiter server, and then run "cd /usr/local/bin" command
 2. Run the "sudo ./noip2 -C" command to reconfigure the No-IP background /usr/local/etc/no-ip2.conf file
 3. Select "wlo1" interface by typing "0" and hitting enter
 4. Use blazes@mfc.us and password saved in MFC BitWarden password manager (or FireFox browser password manager)
 5. Select 5 min update interval by typing "5" and hitting enter
 6. Type "N" and hit enter to not "run something at successful update (y/N)"
 7. Run the "sudo /usr/local/bin/noip2" command to restart No-IP DUC in the background
 8. To check that the No-IP application is running, run the "ps aux | grep noip2" command

<br><br><br>
In order to optimize MammothGPT we will define THREE different Hugging Face Datasets and determine which creates the best AI system. Please see the .csv files in the "DatasetConfiguration" directory to see which data points should be included in each Hugging Face Dataset. A "2" in a .csv row means that data point should be put in Hugging Face Dataset #2. A "0" means the point data should NOT be included in a Hugging Face Dataset. A "-1" in the "id" column of a .csv row means that the rest of row is example data to display how info is normally defined.  
1) Hugging Face Dataset #1 (Largest with minimal data removed from the web scraping and API inputs): See CompleteDataSet.py
2) Hugging Face Dataset #2 (Focused on physical data, such as property details and location data):   See PhysicalDataSet.py 
3) Hugging Face Dataset #3 (Focused on finance data, sush as previous owner, sales, and value data): See FinanceDataSet.py


DatasetDocumentation.numbers (and its export to DatasetDocumentation.xls) should act as the final documentation of python code, and NOT how code initially defined. See the .csv files in the "DatasetConfiguration" directory for how code should be defined.

Make sure you create a Hugging Face User Access Token to run the FinanceDataSet.py scripts 
https://huggingface.co/settings/tokens

<br><br><br>

Our Python virtual enviroment was setup and can be recreated using the following commands:
python3 -m venv .venv 
pip freeze > requirements.txt
pip install -r requirements.txt
