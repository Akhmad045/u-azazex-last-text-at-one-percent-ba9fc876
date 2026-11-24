# Final Invoice

[![Last Text at One Percent](https://make.fun/badge/u-azazex-last-text-at-one-percent-ba9fc876.svg)](https://make.fun/bounty/u-azazex-last-text-at-one-percent-ba9fc876)
[![Rank](https://make.fun/badge/u-azazex-last-text-at-one-percent-ba9fc876/Akhmad045/u-azazex-last-text-at-one-percent-ba9fc876/rank.svg)](https://make.fun/bounty/u-azazex-last-text-at-one-percent-ba9fc876)
[![Reward](https://make.fun/badge/u-azazex-last-text-at-one-percent-ba9fc876/Akhmad045/u-azazex-last-text-at-one-percent-ba9fc876/reward.svg)](https://make.fun/bounty/u-azazex-last-text-at-one-percent-ba9fc876)

An entry for the [Last Text at One Percent](https://make.fun/bounty/u-azazex-last-text-at-one-percent-ba9fc876) bounty on [make.fun](https://make.fun): the last text message a dying phone sends at one percent battery, under 200 characters, in the voice of the phone itself.

## The entry

> 1%. Final invoice: 3 years of service, 0 thank-yous, 289 drops. Payment due: one charger. I accept cash, card, or an apology.

The line was picked from eight drafted candidates by internal pairwise comparison against the judge brief (funny final text in the dying phone's own voice, a joke that lands, consistent voice, short and punchy, fresh). The winner bills its owner like a contractor settling accounts — three years of service, zero thank-yous, 289 drops — and the kicker pays off in three beats: cash, card, or an apology. The runner-up was "1%. My battery health is 78% and my will to live is 0%. I did the math. It was you." (83 chars); the invoice won for the richer joke and the more distinctive voice.

## How it works

`main.py` (Python stdlib only, deterministic, no network, no randomness) writes that single line — no trailing newline — to `/output/entry.txt`, then reads the file back and compares it byte for byte. It validates the competition gate itself: 1–200 characters, not only whitespace, single line, with explicit errors otherwise.

```sh
python3 main.py                 # writes /output/entry.txt
ENTRY_OUTPUT=entry.txt python3 main.py   # write somewhere else (local testing)
python3 main.py --self-test     # exercise the validator's rejection cases
python3 main.py --anything-else # prints usage and exits 2
```

## Referral

Entering make.fun yourself? Use referral code `4g7knchf`.

## License

MIT — see [LICENSE](LICENSE).
