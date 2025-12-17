# Chapter 7.3: BEPS Action 7 – Preventing the Artificial Avoidance of Permanent Establishment

## EXAM INTELLIGENCE
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Syllabus Area: II.G.3 - BEPS Action 7 – Preventing the artificial avoidance of a
               permanent establishment
Syllabus Level: 3 (Advanced Knowledge)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Exam Frequency: HIGH - Often combined with Article 5 questions
Recent Appearances:
  • December 2022 Q8: Explicitly referenced "BEPS Action 7 (Preventing the
    Artificial Avoidance of Permanent Establishment Status, Final Report 2015)"
    as context for 25-mark Article 5 question

Strategic Priority: ★★★★★ CRITICAL
- Contemporary BEPS topic
- Foundation for understanding 2017 Article 5 changes
- Examiner expects candidates to connect policy to technical changes
- MLI implementation is examinable
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 1. INTRODUCTION: THE PE PROBLEM IN BEPS

### 1.1 Why Action 7 Was Needed

The permanent establishment (PE) definition is a cornerstone of international taxation. Under tax treaties, an enterprise's business profits are taxable in a source state **only if** the enterprise has a PE there. This creates a powerful incentive: if an enterprise can conduct substantial business activities in a country without triggering PE status, it can avoid source country taxation entirely.

The BEPS Project identified that MNEs had developed sophisticated strategies to avoid PE status artificially. These strategies allowed enterprises to:
- Make sales in a country through intermediaries without creating taxable presence
- Fragment operations to exploit specific activity exemptions
- Split contracts to avoid duration thresholds

The result was a fundamental disconnect between where economic activities occurred and where profits were taxed - one of the core problems the entire BEPS Project aimed to address.

### 1.2 Action 7 Mandate

The BEPS Action Plan (2013) defined Action 7 as:

> "Develop changes to the definition of PE to prevent the artificial avoidance of PE status in relation to BEPS, including through the use of **commissionaire arrangements** and the **specific activity exemptions**."

This mandate was deliberately narrow - focused on preventing *artificial* avoidance, not expanding PE definitions generally. The concern was strategies that lacked genuine commercial substance and existed primarily for tax reasons.

---

## 2. THE THREE TARGETED STRATEGIES

### 2.1 Strategy 1: Commissionaire Arrangements

**What is a commissionaire?**

A commissionaire is a civil law concept where an agent:
- Sells goods or services in their own name
- Acts on behalf of a principal (the foreign enterprise)
- Takes legal title briefly before transferring to customer
- The principal retains beneficial ownership until sale

```
COMMISSIONAIRE STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

     COUNTRY R (Residence)          COUNTRY S (Source)
    ┌─────────────────────┐        ┌─────────────────────┐
    │                     │        │                     │
    │  PRINCIPAL          │        │  COMMISSIONAIRE     │
    │  (MNE Parent)       │◄───────│  (Local Agent)      │
    │                     │ Agency │                     │
    │                     │ Agree. │  Sells in OWN name  │
    │  Retains profits    │        │  but for Principal  │
    │  (no PE in S)       │        │                     │
    │                     │        │          │          │
    └─────────────────────┘        └──────────┼──────────┘
                                              │
                                              ▼
                                         CUSTOMER
                                   (Contract with
                                    Commissionaire)

PRE-2017 RESULT: No PE because contracts not "in the name of" Principal
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Why this was a problem:**

Under pre-2017 Article 5(5), an agency PE only existed if the agent concluded contracts "in the name of" the foreign enterprise. Because commissionaires concluded contracts in their own name (legally binding themselves, not the principal), no PE was created - even though the principal's goods were being sold and the economic substance of the arrangement was equivalent to a subsidiary distributor.

**Key cases confirming the loophole:**
- **Zimmer (France, 2010)**: French Supreme Court held commissionaire did not create PE
- **Dell (Norway, 2011)**: Norwegian court reached same conclusion

These decisions were technically correct under the existing treaty language but highlighted a policy gap that allowed economically identical arrangements to have vastly different tax consequences.

### 2.2 Strategy 2: Exploitation of Specific Activity Exemptions

**The pre-2017 problem:**

Article 5(4) provided automatic exemptions for certain activities:
- Storage, display, delivery of goods
- Maintaining stock for storage/display/delivery
- Purchasing goods or collecting information
- Any activity of a "preparatory or auxiliary" character

The listed activities (a)-(d) were **automatically** deemed preparatory or auxiliary - no further analysis required. This enabled MNEs to:

```
FRAGMENTATION STRATEGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SINGLE ENTERPRISE operates multiple "exempt" facilities:

  ┌─────────────────────────────────────────────────────┐
  │                    COUNTRY S                        │
  │                                                     │
  │  ┌──────────┐   ┌──────────┐   ┌──────────────┐    │
  │  │Warehouse │   │Warehouse │   │ Information  │    │
  │  │"Delivery"│   │"Storage" │   │  Office      │    │
  │  │ Art 5(4) │   │ Art 5(4) │   │  Art 5(4)    │    │
  │  │   (a)    │   │   (a)    │   │    (d)       │    │
  │  └──────────┘   └──────────┘   └──────────────┘    │
  │                                                     │
  │  Each facility → Auto-exempt → No PE               │
  │                                                     │
  │  COMBINED = Major distribution operation           │
  │  BUT technically: No PE                            │
  └─────────────────────────────────────────────────────┘

