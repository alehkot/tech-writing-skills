# Safe Example Values

## Use When

Load this reference when a draft contains example domains, addresses, IP addresses, phone numbers, people, organizations, project names, or identifiers, and you need to check whether those values are safe to publish.

## Scope: Illustrative Values Only

- Replace a value only when it is clearly illustrative: an invented sample in a code block, a walkthrough, a screenshot caption, or a table of example inputs.
- When a value may be a real documented literal — a public resolver address, the product's actual domain, a documented support line, a real customer identifier, a registered endpoint — keep it exactly as written and put it on the flagged list as a question for the author. Never substitute a reserved value for a fact.
- Never publish real or plausibly real personal data: a real person's name, email address, phone number, street address, account number, payment detail, credential, or token.
- When you cannot tell whether a value is illustrative or real, flag it. A wrong substitution is a factual error, not a style fix.
- Record every substitution in the report, with the original value and the reserved value that replaced it.

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

- List substituted values under `Changes applied`, and possible real values under `Flagged, not changed`, each with the question the author must answer.
- If a draft needs an example value that no reserved range covers, say so and ask; do not invent one that looks real.

## Attribution

Parts of this reference are adapted from the Google developer documentation style guide (https://developers.google.com/style), used under CC BY 4.0 and modified.
