# Project Development

## Introduction
This document will help me track my features and changes I have made to the source code throughout the development cycle.

## Feature Checklist
- [x] Part 1: Fetch and Format stock Data
  - [x] Fetch stock data using yfinance
  - [x] Format using pandas
  - [x] Calculate daily return using pandas
  - [x] Format dataframe to csv

- [ ] Part 2: Predictive Analysis Engine
  - [ ] Implement CSV parsing loop
  - [ ] Get lag order
  - [ ] Build up autocorrelation and target matrices from lag order
  - [ ] Implement matrix multiplication and transposition functions
  - [ ] Implement OLS solver to get coefficients     

- [ ] Part 3: Final Touches and UI
  - [ ] Build user input side of UI
  - [ ] Build graphical side of UI
  - [ ] Implement 5 day prediction loop
  - [ ] Convert predicted prices back to stock prices
  - [ ] Plot prediction on graph
     
## Developer Log
This will allow me to store quick notes on design choices, errors, bugs and tweaks made during the coding phase.

### Date: 11/07/2026 - Project Start
* Focus - finish most of part 1 and maybe start a bit of part 2
* Notes - changed validation for pct change calculations: instead of attempting to fix the div by zero error, I allow pandas to handle it and delete the row with a "NaN" value. created all of part one, including validation.