Problem: Core business functions performed, but no PE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

This was particularly problematic in e-commerce, where large fulfillment warehouses could be characterized as mere "delivery" facilities.

### 2.3 Strategy 3: Contract Splitting

**The construction PE threshold:**

Article 5(3) provides that construction sites are PEs only if they last more than 12 months (OECD) or 6 months (UN). MNEs could avoid this by:

- Splitting a single project into multiple contracts
- Using related enterprises to perform sequential work
- Structuring contracts to stay just under the threshold

**Example:**
```
PROJECT: 18-month construction contract

WITHOUT SPLITTING:
  Single contract: 18 months → Exceeds threshold → PE

WITH SPLITTING:
  Contract 1 (Company A): Months 1-11 → No PE
  Contract 2 (Company B): Months 12-18 → No PE

  Combined work: Same project, but technically no PE
```

---

## 3. BEPS ACTION 7 FINAL REPORT (OCTOBER 2015)

### 3.1 Key Recommendations

The Action 7 Final Report recommended changes in three main areas:

| Area | Problem Addressed | Solution |
|------|-------------------|----------|
| **Agency PE** | Commissionaire escape | Expand "conclude contracts" to include "principal role" |
| **Specific exemptions** | Automatic exemption abuse | Require prep/aux character for ALL activities |
| **Anti-fragmentation** | Splitting operations | New rules to aggregate related activities |
| **Contract splitting** | Avoiding duration thresholds | Aggregate related enterprise contracts |

### 3.2 Changes to Article 5(5): Agency PE

**Old wording:**
> Agent who "habitually exercises... authority to **conclude contracts in the name of** the enterprise"

**New wording (2017 MTC):**
> Agent who habitually:
> - Concludes contracts, OR
> - **Plays the principal role leading to the conclusion of contracts** that are routinely concluded without material modification

**Key additions:**
- Contracts need not be "in the name of" the principal
- "Principal role" captures negotiations even where formal conclusion is elsewhere
- "Routinely concluded without material modification" targets rubber-stamp approvals

### 3.3 Changes to Article 5(4): Specific Exemptions

**Key change:**

Added requirement that ALL activities in Article 5(4)(a)-(e) must be of a "preparatory or auxiliary character" - no more automatic exemptions.

**New Article 5(4.1) - Anti-fragmentation:**

Where an enterprise (or closely related enterprise) carries on activities at the same or different locations, and either:
- That location constitutes a PE of the enterprise, OR
- The **overall activity** resulting from the combination is not preparatory or auxiliary

Then Article 5(4) exemptions do not apply.

### 3.4 Changes to Article 5(6): Independent Agent

**Narrowed the exception:**

An agent acting "exclusively or almost exclusively" for one or more **closely related enterprises** cannot qualify as an independent agent.

**"Closely related" defined (Art 5(8)):**
- More than 50% ownership or control
- Same person owns >50% of both enterprises

---

## 4. IMPLEMENTATION THROUGH THE MLI

### 4.1 MLI Articles 12-15

The Action 7 recommendations are implemented in the Multilateral Instrument (MLI) through four articles:

| MLI Article | Subject | Corresponds to |
|-------------|---------|----------------|
| **Article 12** | Artificial Avoidance through Commissionnaire Arrangements | Art 5(5)-(6) changes |
| **Article 13** | Artificial Avoidance through Specific Activity Exemptions | Art 5(4) changes |
| **Article 14** | Splitting-up of Contracts | Art 5(3) aggregation |
| **Article 15** | Definition of Closely Related Person | Art 5(8) |

### 4.2 NOT a Minimum Standard

**Important**: Action 7 is **NOT a BEPS minimum standard**. This means:
- Adoption is voluntary (though recommended)
- Countries can choose which articles to adopt
- Countries can opt out entirely

This contrasts with Actions 5, 6, 13, and 14, which are minimum standards requiring compliance for Inclusive Framework members.

### 4.3 MLI Implementation Options

**Article 12 (Commissionnaire):**
- Jurisdictions choose whether to adopt
- Covers expanded agency PE definition

**Article 13 (Specific Activity Exemptions):**
- **Option A**: All activities must be preparatory/auxiliary (broader)
- **Option B**: Only applies where anti-fragmentation triggered (narrower)
- Countries can opt out entirely

