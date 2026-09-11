import pandas as pd
from datetime import datetime, timedelta
schedule_path = 'schedule.csv'
procure_path = 'procurement.csv'
output_path = '外購混煉膠交期變更通知單.xlsx'
buffer_days = 7
sched = pd.read_csv(schedule_path, dtype=str)
proc = pd.read_csv(procure_path, dtype=str)
# map product to material (same name)
sched['原料料號'] = sched['產品']
merged = pd.merge(sched, proc, left_on='原料料號', right_on='原料料號', how='left')
merged['預計開工日'] = pd.to_datetime(merged['預計開工日'], errors='coerce')
merged['原 ETA'] = pd.to_datetime(merged['原 ETA'], errors='coerce')

def classify(row):
    if pd.isna(row['原 ETA']) or pd.isna(row['預計開工日']):
        return None
    delta = (row['預計開工日'] - row['原 ETA']).days
    if delta < 0:
        return ('提前', -delta, row['原 ETA'] + timedelta(days=delta))
    elif delta > buffer_days:
        return ('延後', delta, row['原 ETA'] + timedelta(days=delta))
    else:
        return None

merged['結果'] = merged.apply(classify, axis=1)
notify = merged.dropna(subset=['結果']).copy()
notify['動作'] = notify['結果'].apply(lambda x: x[0])
notify['差距天數'] = notify['結果'].apply(lambda x: x[1])
notify['建議新到貨日'] = notify['結果'].apply(lambda x: x[2].date())
notify = notify[['製令編號','產品','PO','原 ETA','建議新到貨日','動作','差距天數']]
notify.columns = ['工單號','產品','PO號','原 ETA','建議新到貨日','動作','差距天數']
notify['簽名'] = ''
notify.to_excel(output_path, index=False)
print('done')