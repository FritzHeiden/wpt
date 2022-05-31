"""Register attribution source for event-level reports."""
import json
from typing import Optional, TypedDict
import uuid

from wptserve.utils import isomorphic_decode, isomorphic_encode


def main(request, response):
  source_event_id = request.GET.get(isomorphic_encode("source_event_id"))
  source_event_id = isomorphic_decode(
      source_event_id) if source_event_id else str(uuid.uuid1().int >> 64)
  source_event = {
      "source_event_id": source_event_id,
      "destination": request.url,
  }
  headers = [("Content-Type", "application/json"),
             ("Attribution-Reporting-Register-Source", json.dumps(source_event))
            ]
  return (200, "OK"), headers, json.dumps({
      "code": 200,
      "message": "Successfully registered source.",
      "headers": headers,
  })