**Article 14 (Contract Splitting):**
- Optional adoption
- Aggregates time periods for related enterprise contracts

**Article 15 (Closely Related Definition):**
- **Mandatory** if any of Articles 12, 13, or 14 adopted
- Provides consistent 50% threshold definition

### 4.4 Country Adoption Examples

| Country | Article 12 | Article 13 | Article 14 |
|---------|------------|------------|------------|
| **Australia** | Adopted | Option A | Adopted |
| **UK** | Adopted | Neither option | Adopted |
| **France** | Adopted | Option B | Adopted |
| **Canada** | Adopted | Opted out | Adopted |
| **USA** | Not MLI signatory | - | - |

---

## 5. PROFIT ATTRIBUTION GUIDANCE (2018)

### 5.1 The Attribution Challenge

The expanded PE definitions create new PEs, but how should profits be attributed to them? A commissionaire-arrangement PE doesn't have traditional assets or employees - the commissionaire does.

The Action 7 Final Report mandated additional guidance on profit attribution, delivered in March 2018.

### 5.2 The 2018 Additional Guidance

**Report:** "Additional Guidance on the Attribution of Profits to Permanent Establishments under BEPS Action 7" (OECD, March 2018)

**Key principles:**

1. **Authorised OECD Approach (AOA) applies**: Same framework as traditional PEs
2. **Functional analysis crucial**: Identify significant people functions
3. **Limited profits to expanded PEs**: These PEs typically perform limited functions
4. **Avoid double taxation**: Article 9 (transfer pricing) and Article 7 (PE attribution) must be coordinated

### 5.3 Practical Application

**For commissionnaire-arrangement PEs:**

```
PROFIT ATTRIBUTION - COMMISSIONNAIRE PE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Identify functions, assets, risks of deemed PE
  • Functions: Contract negotiation by agent
  • Assets: Typically none (belong to agent entity)
  • Risks: Limited (agent bears inventory/credit risk)

STEP 2: Apply arm's length principle
  • What would independent enterprise earn for these functions?
  • Typically: Commission-type return

STEP 3: Coordinate with Article 9
  • Agent entity (Article 9): Arm's length remuneration
  • Deemed PE (Article 7): Remaining attributable profit
  • TOTAL should not exceed combined enterprise profit

RESULT: Often minimal additional profit to deemed PE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5.4 Key Examples in 2018 Guidance

The guidance includes detailed examples:
- **Example A**: Commissionnaire structure for sale of goods
- **Example B**: Online advertising sales structure
- **Example C**: Procurement structure

Each demonstrates how to identify significant people functions and attribute profits accordingly.

---

## 6. RELATIONSHIP TO OTHER BEPS ACTIONS

### 6.1 Connection to Other Actions

| Related Action | Connection to Action 7 |
|----------------|------------------------|
| **Action 1** (Digital Economy) | Digital businesses often avoid PE through online sales |
| **Actions 8-10** (Transfer Pricing) | Profit attribution to new PEs uses TP principles |
| **Action 13** (CbCR) | Increased transparency reveals PE avoidance |
| **Action 15** (MLI) | Implementation vehicle for Action 7 changes |

### 6.2 Action 7 in BEPS Context

Action 7 addresses the "where to tax" question (nexus), while Actions 8-10 address "how much to tax" (profit allocation). Together, they aim to ensure profits are taxed where economic activity occurs.

---

## 7. PRACTICAL IMPLICATIONS FOR BUSINESSES

### 7.1 Structures at Risk

MNEs should review arrangements where:
- Sales representatives negotiate contracts approved elsewhere
- Warehouses/fulfillment centers are characterized as "delivery" facilities
- Multiple exempt activities are performed in one jurisdiction
- Related companies perform sequential work on same projects

### 7.2 Restructuring Considerations

Many MNEs have responded by converting:
- Commissionaire arrangements → Limited risk distributors (LRDs)
- Principal structures → More substance in source countries
- Split operations → Consolidated structures accepting PE status

### 7.3 Documentation Needs

Enhanced documentation required:
- Functional analysis of local activities
- Evidence of preparatory/auxiliary character
- Agent independence evidence
- Contract structure justification

---

## 8. EXAM APPLICATION

### 8.1 December 2022 Q8 - How to Use Action 7

The December 2022 Q8 asked candidates to:
1. Outline changes made to Article 5 in OECD MTC 2017
2. Summarize impact on source state taxing rights
3. Consider Article 5 as it relates to commissionaire arrangements

**Examiner guidance**: "Candidates' answers could begin by setting the scene, which may include... providing some context to the 2017 changes i.e. **BEPS Action 7** (Preventing the Artificial Avoidance of Permanent Establishment Status, Final Report 2015)."

### 8.2 Answer Framework

```
EXAM APPROACH: BEPS ACTION 7 QUESTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. SET THE SCENE (2-3 marks)
   • PE definition is gateway to source taxation of business profits
   • MNEs had developed strategies to avoid PE artificially
   • BEPS Action 7 mandate: Address commissionaire and specific exemptions

