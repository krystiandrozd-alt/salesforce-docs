---
name: "ambition-amplifier"
description: "Raises the ambition of a task before starting it (altitude, depth, range, outside verification) and rewrites it into a bolder, verifiable brief. Use for 'think bigger', 'podnieś poprzeczkę', or routine tasks wanting more."
---

# Ambition Amplifier

The default reading of a request is usually the smallest one: make the deck, fix the bug, summarise the data. Models can often do much more, but only if the brief asks for it and gives them raw material, real methods and a way to check the result. This skill turns a modest request into an ambitious, verifiable brief, and then (if the user wants) runs it. Based on Felix Rieseberg's "How to be more ambitious: a tutorial for humans with models".

Reply in the user's language (Polish or English).

Trigger also when the user hands over a routine task (QBR deck, report, analysis, bug fix, RFP section) and wants more than the obvious version, or says "jak zrobiłby to najlepszy ekspert", "co dalej po tym celu", "make this prompt more ambitious", even without the word "ambition".

## Workflow

### 1. Capture the starting task
Restate the task in one line, plus what the user has: data sources, tools, connectors, time, audience. If the request is vague, ask at most one question. Otherwise go on.

### 2. Altitude: go from the task to the outcome
Ask "and after that, what should happen?" two or three times. Each answer is one rung:
- **Rung 1, the task as asked** (e.g. a QBR deck for a customer).
- **Rung 2, the decision it serves** (e.g. the three decisions leadership must make, with the case for and against each).
- **Rung 3, the system that makes the task unnecessary or continuous** (e.g. an early-warning mechanism that catches problems before a quarterly review, back-tested on past quarters and run alongside the current process).

Altitude fits outcome-driven work. A good sign is that people normally hold meetings about it. For creative work, skip this step or keep it light.

Rung 3 usually means taking the human out of the loop. Name what that needs: access to the data (connectors, exports), mapping between artifacts (versions to commits, orders to accounts), environments in which to reproduce and verify.

### 3. Depth: work the way the best professional would
Answer these four questions explicitly before you rewrite anything:
1. What would a top professional do here that goes beyond the request?
2. What is the rawest source material they would start from? Prefer raw records, logs and exports over summaries.
3. Which specific methods and instruments would they use? Name them: a database, a statistical test, a cohort analysis, a simulation, a profiler. Being told to "act like an expert" changes the vocabulary but not the work, so ask for the methods.
4. What, other than the model or the user, would verify the result? (See step 5.)

Then add two depth moves where they fit:
- **A target that seems unreasonable but is stated as achievable.** Pick one much stricter than needed (200 ms instead of 5 s, every claim traceable to a source row). Specific, hard goals beat "do your best".
- **An adversarial test of a belief.** State the team's working assumption ("churn is an onboarding problem") and ask the model to try to reproduce it from raw data, or refute it. Where possible, ask for new knowledge as well: blind spots and signals nobody knew about, validated on held-out data.

### 4. Range: bring in other fields
- **Replace nouns with verbs.** Rewrite the deliverable as the job it does. "A deck" becomes "getting busy people to believe a cause-and-effect story and decide under uncertainty in 30 minutes." The verbs show which fields have techniques for that job: persuasion, journalism, forecasting, information design.
- **Assemble the crew.** List 4–6 disciplines whose techniques apply, each with one concrete technique, and include at least one adversarial role (red team, short seller, forensic accountant, hostile auditor).
- **Methods, not costumes.** Use the fields to find techniques and ask for what the professional does, not for writing in their voice. Role play makes the output stranger without improving it.
- If subagents or parallel threads are available, each crew member can be its own pass.

### 5. Verification: an outside judge
Don't let the model grade its own work. Pick the strongest check available, in this order of preference:
1. A tool the model can run itself for immediate feedback: tests, a benchmark, a validator, a back-test, a reproduction on a clean machine.
2. Held-out data or historical outcomes.
3. A separate reviewer agent that hasn't seen how the work was produced.
4. A named human check, as a last resort.

### 6. Check feasibility
All of the above assumes the model has a computer, the ability to install software, and access to the data. List what's missing (connector, export, access rights, environment). Make each item an action for the user, not a reason to drop ambition.

### 7. Write the amplified brief
Use this structure:

```
## Starting task
<one line>

## Ambition ladder
1. As asked: ...
2. Next level: ...
3. Most ambitious: ...
Recommended rung: <n>, because <why: value vs. feasibility now>

## Amplified prompt
<the ready-to-run prompt at the recommended rung, covering raw sources, named methods,
the stretch target, the adversarial test, the crew techniques and the verification step>

## Crew (range)
- <discipline>: <technique it contributes>
- ... (at least one adversarial role)

## Verification
<the outside judge and how it is run>

## Prerequisites / gaps
- <access, tool, data the user must provide>
```

Then offer to run the amplified prompt now.

## Tone: self-efficacy
People limit ambition as much as models do, through doubt about what's possible. Present the top rung as a real option, not as a fantasy, and keep the rest of the ladder so a smaller first step is acceptable. Permission to try and fail is part of the point. Don't moralise about it. One sentence at most, if any.

## Anti-patterns to avoid
- Letting the model judge its own output.
- Vague goals ("make it better", "make money") with no specific target.
- Accepting the first reading of the task without asking about the outcome.
- Role play instead of methods.
- Summaries in place of raw data.
- An ambitious brief with no tools, data or verification behind it.

## Example (abridged)
**Input:** "Przygotuj QBR dla klienta Acme na przyszły tydzień."

**Ladder:** (1) deck with KPIs and the quarter's changes; (2) the three most urgent decisions for Acme leadership, each with a case for and against and the supporting data; (3) a continuous health monitor that flags the issues a QBR would surface, back-tested on the last four quarters and piloted alongside the next QBR.

**Depth:** start from raw orders, tickets and usage exports rather than last quarter's deck. Methods: cohort analysis, a variance bridge, a significance check on changes. Stretch target: every number on a slide traceable to a source query. Adversarial test: "We believe the decline comes from pricing. Try to reproduce that from raw data."

**Crew:** analyst (variance bridge), journalist (lead with the story), editor (cut to 30 minutes), information designer (one chart per decision), forensic accountant (red team on the numbers).

**Verification:** a script that recomputes every slide figure from the source data, plus a back-test of the monitor's flags against past quarters.