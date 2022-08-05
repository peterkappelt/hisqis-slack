# %%
from hisqis import get_grades, get_grade_delta
from slack import slack_send_mrkdwn
import time
import os
# %%
old = get_grades()
if "DBG_DUMP_HISQIS" in os.environ:
  old = old[5:]

while True:
  print("Reading data...")
  try:
    new = get_grades()
    if new is None:
      raise Exception("get_grades returned no data")
  except Exception as e:
    print(f"Exception occured, retrying: {e}")
    time.sleep(5)
    continue

  changed_rows = get_grade_delta(old, new)
  for idx, row in changed_rows.iterrows():
    notification_text = (
        f"- *Name:* {row['Prüfungstext']}\n"
        f"- *Status:* {row['Status']}\n"
        f"- *Note:* {row['Note']}\n"
        f"- *Vermerk:* {row['Vermerk']}\n"
        f"- *SWS:* {row['SWS']}"
    )
    slack_send_mrkdwn(notification_text)
    
  old = new
  time.sleep(10 * 60)
# %%
