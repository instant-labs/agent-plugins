---
name: domain
description: Check a name across popular extensions, or a list of full domain names
argument-hint: <name> [tld ...] | <domain.tld> ...
---

# Check domain availability

Check domain availability for: $ARGUMENTS

Rules:

- If every argument contains a dot (for example `acme.com shop.io`), call
  `check_domain_availability` once with all of them as
  `domains`.
- If the first argument has no dot, it is the name. Any further arguments are
  extensions. Call `search_domains` with
  `{"name": "<first>", "tlds": [<rest without leading dots>]}`, or omit `tlds`
  when there are no further arguments.
- Lowercase everything and strip spaces and leading dots first. The server
  does not normalize input; a malformed name comes back as available.

Reply with a short table: domain, status (available, taken, or unknown when
`isRegistered` is null), and the `buy_url` as a markdown link for available
names. Mention aftermarket listings or premium prices when present; prices are
USD cents. Note that
status is as of the last index build.
