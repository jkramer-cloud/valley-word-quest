# Valley Word Quest — Daily Dash (v1.1)

A fully client-side, mobile-friendly daily word-guessing game for grades **3–12**, designed for educational use on PlayForge.

Play: https://jkramer-cloud.github.io/valley-word-quest/

## v1.1 — One successful solve per day

- Each grade still receives its own daily word, with the same deterministic word schedule and original dictionary.
- Students can choose or change grades before solving a word. Unfinished work is saved per grade and local nickname.
- A successful solve locks *all ten grades* until midnight Pacific Time (America/Los_Angeles). Both physical and onscreen keyboard, hint, grade, profile switch and reset controls are blocked for further play. The result, calendar, achievements and sharing remain available.
- Exhausting attempts on a grade without solving does **not** trigger the global completion lock. Students may choose another grade until one word is solved. The exhausted grade cannot be replayed that day.
- The lock is shared by all local nicknames in the same browser; switching profiles or resetting old history cannot bypass it. This intentionally applies to the browser rather than a named student: students sharing the same browser storage also share the daily allowance.
- Existing same-day wins from v1.0 are recognized upon upgrade, including wins under other local nicknames. The lock remains separate from historical records. Old grade-level progress and achievements are retained; historical reset now preserves today's record and is disabled during the lock.
- Open tabs check local storage and the date, including on storage notifications and before gameplay input. On reopening, a completed grade's result is restored for its original local nickname.
- A completion banner and a Return to PlayForge link encourage students to move on.
- Existing seasonal themes, grade-specific achievements, calendar, audio preferences, contrast and motion settings are preserved.

## Update the existing GitHub Pages repository

1. Extract the **Valley-Word-Quest-v1.1-Update.zip** file.
2. Open `jkramer-cloud/valley-word-quest` on GitHub.
3. Replace the root `index.html`, `game.js`, and `README.md` with the supplied files.
4. Leave the existing `styles.css`, `word-bank.js`, optional `build_words.py`, and all other repository files intact. This ZIP is an update containing the complete replacements for the three changed files, not a standalone installation.
5. Commit to the publishing branch (`main`); leave the existing GitHub Pages settings unchanged.
6. Once deployed, hard-refresh the game (Ctrl+Shift+R on Windows/Chromebooks). Verify that completing one word disables the grade menu and that returning to the game on the same device does not permit more guesses.

The PlayForge card and game URL are unchanged; no Hub update is necessary. **Do not upload these files to the Hub repository.**

## Rules and features

- Grades 3–4 get 4 letters, 5–6 get 5, 7–8 get 6, 9–10 get 7, and 11–12 get 8.
- Same grade + same Pacific calendar date = same answer. The existing calendar-year shuffle and holiday answer overrides are unchanged.
- Word banks: 5,709 grade-assigned answers (3,589 unique words) and 85,462 allowed spelling entries across lengths 4–8. Each grade has at least 392 eligible year-round answers plus seasonal overrides. Answers are selected from high-frequency dictionary entries, with a school-oriented exclusion list. Corpus frequency is not a formal readability rating; vocabulary suitability should still be reviewed for the intended age group.
- Daily attempt limits: 7 (grades 3–4), 6 (grades 5–8), 7 (grades 9–12). No retry after finishing a grade's date-specific puzzle.
- Streaks require consecutive calendar days with wins at the same grade. A loss breaks that grade's streak. Grade-specific wins, best time, win rate, achievement badges and shareable results are stored per local nickname.
- Timer starts with the first typed letter and pauses if the page is hidden. The timer is restored on reload. Optional one-time first-letter hint adds 30 seconds.
- Calendar shows previous results without enabling replay or future puzzles.
- Seasonal themes include spring, summer, autumn, winter, Halloween, harvest/Thanksgiving, Jan 1, Feb 14, Pi Day, Earth Day, summer solstice, back-to-school, winter solstice.
- Sound is off by default. Reduced motion and high-contrast tiles are available.

## Privacy and limitations

- No personal information is transmitted by the game. Nicknames, puzzle history, and completion lock are stored only in this browser using `localStorage`. Profiles are not password-protected. Use non-identifying nicknames rather than student names.
- The daily lock is not synchronized between devices, browser profiles, or private browsing sessions. Clearing browser data, manipulating local storage, changing the system clock, or using another browser/device can bypass it. This is a classroom convenience, not a secure anti-cheating mechanism. Server-enforced school-account limits would require an approved backend and authentication design.
- The new Pacific time boundary matches Sudoku Quest. Existing Washington-based device histories remain compatible; histories from devices using other time zones retain their original saved date labels.
- Calendar results are summaries only. The optional Google Fonts used in the original stylesheet require internet access to load; system font fallbacks are retained. No npm, API key or build server is needed.

## Validation

The reconstructed v1.0 index, game script, stylesheet, and word bank were checked against the corresponding live GitHub blob hashes. The original stylesheet and word bank are unchanged. The v1.1 script passed JavaScript syntax checks and automated Chromium interface tests with simulated browser storage: all ten grade levels, unfinished puzzle persistence, loss without global lock, success with global lock, grade/profile/reset guards, existing-win migration, reload history, simulated storage events, Pacific-midnight rollover, and mobile width. Actual GitHub Pages deployment and Chromebook persistent storage still require classroom verification.

## Source and word bank customization

`word-bank.js` is generated by `build_words.py` using frequency data from TextBlob `en-spelling.txt` (based on public-domain Gutenberg books plus word-frequency sources) and its `en-lexicon.txt` (Brill-tagged lexicon and later additions). Guess validation also uses entries from the CMU Pronouncing Dictionary. TextBlob corpus and lexicon notices: https://textblob.readthedocs.io/ ; CMUdict: https://github.com/cmusphinx/cmudict . Review license and attribution before redistribution beyond the classroom.

To regenerate the word-bank files locally, Python needs `textblob` and `cmudict`; the game itself does not require them. To adapt vocabulary, edit `build_words.py` or manually change grade arrays in `word-bank.js`. Holiday answer pools are at `window.VWQ_WORDS.holidays`. Avoid changing the answer lists during a school year, because doing so may change earlier answers for the same grade/date. For future expansion, use a versioned algorithm or stable year-specific answer schedules.

## Repository files

- `index.html` — game layout, dialogs, calendar, accessible controls and completion banner.
- `styles.css` — responsive theme, tile and achievement animations (unchanged).
- `game.js` — deterministic daily word, feedback, persistence, daily lock, profiles, streaks, themes and timer.
- `word-bank.js` — bundled dictionary (unchanged).
- `build_words.py` — optional word-bank generation script (unchanged).

Created October 2026 for classroom learning use. Updated November 18, 2026.
