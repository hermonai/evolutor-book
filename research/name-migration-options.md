# Name migration options

## Option A - Invert the brands immediately

Use DOGMA for Transformer DNA and Hermon DNA for non-Transformer work now.

Risk: historical papers, measured artifacts, package names, and engines would appear to support the wrong architecture. Rejected during bootstrap.

## Option B - Keep historical names forever

Keep DOGMA recurrent and Hermon transformer-oriented.

Benefit: minimal confusion in existing artifacts. Cost: does not follow the intended target taxonomy.

## Option C - Qualified transition, then explicit migration

Use DOGMA-R / Hermon Engine for historical/current artifacts and DOGMA-T / Hermon DNA-R for target branches. Require a migration RFC before unqualified public names.

**Recommendation: Option C.** It respects the intended direction without corrupting provenance.

## Migration RFC requirements

- repository and package mapping;
- model/config/checkpoint architecture IDs independent of brand names;
- data and checkpoint compatibility matrix;
- claims-to-artifacts map;
- documentation redirects and deprecation period;
- artifact metadata schema with `architecture_family`, `architecture_version`, and `lineage_name`;
- explicit statement that historical results are not transferred.

Until then, book prose always qualifies the four names.

