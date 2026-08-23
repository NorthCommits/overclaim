# Schema v2

One row per claim, denormalised. violation_group_id allows regrouping.

## Provenance
row_id, letter_url, letter_date, letter_type, company, retrieved_at
reference_id        string   FDA internal ref from letter footer

## Product
application_number  string   from RE line, always present
brand_name, generic_name
ma_number           string
spl_setid           string   nullable, openFDA match

## Promotional piece
promo_piece_type    enum     webpage | video | banner | sales_aid |
                             brochure | social | other
promo_piece_title   string
promo_piece_code    string   nullable, internal code e.g. US25OZM01130

## Claim
violation_group_id  string
claim_text          string   verbatim
claim_role          enum     headline | body | vo | super | graphic_caption
timestamp           string   nullable, video only
visual_element_cited bool    FDA cites imagery, layout, or prominence

## FDA reasoning
misleading_impression string  FDA's own "creates the impression that X"
basis_type          string   nullable in v2. Free text extraction first.
                             Enum to be derived from clustering, not
                             assumed. See recon notes.
basis_detail        string   condensed reasoning
cited_evidence      string   nullable, study the company relied on
evidence_limitation string   nullable, why it fails

## Mitigation attempt
mitigating_disclosure string nullable, disclaimer the company included
mitigation_rejected   string nullable, why FDA found it insufficient

## Label link
label_section       string   nullable
label_quote         string   nullable, populated only when FDA quotes it

## Verdict
verdict             enum     misleading | supported