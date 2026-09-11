import pandas as pd
path = r"C:\\Users\\njkpr\\OneDrive\\OPENCODEGITHUB\\schedule-sync\\外購混煉膠交期變更通知單.xlsx"
df = pd.read_excel(path)
print(df.head().to_string(index=False))