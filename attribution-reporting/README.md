# Attribution Reporting tests.

Tests for the
[Event-level reports API](https://github.com/WICG/conversion-measurement-api/blob/main/EVENT.md)
and
[Aggregatable reports API](https://github.com/WICG/conversion-measurement-api/blob/main/AGGREGATE.md).
Please refer to
[this](https://docs.google.com/document/d/1Knot4w5JJZEdGCfjO9gwafbli0J6FIaVhAKy0ZxfZzs/edit?resourcekey=0--2ILmhGk95CvpM4lqq8J3Q#heading=h.lldt5vlxjhnx)
for the server support design.

## Contributing

1.  You need to add all the tests to the the attribution reporting folder.
2.  You need to make a POST request to
    `/.well-know/attribution-reporting/report-event-attribution` for event-level
    and `/.well-known/attribution-reporting/report-aggregate-attribution` for
    aggregatable reports with body `{"clear_stash": true}`. This is necessary to
    avoid any pollution in the server-side stash.
3.  All the report code is in `/.well-known/` directory since reports are posted
    to a fixed route by the browser.
4.  The APIs add noise and delay to the reports by default. To disable this,
    additional command line arguments need to be passed. For this reason, all
    the attribution reporting tests are virtual and the real tests are skipped.
