# F-<number>: <one-sentence claim>

Status: `[OPEN]` | `[RESOLVED]` | `[REFUTED]`
Date: YYYY-MM-DD
Track: fleet | qualcomm | mediatek | soc | laptop | historic | papers

## Claim

State what the firmware *is*, in one falsifiable sentence. Do not describe what
it might be or what you suspect. If the claim is a correction, link the original
claim and add a row to `research/CORRECTIONS.md`.

## Prior art (RULE 0)

Record exact query strings and access dates. Partial overlap is overlap.

| Source | Query | Date | Result |
| --- | --- | --- | --- |
| GitHub code (excluding `adineo-cmd/*`) | | | |
| Web: XDA / LWN / HN / Reddit | | | |
| arXiv / Scholar | | | |
| Kernel + linux-firmware trees | | | |

Verdict: `NEW` | `DELTA <the precise new contribution>` | `PRIOR-ART <urls>`

If prior art covers the claim, close it as a duplicate and record what the prior
art covers. Do not rebuild.

## Evidence

- Device / SoC / partition:
- Reproduction command or script (committed path):
- Measured values (addresses, hashes, versions, constants):
- Evidence class: `[M]` own measurement | `[F]` fact from public source | `[D]` derived

Show the bytes or instruction coverage that prove the claim. A header field is
not proof of an ISA; a disassembly is.

## Falsification chain

What observation would disprove this claim? List the checks already performed
and the remaining ones. An unbroken chain is what makes a finding publishable.

## Negative results

Record hypotheses tested and rejected, with the command/output that rejected
them. `SCOPE.md` calls these results, not noise.

## Open questions

List remaining `[OPEN]` items here and add a pointer to `research/OPEN-QUESTIONS.md`.
Do not silently drop an unresolved sub-question.

## Boundary check

- [ ] No proprietary bytes, decompiled output or device-private data in this file
- [ ] No CVE or exploit content
- [ ] Every number verified by command output
- [ ] Adversarial prior-art audit run (about every 10 findings or per session)
