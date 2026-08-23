# Letter recon findings

Read in full: VYEPTI 6/24/2026, OZEMPIC 2/26/2026, SKYRIZI 9/9/2025

## The decisive answer
FDA quotes approved label text in 1 of 3. The other two cite no PI at all.
Dominant evidence type is FDA's critique of the study the company cited,
not a label passage.

## Consistent letter structure
1. RE block: application number, product, MA number
2. Promotional piece identified by title and internal code
3. Claims quoted verbatim in bullets, emphasis noted
4. "These claims create a misleading impression that X, when this is not
   the case"
5. Reasoning about the cited evidence
6. "We acknowledge [disclaimer]. However, [why it fails]"
7. Conclusion and Requested Action, boilerplate

## Observed violation bases
- indication_overreach (Ozempic: implies all patients qualify for all uses)
- unsupported_superiority (Ozempic vs other GLP-1s, Skyrizi vs Stelara)
- study_design_inadequate (Skyrizi open-label, differential dropout)
- exploratory_endpoint (Vyepti post-hoc, no alpha allocation)
- instrument_validity (Vyepti HIT-6 content validity, MIDAS recall bias)
- risk_presentation (Ozempic: no signal that risk info follows)

## Claim counts
Ozempic 9 quoted lines, 3 violation groups
Skyrizi 8 quoted claims, 1 violation group
Vyepti 14 quoted claims, 3 violation groups
Structure is letter -> violation groups -> claims. One to many both ways.

## Corrections to earlier assumptions
- Application number always present in RE line, index omission is irrelevant
- Do not exclude visual claims. Visual elements are cited as part of the
  reasoning (shirt colours, graph prominence, font size)
- Ozempic is video: claims are tagged VO or SUPER with timestamps

## Corpus survey (all 115 letters)

Regex-reliable:
  requested_action boilerplate  98%
  application number            96%
  RE block                      92%

Content markers:
  "misleading impression"       67%
  + "misleadingly"              90% combined
  PI section named              45%

Out of scope: 5 letters (110684, 114446, 117097, 120674, 132641).
Unapproved-product distribution under 502(f)(1), no promotional claims
to extract. 117097 hits one marker only, needs manual confirmation.

Working corpus: 110 letters.
Quoted spans across corpus: 1,038. Median 7 per letter, max 66.

## Corrections to my own recon
The three letters I read closely were not representative. Violation types
I generalised from them are rare corpus-wide:
  superiority   2 / 115
  post hoc      6 / 115
  open label   11 / 115
Do not fix the basis_type enum in advance. Extract FDA reasoning as free
text, cluster it, then derive categories from what is actually there.