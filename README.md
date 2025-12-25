# Crowding-Out Experiment

## Testing How Incentive Structures Affect Intrinsic Motivation

A behavioral economics experiment built with **oTree** (Python) investigating whether target-based bonuses crowd out intrinsic motivation more than piece-rate incentives.

## Research Question

**Does a target-based Individual Bonus crowd out intrinsic motivation more than a general Piece Rate incentive?**

This experiment tests a core prediction from motivation crowding theory (Deci & Ryan): that controlling incentives undermine intrinsic motivation more than informational incentives of equivalent expected value.

## Experimental Design

### Structure: Within-Subjects with Counterbalancing

| Phase | Duration | Payment | Purpose |
|-------|----------|---------|---------|
| **Phase 1: Baseline** | 5 min | None | Measure baseline intrinsic motivation |
| **Phase 2: Treatment A** | 5 min | Piece Rate OR Bonus | First incentivized period |
| **Phase 3: Post-Treatment A** | 3 min | None | Measure crowding-out effect |
| **Phase 4: Treatment B** | 5 min | Bonus OR Piece Rate | Second incentivized period |
| **Phase 5: Post-Treatment B** | 3 min | None | Measure crowding-out effect |

### Treatment Conditions

**Piece Rate (Non-controlling)**
- €0.20 per correct word found
- General performance reward

**Individual Bonus (Controlling)**
- €3.00 if participant finds 12+ words
- €0.00 if fewer than 12 words
- Target-based, all-or-nothing reward

### Counterbalancing
- Group 1 (n=6): Piece Rate first → Bonus second
- Group 2 (n=6): Bonus first → Piece Rate second

## The Task: Word Puzzle

Participants find words in a 4×4 letter grid:
- Words must be 4+ letters
- Adjacent letters only (horizontal, vertical, diagonal)
- Each cell used once per word
- Valid English dictionary words only

```
S  T  R  A
E  P  O  L
I  N  T  E
D  S  E  R
```

## Hypotheses

**H1 (Primary):** Post-incentive performance will decline more after the Individual Bonus treatment compared to the Piece Rate treatment.

**H2 (Mechanism):** Participants will report lower perceived autonomy and task enjoyment after the Bonus treatment.

**H3 (Order effects):** The crowding-out effect should persist regardless of treatment order.

## Technical Implementation

### Built With
- **oTree** — Python framework for behavioral experiments
- **Python 3** — Backend logic, data models, payment calculations
- **JavaScript** — Real-time puzzle interface, timer, word validation
- **HTML/CSS** — Responsive UI templates
- **JSON** — Word grids and configuration

### Project Structure
```
crowding_out/
├── __init__.py              # Data models, pages, game logic
├── Consent.html             # Informed consent
├── Instructions.html        # Task explanation
├── Practice.html            # Practice round
├── Phase1-5.html            # Main experiment phases
├── Questionnaire2/4.html    # Post-treatment surveys
├── FinalQuestionnaire.html  # Demographics & debrief
├── Payment.html             # Earnings display
└── _static/
    ├── styles.css           # UI styling
    ├── puzzle.js            # Word puzzle logic
    └── word_grids.json      # Letter grids for each phase
```

### Key Features
- **Automatic counterbalancing** — Treatment order assigned at session creation
- **Real-time validation** — Immediate feedback on word submissions
- **Timed phases** — Automatic progression with countdown timer
- **Payment calculation** — Dynamic earnings based on performance
- **Data export** — All responses captured for analysis

## Measured Variables

### Performance Data (automatic)
- Words found per phase
- % change from baseline
- Within-person treatment difference

### Questionnaire Data
- Perceived autonomy (7-point Likert)
- Task enjoyment (7-point Likert)
- Payment preference
- Demographics

## Running the Experiment

### Prerequisites
```bash
pip install otree
```

### Local Development
```bash
otree devserver
```
Then open http://localhost:8000

### Create Session
1. Go to http://localhost:8000/demo
2. Click "Crowding Out Experiment"
3. Start session with desired number of participants

## Analysis Plan

### Primary Analysis
- **Paired t-test** comparing post-Bonus vs post-Piece-Rate performance
- **Effect size** (Cohen's d) for within-person differences

### Secondary Analysis
- **Mixed ANOVA** with treatment (within) × order (between)
- **Correlation** between autonomy ratings and performance drops

## Theoretical Background

This experiment extends classic motivation crowding research:

- **Gneezy & Rustichini (2000):** "Pay Enough or Don't Pay at All" — small payments can be worse than no payment
- **Frey & Jegen (2001):** Controlling vs. informational incentives have different motivational effects
- **Deci & Ryan (1985):** Self-Determination Theory — autonomy is a basic psychological need

**Key insight:** We test whether *structure* of payment (controlling bonus vs. non-controlling piece rate) matters, holding expected value constant.

## Skills Demonstrated

| Skill | Application |
|-------|-------------|
| **Python** | oTree backend, data models, session logic |
| **JavaScript** | Interactive puzzle interface, real-time validation |
| **Experimental Design** | Within-subjects, counterbalancing, power analysis |
| **Behavioral Economics** | Motivation theory, incentive design |
| **Statistical Analysis** | Paired comparisons, effect sizes, ANOVA |
| **Web Development** | HTML templates, CSS styling, JSON data |

## Author

**Mouhamadou SENE**  
MSc Data Science & Organizational Behavior  
Burgundy School of Business  
December 2025

## References

1. Deci, E. L., & Ryan, R. M. (1985). *Intrinsic motivation and self-determination in human behavior*. Plenum Press.
2. Frey, B. S., & Jegen, R. (2001). Motivation crowding theory. *Journal of Economic Surveys*, 15(5), 589-611.
3. Gneezy, U., & Rustichini, A. (2000). Pay enough or don't pay at all. *Quarterly Journal of Economics*, 115(3), 791-810.

## License

This project was developed for academic purposes as part of the Experimental Tools course.
