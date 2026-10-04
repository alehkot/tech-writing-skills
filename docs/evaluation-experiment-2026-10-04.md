# Technical-writing evaluation experiment

The 36 primary assertions were frozen before changes. Three rounds started within a 30-minute limit. No 36/36 success was established.

| Approach | Result |
| --- | --- |
| Source evidence and branch mapping before drafting | 34/36, independent blind review |
| Evidence-adapted templates added | 33/36 automatic; 32/36 after source review, plus a chronology defect |
| Same second candidate with higher reasoning effort | Incomplete: two generation timeouts at 90 seconds |

The first candidate is retained. Three transfer cases (15 assertions) were frozen but not executed, and no confirmation repeat completed. These results do not establish generalization or reliable perfect scores. Original outputs and frozen manifests remain in `workspaces/goal-36-20261004/`.

## Alternative Jev grading

`scripts/grade_with_jev.py` grades saved outputs through the TypeSafe Choice API, preserving original grades and writing separate `.jev.json` files. Live grading of all five first-round answers returned 36/36. Independent blind review scored those same answers 34/36: Jev missed an unsupported shell-prompt outcome and invented absence of options. Preserve this disagreement; do not treat Jev's perfect score as achievement of the goal.

API documentation: https://docs.typesafe.ai/api
