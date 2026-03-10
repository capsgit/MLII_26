import os
from pathlib import Path
import pandas as pd
from ydata_profiling import ProfileReport

os.chdir(Path(__file__).parent)

# 1. read cvs
df = pd.read_csv("./data.csv")

# 2. Create profil
profile = ProfileReport(df)

# 3. Export report to HTML
profile.to_file("data_report.html")