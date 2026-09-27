# Release-status verification for fast-moving agent stacks

Use this note when a vendor's blog, documentation, repository, and package registry appear to describe different “current” versions.

## Required distinctions

Keep these states separate:

1. Marketing name or launch announcement.
2. Exact stable release/tag that carries that name.
3. Later stable patches that should be evaluated operationally but not attributed to the original release.
4. Documentation for an unreleased, beta, or future version.

## Verification sequence

1. Find the vendor's official announcement and exact release identifier.
2. Verify the immutable repository tag or release object.
3. Check the repository latest-release endpoint.
4. Check the package registry's `latest` or stable distribution tag.
5. Check exact tags for beta/pre-release collisions or mistaken version numbers.
6. If any source disagrees, state the discrepancy and use the last independently confirmed stable artifact as the comparison baseline.

A published documentation page is not proof that a stable build exists. Do not mix future release notes into a released product comparison.
