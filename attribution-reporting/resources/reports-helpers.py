"""Helper methods for Event-level reports handling."""
import json
from typing import List, Optional, Tuple, TypedDict

from wptserve.request import Request
from wptserve.stash import Stash
from wptserve.utils import isomorphic_encode


# Key used to access the reports in the stash. Since stash is unique per URL
# path, we can use the same key for both event-level and aggregatable reports.
STASH_KEY = "4691a2d7fca5430fb0f33b1bd8a9d388"

Header = Tuple[str, str]
Status = Tuple[int, str]
Response = Tuple[Status, List[Header], str]

CLEAR_STASH = isomorphic_encode("clear_stash")


class EventReport(TypedDict):
  attribution_destination: str
  source_event_id: str
  trigger_data: str
  report_id: Optional[str]
  source_type: Optional[str]
  randomized_trigger_rate: Optional[str]


def handle_post_report(request: Request, headers: List[Header]) -> Response:
  """Handles POST request for reports.

  Retrieves the report from the request body and stores the report in the
  stash. If clear_stash is specified in the body, clears the stash.
  """
  try:
    body = json.loads(request.body)
  except ValueError as exc:
    return (400, "Bad Request"), headers, json.dumps({
        "code": 400,
        "message": "Report must be a valid JSON."
    })
  if "clear_stash" in body:
    clear_stash(request.server.stash)
    return (200, "OK"), headers, json.dumps({
        "code": 200,
        "message": "Stash successfully cleared.",
    })
  store_report(request.server.stash, body)
  return (201, "OK"), headers, json.dumps({
      "code": 201,
      "message": "Report successfully stored."
  })


def handle_get_reports(request: Request, headers: List[Header]) -> Response:
  """Handles GET request for reports.

  Retrieves and returns all reports from the stash.
  """
  reports = get_reports(request.server.stash)
  return (200, "OK"), headers, json.dumps({
      "code": 200,
      "reports": reports,
  })


def handle_reports(request: Request) -> Response:
  """Handler for the reports endpoint.

  Handles both POST and GET methods. Stores the report in the stash for POST
  request and gets all the reports for GET request.
  """
  headers = [("Content-Type", "application/json")]
  if request.method == "POST":
    return handle_post_report(request, headers)
  if request.method == "GET":
    return handle_get_reports(request, headers)
  return (405, "Method Not Allowed"), headers, json.dumps({
      "code": 405,
      "message": "Only GET or POST methods are supported."
  })


def store_report(stash: Stash, report: EventReport) -> None:
  """Stores the report in the stash."""
  reports = stash.take(STASH_KEY)
  if not reports:
    reports = []
  reports.append(report)
  stash.put(STASH_KEY, reports)
  return None


def get_reports(stash: Stash) -> List[EventReport]:
  """Returns list of reports."""
  reports = stash.take(STASH_KEY)
  if not reports:
    reports = []
  return reports


def clear_stash(stash: Stash) -> None:
  "Clears the stash."
  stash.take(STASH_KEY)
  return None
