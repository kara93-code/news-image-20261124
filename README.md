# Tuesday 24 November 2026 — the world in one picture

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/kara93-code/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/kara93-code/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Final round of the blind rounds: a rebuilt broadsheet for Tuesday
24 November 2026, in the style of the news-image-20261125 entry.
A blue serif masthead, a red date line and a six-point UTC timeline
open the page; three illustrated leads follow — COP31 ending in
deadlock in Antalya, the candy-factory fire in Banten, 25 sailors
dead near the Strait of Hormuz — then nine numbered cards, twelve
more stories in "Also on Tuesday", and a date-check footer that keeps
out what is not from today (the AFCON final was 18 January, the
oil-gas bill rose in October, the chess ceremony was Sunday).

The image is drawn with Pillow by `draw.py` into `assets/entry.png`;
`main.py` (Python 3.13, standard library only) validates the PNG
chunk by chunk and copies it to `/output/entry.png`. The program runs
with no network and writes identical bytes on every run.
