# Task Execution Lifecycle

Initial supported states:

`pending -> running -> completed`

`pending -> running -> failed`

`pending -> cancelled`

`running -> cancelled`

`running -> waiting_approval` and approval-resumption transitions are planned but not implemented yet.

The API currently validates transitions but does not execute workflows or agents. A future worker/orchestrator will own execution and update task state through a controlled service interface.
