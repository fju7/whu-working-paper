# Fresh public-only reconstruction

Date: `2026-09-27`

An isolated directory was created from only the manifest-listed candidate files plus the manifest.
It had no source-repository history or hidden repository context. The following passed:

- 81/81 exact-number entries, six figures, six tables, and required evidence boundaries;
- 84/84 candidate files, exact hashes, paths, links, evidence labels, deny-list checks, and strict
  equality between the physical file tree and declared inventory;
- V3 calibration selection/refit and every consumed-evaluation result from 960/240 released rows;
- every convergence V2 calibration count, baseline, ratio, route-cost value, comparator, and failed
  gate from 1,294 released calibration-only rows and labels;
- V2 holdout commitment, no-authorization/no-result disposition, manifest exclusion, calibration
  result binding, and absence of a holdout-derived paper claim;
- byte-identical rebuild of all six SVG figures, the 81-entry manifest, and manuscript HTML.

Regression injections of each forbidden V2 path failed strict verification when added without being
listed. The final bypass test added an unlisted dual-partition builder carrying the known partition
generation signature; verification failed for the unlisted file, forbidden path, and forbidden
signature.

The source repository's original 49 focused tests also remained `49 passed`; they are not the public
reproduction command.
