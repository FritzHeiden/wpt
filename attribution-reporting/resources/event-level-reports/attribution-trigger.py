"""Returns trigger data for source attribution."""
import json


def main(request, response):
  headers = [("Content-Type", "application/json"),
             ("Attribution-Reporting-Register-Event-Trigger",
              json.dumps([{
                  "trigger_data": "2"
              }]))]
  return (200, "OK"), headers, json.dumps({
      "code": 200,
      "message": "Attribution trigger.",
      "headers": headers
  })
