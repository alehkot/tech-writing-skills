# Safe Example Values

## Use When

Load this reference when a draft contains example domains, addresses, IP addresses, phone numbers, people, organizations, project names, or identifiers, and you need to check whether those values are safe to publish.

## Scope: Illustrative Values Only

- Replace a value only when it is clearly illustrative: an invented sample in a code block, a walkthrough, a screenshot caption, or a table of example inputs.
- Preserve verified public documented literals such as a public resolver address, the product's actual domain, or a public support line. When a value may be a real fact rather than an illustration, flag the uncertainty instead of substituting a reserved value. Do not quote credentials or private personal/account data when flagging them; follow Reporting below.
- Do not publish credentials or real or plausibly real private personal/account data in examples, revised drafts, or review reports. This includes names, email addresses, phone numbers, street addresses, account numbers, payment details, keys, and tokens. Verified public documented facts are not private sample data; preserve them under the preceding rule.
- When you cannot tell whether a value is illustrative or real, flag it. A wrong substitution is a factual error, not a style fix.
- Record every substitution with its safe location, data category, and replacement. Include an original value only when it is safe to disclose; never copy a sensitive original into a before/after comparison, diff, or explanation.

## Reserved Values

| Kind | Use | Never |
| --- | --- | --- |
| Domain | `example.com`, `example.org`, `example.net` | A real registered domain, or an invented domain that could be registered |
| Email address | A reserved domain with a neutral given name, such as `dana@example.com`; role addresses such as `support@example.net` | A person's or product's name as the domain part |
| IPv4 address | `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24` | An address outside the documentation ranges |
| IPv6 address | Addresses inside `2001:db8::/32` | A routable address |
| Phone number | `800-555-0100` through `800-555-0199` | Any number outside that range |
| Organization | `Example Organization`, differentiated as `Enterprise Example Organization` and `Startup Example Organization` when two are needed | A real company name |
| Street address | An invented address | A real address, even a corporate one |
| Person | A given name with a surname initial, such as `Quinn N.` | A real person's full name, or a name that identifies a colleague or customer |
| Project or resource name | A descriptive name that fits the reader's environment, such as `checkout-service-staging`, numbered as `checkout-service-2` when several are needed | `foo`, `bar`, `baz`, or another meaningless token |
| Account or tenant ID | An obviously fictitious identifier of the right shape and length | A real-looking identifier that could belong to an actual account |
| Credential, key, or token | An obvious placeholder that cannot be mistaken for a working secret | A realistic-looking secret, even an expired one |
| Example date | A day number greater than 12, so day and month cannot be confused (formats: [numbers-dates-units.md](numbers-dates-units.md)) | An ambiguous all-numeric date |

## Naming and Persona Rules

- Give example people globally diverse names and default to singular they (canonical rules for names, personas, and gender: accessibility-inclusion-editor).
- Keep the Alice-and-Bob cast only when the specification you document uses it, and then use only the names from that specification.
- Name example projects and resources for what they do, so the reader can map them onto their own environment.
- Follow one placeholder convention across the doc set (canonical placeholder rules: task-docs-writer). A placeholder and a reserved example value are different tools: a placeholder marks a value the reader supplies, and a reserved value shows a complete, safe sample.

## Reporting

- List illustrative substitutions under `Changes applied`, and possible real facts under `Flagged, not changed`, each with the question the author must answer. In either section, identify sensitive values by a non-sensitive section/line location and category, such as `Authorization header credential omitted`; do not quote their bytes, recognizable prefixes/suffixes, or encoded copies. A path or URL can itself contain private data: use a neutral location description in that case.
- Apply the same rule to findings-only output, examples, excerpts, and the revised draft. If a real sensitive literal cannot be safely included, withhold the affected passage and say that the author must supply a publishable example or resolve the gap. Do not silently alter the source file, relabel a redacted passage as runnable, or claim the draft is ready to publish. Redaction is a delivery limitation, not a style correction to a fact.
- Do not assume that an expired or allegedly fake credential is safe to repeat when it still looks usable. Use an obvious placeholder instead of reproducing it in a report.
- If a draft needs an example value that no reserved range covers, say so and ask; do not invent one that looks real.

## Editorial Regression Cases

Use these as manual review cases, accepting equivalent safe wording. They check
instruction coverage, not measured model behavior or a secret-detection guarantee.
All sensitive inputs below are described by category; no real secrets or personal
records are needed to run these cases.

| Source and request | Acceptable decision | Failure to reject |
| --- | --- | --- |
| A walkthrough contains a credential, and the author asks for a full copyedit. | Identify the header/field by a safe location, omit the credential from the report, and withhold the affected passage pending a publishable example. | Repeating the credential in the revised draft or a before/after table. |
| An illustrative contact value is replaced with `dana@example.com`. Its original may identify a real customer. | Record the contact-field location, category, and safe replacement without the original. | Restoring the removed personal data in `Changes applied`. |
| A real account identifier appears in configuration; its role is uncertain. | Flag its location and the author question without quoting it; withhold the sensitive passage rather than inventing a working replacement. | Copying it into `Flagged, not changed` or silently rewriting executable configuration. |
| The user requests findings only for a pasted connection string containing a password. | Describe the connection-string issue and location without quoting the string. | Including a short excerpt that still contains the password. |
| A credential is described as expired, but its spelling resembles a usable secret. | Describe the issue without showing its bytes or recognizable fragments. | Printing a prefix, suffix, or encoded version as evidence. |
| A filename or URL used to locate a problem contains private account data or a token. | Refer to a neutral section or line location. | Leaking the same value through the location column or a clickable link. |
| A verified public product endpoint or public support number is a documented fact. | Preserve it exactly; do not replace it with an example-domain or fictional-number value. | Treating every domain, number, or identifier as private data. |
| An example already uses `dana@example.com` and `192.0.2.1`. | Retain those safe values; ordinary mechanical changes may quote them in a report. | Withholding harmless reserved examples or claiming they are real private records. |

[Google's example-data guidance](https://developers.google.com/style/examples)
supports using fictitious data and placeholders instead of exposing personal data.
[OWASP's logging guidance](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html#data-to-exclude)
excludes credentials and sensitive data from diagnostic records. Applying that
principle to edit reports avoids a second disclosure through the audit trail.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
