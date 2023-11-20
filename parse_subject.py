import re

compiled = re.compile(r"Your requested ([\w ()]+) data file is ready for download.")

"""
<p>Please follow the link below to download your Financial
 Transparency Dashboard (district overview) file for State
wide, school year 2021-22:</p>
<p><a href="https://downloads.mischooldata.org/GeneratedDa
taFile?filename=c8a4eef5-c9b3-4405-abbb-0e18958adcf1.csv">
https://downloads.mischooldata.org/GeneratedDataFile?filen
ame=c8a4eef5-c9b3-4405-abbb-0e18958adcf1.csv</a></p>
<p>This data file will expire after 72 hours.</p>
<p>Technical Assistance</p>
<p>For a definition of the column headers, go to the <a hr
ef="http://www.michigan.gov/documents/cepi/K12DataFileLayo
uts_wdescription_526277_7.xls">Data File Layout</a> docume
nt.</p>
"""

para = """
Please follow the link below to download your Financial Transparency Dashboard (district overview) file for State wide, school year 2021-22:
"""

result = re.search(r"[\w ,']+([0-9]{4}-[0-9]{2}):", para)

print(result.groups()[0])
