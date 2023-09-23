# Inspiration
- Inspired by R {fakir}, {charlatan} and Python  [faker](https://github.com/joke2k/faker) and MIMIC-IV.

# Goal
- Fake data for ventilator visuals dashboard
- see physiovar.md
- Eventually, publish as a python package

# Setup

- locally run through conda venv 'synenv' 
- newstwo.py will generate observations
- abg.py will generate abg measurements


# Issues

Fake data should be as 'real' as possible. Therefore

1. Missing data 
Patterns : missing completely at random (MCAR) vs. MAR vs. MNAR as per [Rubin](https://www.jstor.org/stable/2335739)

2. Errors
- Measurement Errors
- User Errors
 ~ 1 to 5% of errors would be realistic
- Containment e.g., ABG with containment 

3. Phases / States
Patient should usually follow the following states :
> Illness state (worse NEWS score and increased frequency of measurements)
> Improvement state (improvement in measured frequency and reduced frequency of measurements)
> Dying / Death state

The states can transition between each other.
Using NHS Levels of care intensity, LEVELs 0,1,2,3 can transition. 
?What is the transition probability 
- usually 1 to 3 patients admitted Level 2 or Level 3 per day

4. Ceiling Effect
- BM or pH 

5. Adult / Paeds / Neonate
- currently this is only for adult patients.

6. Variation
- ideeally observations should have diurnal variation or variation around the mean.

7. Timestamp
- alongside number 6, ideally should allow timestamping.

8. Congruency 
- internal logics have to work.  for example SBP > DBP 

9. Derived value
some of the ABG values are derived values

10. Outlier events


### abg.py

- temperature adjustment 
- Hendeson-Hasselbach equation for HCO3 from PaCO2 

### newstwo.py

> TO DO LIST
- need to allow scale 2 
- need to allow 'transitioning' from unwell to well and vice versa
- would therefore have 2 transitioning states
    - well -> unwell
    - unwell -> well 

this script has a main class called 'newsgen' class.
Newsgen has properties of status 'well' or 'sick'

first, you create a newsgen object with a desired property. 
second, you then apply a method from newsgen class called 'makeobs'. This takes argument n for number of observations.
then it will return a dictionary with 3 keys
key 1 is 't' which is effectively a timestamp in a longitudinal order. Currently this is just integers
key 2 is observations which is all the observations
key 3 is observations that is in a format for newscalculation custom function.