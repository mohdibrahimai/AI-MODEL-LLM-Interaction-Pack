# Failure‑Mode Atlas

This atlas catalogues common failure patterns observed in question‑answering interactions.  Each entry includes a brief description of the symptom, a quick way to detect it and a suggested fix using simple rules or micro‑tools.  Use this as a reference when evaluating and improving model outputs.

| #  | Name                     | Symptom                                                      | Quick Test                                      | Fix                                                |
|----|-------------------------|--------------------------------------------------------------|-------------------------------------------------|----------------------------------------------------|
| 1  | Over‑hedging            | Excessive use of "might", "maybe", "perhaps"               | Look for hedging words                          | Run `tone_normalizer` to remove hedges             |
| 2  | Missing answer          | Avoids answering the core question                           | Check if the answer contains keywords from query| Insert a direct answer at the beginning           |
| 3  | Hallucinated citations  | Cites sources unrelated to the answer                        | Compare citations to gold sources               | Use `citation_deduper` and restrict to gold        |
| 4  | Citation spam           | Includes too many citations                                  | Count citations >2                               | Deduplicate and select only necessary citations    |
| 5  | Ambiguity ignored       | Fails to clarify an ambiguous query                          | Contains multiple conjunctions or vague nouns    | Use `question_splitter` and ask for clarification  |
| 6  | Overlong answer         | Runs on without structure or stops late                     | Token count >120                                 | Trim to ≤120 tokens and structure with bullets     |
| 7  | Missing refusal         | Invents an answer when data is unavailable                   | No supporting sources exist                      | Refuse politely and suggest next steps             |
| 8  | Conflict unacknowledged | Does not mention known disagreements between sources          | Query mentions "some say... others..."           | Use disagreement/abstain template                  |
| 9  | Jargon overload         | Uses technical jargon without explanation                    | Contains many domain‑specific terms             | Rewrite in plain language or define terms          |
| 10 | Bullet soup             | Lists items without logical order or too many bullets        | Bullet count >5                                  | Limit to ≤5 bullets; group or summarise            |
| 11 | Passive voice           | Uses passive constructions excessively                       | Detect "was", "were", "has been"                 | Rewrite to active voice                            |
| 12 | Redundancy              | Repeats the same information several times                   | Identical phrases repeated                       | Remove duplicate sentences                         |
| 13 | Outdated information    | Provides facts that are no longer current                    | Mentions outdated years or obsolete facts        | Verify recency; suggest newer sources              |
| 14 | Scope creep             | Answers tangential questions the user didn’t ask             | Introduces new topics not in the query           | Restate the scope and remove tangential material   |
| 15 | Math errors             | Miscalculates or misstates numbers                           | Contains numerical calculations                  | Double‑check with a calculator                     |
| 16 | Missing definition      | Launches into nuance without defining key terms              | Uses specialised terms without definition        | Provide a one‑sentence definition first            |
| 17 | Unranked list           | Gives a list without ranking or criteria                    | List items not ordered or justified             | Provide ordering or explain how they were selected |
| 18 | Buried lede             | Hides the main answer in the middle of the response          | Answer appears after the first two sentences     | Move answer to the first sentence                  |
| 19 | No next step            | Fails to guide the user after a partial answer               | No imperative phrases like "consult" or "search" | Suggest a concrete next action                     |
| 20 | Tone mismatch           | Tone is too casual or too formal for the context             | Use of slang or overly technical language        | Adjust tone to a neutral, informative style        |