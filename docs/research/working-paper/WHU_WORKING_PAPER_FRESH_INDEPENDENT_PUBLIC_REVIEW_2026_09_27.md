# Fresh independent outside-researcher review

Date: `2026-09-27`

Verdict: `PASS` — no material findings in the final candidate.

The reviewer was restricted to the isolated public package and was not given prior gate reports or
adjudications. The central question was whether every published empirical result could be reproduced
and every substantive claim evaluated while verifying, rather than violating, custody of deliberately
unopened evidence—or whether inconvenient dependencies had merely been defined out of scope.

The reviewer independently ran all five documented commands and confirmed:

- all 81 quantitative entries and derived paper artifacts verify and rebuild;
- V3 threshold selection and logistic fitting reproduce on 960 calibration rows, and all published
  metrics reproduce on the 240 released consumed-evaluation rows;
- every published convergence V2 calibration output reproduces from exactly 1,294 calibration-only
  rows and labels;
- no dual-partition builder, original scorer, full V2 seed/partition recipe, full runtime, partition
  manifest, protected label file, or derivation signature is present;
- the V2 calibration-only specification cannot derive the 306-case holdout; and
- an injected unlisted forbidden builder is rejected as an unlisted file, forbidden path, and
  forbidden generation signature.

The reviewer concluded that the final package does not define a result-bearing inaccessible dependency
out of scope and preserves the unopened V2 holdout boundary.
