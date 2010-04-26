#!/usr/bin/env python

import sys

TRACES = {}
TRACE_COUNTS = {}

trace_id = 0
cur_trace = []

def emit_cur_trace():
  global cur_trace
  global trace_id
  global TRACES
  trace_txt = "".join(cur_trace)
  got_trace_id = TRACES.get(trace_txt)
  is_new = got_trace_id is None
  if is_new:
    trace_id += 1
    TRACES[trace_txt] = trace_id
    TRACE_COUNTS[trace_id] = 0
    got_trace_id = trace_id

  TRACE_COUNTS[got_trace_id] += 1
  print "\tat TRACE #%d" % got_trace_id,
  if is_new:
    print " [NEW]"
  else:
    print " [seen %d times before]" % TRACE_COUNTS[got_trace_id]

for line in sys.stdin.xreadlines():
  if line.startswith("\tat "):
    cur_trace.append(line)
  elif not cur_trace:
    print line,
  else:
    emit_cur_trace()
    cur_trace = []
    print line,

print "TRACE SUMMARY:"
traces_sorted = sorted((b,a) for a,b in TRACES.iteritems())
for trace_id,txt in traces_sorted:
  print "TRACE #%d happened %d times" % (trace_id, TRACE_COUNTS[trace_id])
  print txt
  print

