# %%
import requests
import json
import os
# %%


def slack_send_mrkdwn(mrkdwn):
  requests.post(
      os.environ["SLACK_WEBHOOK"],
      data=json.dumps(
          {"blocks": [
              {
                  "type": "section",
                  "text": {"type": "mrkdwn", "text": mrkdwn}
              }
          ]}
      )
  )
