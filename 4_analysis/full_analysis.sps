* Project  : Family Planning Among Married Women of Reproductive Age
*            in Kassala City, Sudan - 2025
* Script   : Full Statistical Analysis
* Author   : Abdulrahman Sirelkhatim
* Date     : March 2026
*
* NOTE: Update the FILE path in the GET DATA command below before running.
* Encoding: UTF-8.

GET DATA
  /TYPE=XLSX
  /FILE='C:\path\to\1_data\cleaned\cleaned_data.xlsx'
  /SHEET=name 'Sheet1'
  /READNAMES=ON.
CACHE.
EXECUTE.

VARIABLE LABELS
  age 'Age (years)'
  age_group 'Age Group'
  education 'Education Level'
  education_code 'Education Level (Numeric)'
  occupation 'Occupation'
  fp_use 'Currently Using Family Planning (1=Yes, 0=No)'
  received_counseling 'Received FP Counseling from Health Worker (1=Yes, 0=No)'
  experienced_side_effects 'Experienced Side Effects (1=Yes, 0=No)'
  satisfaction_fp_info 'Satisfaction with FP Information'
  satisfaction_code 'Satisfaction Score (1=Very Dissatisfied to 5=Very Satisfied)'
  husband_reaction 'Husband Reaction to FP'
  husband_reaction_code 'Husband Reaction (Numeric)'
  main_influencer 'Main Influencer on FP Decision'
  community_acceptability 'Community Acceptability of FP'
  community_acceptability_code 'Community Acceptability Score (1-4)'
  total_encouragement_factors 'Total Encouragement Factors Endorsed'
  total_avoidance_reasons 'Total Avoidance Reasons Endorsed'
  method_pills 'Uses Pills (1=Yes)'
  method_injectables 'Uses Injectables (1=Yes)'
  method_implants 'Uses Implants (1=Yes)'
  method_iud 'Uses IUD (1=Yes)'
  method_condoms 'Uses Condoms (1=Yes)'
  method_other 'Uses Other Method (1=Yes)'.

VALUE LABELS
  fp_use 0 'Not Using' 1 'Currently Using'
  /received_counseling 0 'No' 1 'Yes'
  /experienced_side_effects 0 'No' 1 'Yes'
  /education_code 1 'None' 2 'Primary' 3 'Secondary' 4 'Higher'
  /satisfaction_code 1 'Very Dissatisfied' 2 'Dissatisfied' 3 'Neutral' 4 'Satisfied' 5 'Very Satisfied'
  /husband_reaction_code 1 'Supports it' 2 'Neutral' 3 'Does not know' 4 'Opposes it'
  /community_acceptability_code 1 'Not acceptable' 2 'Not sure' 3 'Somewhat acceptable' 4 'Very acceptable'.
EXECUTE.

* Descriptive statistics.
DESCRIPTIVES VARIABLES=age total_encouragement_factors total_avoidance_reasons
  /STATISTICS=MEAN STDDEV MIN MAX.

FREQUENCIES VARIABLES=age_group education_code occupation fp_use
  received_counseling experienced_side_effects satisfaction_code
  husband_reaction_code community_acceptability_code main_influencer
  method_pills method_injectables method_implants method_iud method_condoms method_other
  enc_hw_advice enc_work enc_education enc_health_risk enc_husband_support
  enc_friends enc_access enc_economic
  avoid_more_children avoid_side_effects avoid_husband avoid_religion
  avoid_no_knowledge avoid_bad_exp avoid_no_access
  /STATISTICS=MODE /BARCHART PERCENT.

* Spearman and Pearson correlations: satisfaction vs FP use.
NONPAR CORR
  /VARIABLES=satisfaction_code fp_use
  /PRINT=SPEARMAN TWOTAIL NOSIG.

CORRELATIONS
  /VARIABLES=satisfaction_code fp_use
  /PRINT=TWOTAIL NOSIG.

* Chi-square tests: factors associated with FP use.
CROSSTABS /TABLES=age_group BY fp_use /CELLS=COUNT ROW /STATISTICS=CHISQ PHI.
CROSSTABS /TABLES=education_code BY fp_use /CELLS=COUNT ROW /STATISTICS=CHISQ PHI.
CROSSTABS /TABLES=occupation BY fp_use /CELLS=COUNT ROW /STATISTICS=CHISQ PHI.
CROSSTABS /TABLES=husband_reaction_code BY fp_use /CELLS=COUNT ROW /STATISTICS=CHISQ PHI.
CROSSTABS /TABLES=community_acceptability_code BY fp_use /CELLS=COUNT ROW /STATISTICS=CHISQ PHI.
CROSSTABS /TABLES=received_counseling BY fp_use /CELLS=COUNT ROW /STATISTICS=CHISQ RISK.
CROSSTABS /TABLES=main_influencer BY fp_use /CELLS=COUNT ROW /STATISTICS=CHISQ PHI.
CROSSTABS /TABLES=satisfaction_code BY fp_use /CELLS=COUNT ROW /STATISTICS=CHISQ PHI.
CROSSTABS /TABLES=experienced_side_effects BY fp_use /CELLS=COUNT ROW /STATISTICS=CHISQ PHI.

* Binary logistic regression: predictors of FP use.
LOGISTIC REGRESSION VAR=fp_use
  /METHOD=ENTER education_code received_counseling experienced_side_effects
    satisfaction_code community_acceptability_code
  /PRINT=GOODFIT CI(95) ITER(1) HOSMER
  /CRITERIA=PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.5).

* NOTE: Update the OUTFILE path below before saving.
SAVE OUTFILE='C:\path\to\1_data\cleaned\cleaned_data.sav' /COMPRESSED.
EXECUTE.
