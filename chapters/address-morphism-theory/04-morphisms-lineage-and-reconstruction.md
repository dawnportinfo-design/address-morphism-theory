# Morphisms, Lineage, and Reconstruction

Address data changes over time. Municipal mergers, street renaming, building
demolition, new entrances, and postal-code changes create lineage rather than
simple replacement.

AMT models these changes as morphisms between versioned address graphs:

```text
G_t -> G_t+1
```

The morphism may preserve, split, merge, deprecate, or supersede a referent.

## Breadcrumb Reconstruction

Breadcrumb storage is useful when it preserves parent-child lineage:

```text
country -> region -> municipality -> locality -> street -> building -> unit
```

However, breadcrumbs are not sufficient by themselves. They need:

- stable node identifiers
- versioned parent edges
- successor links for deprecated nodes
- purpose-specific display rules
- evidence records for reconstruction

The best AGID-compatible model is therefore a versioned address graph with a
breadcrumb projection, not a breadcrumb-only tree.
