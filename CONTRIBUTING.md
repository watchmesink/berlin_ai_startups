# Contributing

This repository is a hand-verified Berlin AI company directory plus a Germany-eligible AI/ML Product Manager jobs tracker. Please keep those two lists distinct.

## Berlin directory (`README.md`)

A useful company PR includes:

1. The company website and evidence of a Berlin headquarters, office, or substantial operating team.
2. Evidence that AI/ML is core to the product (not a consultancy engagement, agency, or research project).
3. A Seed-or-later announcement, or equivalent maturity (bootstrapped scaleup, corporate-backed product company, public company).
4. A recent activity signal (2025–26 funding, product news, hiring, or operating team).
5. Sources for team size, latest disclosed financing, and open roles.

Do not add pre-seed-only startups, stealth companies, absorbed product brands, or companies that have left Berlin.

**Ownership changes:** list the company only if a distinct product, brand, and Berlin operation remain (see the exceptions under Explicit exclusions in the README). Uncompleted deals stay listed until they close.

Openings counts on global ATS boards are worldwide totals unless the URL is location-filtered. Prefer a first-party careers URL over a LinkedIn keyword search.

## Jobs tracker (`AI_PM_ROLES_IN_GERMANY.md`)

Include a role when:

- it is live on the employer’s own careers site,
- the location signal is Berlin, Germany, Europe/EMEA remote, or genuinely global remote,
- the employer is past pre-seed or is an established bootstrapped, corporate-backed, or public company,
- the work can be done without relocating away from Berlin/Germany.

The employer does **not** need to be in the Berlin directory. Public companies, international firms with a Germany-eligible seat, and occasional investor or services employers with a product role are in scope here.

## When a company is in both files

Copy the same website URL and the same `👥 · 💰 · 💼` line into both files. `python scripts/check.py` fails the PR if they drift.

After adding or removing roles, update:

- the jobs-file intro (`N roles across M companies`), and
- the README “Also in this repo” table.

## Checks

Run locally before opening a PR:

```bash
python scripts/check.py
```

Use the issue templates for additions, corrections, dead links, and new PM roles.
