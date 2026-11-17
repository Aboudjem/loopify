# QUEUE: hand-backs for the human

- [tick 4] Post the drafted reply on the `fetchAll` rename thread of PR #412
  reason: posting on the PR is above this loop's autonomy level (commit named paths, never post)
  unblock: post the reply below on the thread, then delete this item

      Renamed to `listAll` in 1d7c2aa (3 files). Tests pass, 12/12.

- [tick 5] `e2e` fails in checkout.spec.ts line 88: expected total 42.00, received 41.99
  reason: a real assertion failure in product code, not a flake and not a lint fix
  unblock: fix the rounding in src/cart/total.ts or mark the PR as blocked
