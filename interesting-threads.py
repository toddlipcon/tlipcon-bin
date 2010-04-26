#!/usr/bin/env python

import sys
import re

trace = sys.stdin.read()

trace_stanzas = trace.split("\n\n")
header = trace_stanzas[0]
del trace_stanzas[0]

BORING_REGEXES = [
  re.compile("""
"IPC Server handler \d+ on \d+" daemon prio=\d+ tid=\S+ nid=\S+ waiting on condition \[\S+\]
   java.lang.Thread.State: WAITING \(parking\)
\s+at sun.misc.Unsafe.park\(Native Method\)
\s+- parking to wait for  <\S+> \(a java.util.concurrent.locks.AbstractQueuedSynchronizer\$ConditionObject\)
\s+at java.util.concurrent.locks.LockSupport.park\(LockSupport.java:\d+\)
\s+at java.util.concurrent.locks.AbstractQueuedSynchronizer\$ConditionObject.await\(AbstractQueuedSynchronizer.java:\d+\)
\s+at java.util.concurrent.LinkedBlockingQueue.take\(LinkedBlockingQueue.java:358\)
\s+at org.apache.hadoop.hbase.ipc.HBaseServer\$Handler.run\(HBaseServer.java:\d+\)
""".strip()),
  re.compile("""
"\d+@qtp\d+-\d+ - Acceptor\d+ SelectChannelConnector@\d+.\d+.\d+.\d+:\d+" prio=\d+ tid=\S+ nid=\S+ runnable \[\S+\]
   java.lang.Thread.State: RUNNABLE
\\s+at sun.nio.ch.EPollArrayWrapper.epollWait\(Native Method\)
\\s+at sun.nio.ch.EPollArrayWrapper.poll\(EPollArrayWrapper.java:\d+\)
\\s+at sun.nio.ch.EPollSelectorImpl.doSelect\(EPollSelectorImpl.java:\d+\)
\\s+at sun.nio.ch.SelectorImpl.lockAndDoSelect\(SelectorImpl.java:\d+\)
\\s+- locked <\S+> \(a sun.nio.ch.Util\$\d+\)
\\s+- locked <\S+> \(a java.util.Collections\$UnmodifiableSet\)
\\s+- locked <\S+> \(a sun.nio.ch.EPollSelectorImpl\)
\\s+at sun.nio.ch.SelectorImpl.select\(SelectorImpl.java:\d+\)
\\s+at org.mortbay.io.nio.SelectorManager\$SelectSet.doSelect\(SelectorManager.java:\d+\)
\\s+at org.mortbay.io.nio.SelectorManager.doSelect\(SelectorManager.java:\d+\)
\\s+at org.mortbay.jetty.nio.SelectChannelConnector.accept\(SelectChannelConnector.java:\d+\)
\\s+at org.mortbay.jetty.AbstractConnector\$Acceptor.run\(AbstractConnector.java:\d+\)
\\s+at org.mortbay.thread.QueuedThreadPool\$PoolThread.run\(QueuedThreadPool.java:\d+\)
""".strip()),

  re.compile("""
"Gang worker#\d+ \(Parallel (GC|CMS) Threads\)" prio=10 tid=\S+ nid=\S+ runnable 
""".strip()),
  re.compile("""
"IPC Client \(\d+\) connection to /\d+.\d+.\d+.\d+:\d+ from an unknown user" daemon prio=10 tid=\S+ nid=\S+ in Object.wait\(\) \[\S+\]
\s+java.lang.Thread.State: TIMED_WAITING \(on object monitor\)
\s+at java.lang.Object.wait\(Native Method\)
\s+- waiting on \<\S+\> \(a org.apache.hadoop.hbase.ipc.HBaseClient\$Connection\)
\s+at org.apache.hadoop.hbase.ipc.HBaseClient\$Connection.waitForWork\(HBaseClient.java:\d+\)
\s+- locked <\S+> \(a org.apache.hadoop.hbase.ipc.HBaseClient\$Connection\)
\s+at org.apache.hadoop.hbase.ipc.HBaseClient\$Connection.run\(HBaseClient.java:\d+\)
""".strip()),
  re.compile("""
"VM Thread" prio=\d+ tid=\S+ nid=\S+ runnable 
""".strip()),
  re.compile("""
"VM Periodic Task Thread" prio=\d+ tid=\S+ nid=\S+ waiting on condition 
""".strip()),
  re.compile("""
"Low Memory Detector" daemon prio=10 tid=\S+ nid=\S+ runnable [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE
""".strip()),
  re.compile("""
("CompilerThread\d+"|"Signal Dispatcher"|"Surrogate Locker Thread \(CMS\)"|"Low Memory Detector"|"DestroyJavaVM"|"Attach Listener") (daemon )?prio=10 tid=\S+ nid=\S+ (waiting on condition|runnable) \[0x0000000000000000\]
   java.lang.Thread.State: RUNNABLE
""".strip()),

]

for s in trace_stanzas:
  matched = False
  for r in BORING_REGEXES:
    if re.search(r, s):
      matched = True
      break
  if matched: continue
  print s
  print
  print