2. IDENTIFY STRATEGIES TARGETED (3-4 marks)
   • Commissionaire arrangements
   • Fragmentation of activities
   • Contract splitting

3. EXPLAIN KEY CHANGES (5-8 marks)
   • Article 5(5): Expanded agency PE ("principal role" test)
   • Article 5(4): Prep/aux requirement for all activities
   • Article 5(4.1): Anti-fragmentation rule
   • Article 5(6): Narrowed independent agent exception

4. DISCUSS IMPLEMENTATION (2-3 marks)
   • MLI Articles 12-15
   • NOT a minimum standard
   • Variable country adoption

5. CONSIDER PROFIT ATTRIBUTION (if asked) (2-3 marks)
   • 2018 Additional Guidance
   • AOA applies but limited functions = limited profits
   • Coordinate Article 7 and Article 9

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 9. SUMMARY: KEY POINTS FOR EXAM

```
BEPS ACTION 7 - ESSENTIAL KNOWLEDGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. MANDATE
   • Prevent ARTIFICIAL avoidance of PE status
   • Focus: Commissionaire arrangements + specific exemptions

2. THREE TARGETED STRATEGIES
   • Commissionaire arrangements (contract not "in name of" principal)
   • Exploitation of Article 5(4) automatic exemptions
   • Contract splitting to avoid duration thresholds

3. KEY CHANGES (2015 Report → 2017 MTC)
   • Art 5(5): "Principal role" expands agency PE
   • Art 5(4): Prep/aux test now applies to ALL activities
   • Art 5(4.1): Anti-fragmentation rule
   • Art 5(6): Narrowed independent agent exception
   • Art 5(8): "Closely related" definition (50% threshold)

4. MLI IMPLEMENTATION
   • Articles 12, 13, 14, 15
   • NOT a minimum standard (voluntary)
   • Options A and B for Article 13
   • Variable country adoption

5. PROFIT ATTRIBUTION (2018 Guidance)
   • AOA applies to new PEs
   • Limited functions = limited profits
   • Coordinate with transfer pricing (Article 9)

6. KEY CASES
   • Zimmer (France, 2010) - commissionaire no PE pre-2017
   • Dell (Norway, 2011) - same conclusion

7. EXAM APPROACH
   • Link policy context to technical changes
   • Explain problem → solution → implementation
   • Reference Final Report and 2018 Guidance

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 10. LINK TO OTHER CHAPTERS

| Topic | Chapter | Connection |
|-------|---------|------------|
| Article 5 Technical Details | 7.2 | Detailed analysis of PE provisions |
| Article 7 Business Profits | 8.1 | Profit attribution to PEs |
| Transfer Pricing | Part IV | Actions 8-10, profit allocation |
| MLI | 3.4 | Implementation vehicle |
| BEPS Overview | Various | Context for all BEPS actions |

---

## 11. REFERENCES

### Primary Sources
- OECD. **Preventing the Artificial Avoidance of Permanent Establishment Status, Action 7 - 2015 Final Report** (Paris: OECD, 2015)
- OECD. **Additional Guidance on the Attribution of Profits to a Permanent Establishment under BEPS Action 7** (Paris: OECD, 2018)
- OECD. **Multilateral Convention to Implement Tax Treaty Related Measures to Prevent BEPS** (Paris: OECD, 2016)
- OECD. **Model Tax Convention on Income and on Capital** (Paris: OECD, 2017)

### Web Sources (December 2025)
- [OECD Action 7 Final Report](https://www.oecd.org/en/publications/2015/10/preventing-the-artificial-avoidance-of-permanent-establishment-status-action-7-2015-final-report_g1g58ce8.html)
- [OECD 2018 Additional Guidance](https://www.oecd.org/en/publications/2018/03/additional-guidance-on-the-attribution-of-profits-to-a-permanent-establishment-under-beps-action-7_63ee620d.html)
- [MLI Articles 12-15 Implementation](https://www.action15-mli.net/multilateral-convention/article-12-avoiding-p-e-status-commissionnaire-arrangements/article-12-avoidance-of-p-e-status-through-commissionnaire-arrangements.html)

### Past Exam Questions
- December 2022 Q8: Article 5 changes with BEPS Action 7 context (25 marks)

---

*Chapter 7.3 covers syllabus area II.G.3 - BEPS Action 7 – Preventing the artificial avoidance of a permanent establishment. This is a Level 3 topic requiring advanced knowledge of the policy context, targeted strategies, recommended changes, and implementation through the MLI.*
