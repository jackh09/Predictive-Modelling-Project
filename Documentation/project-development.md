# Project Development

## Introduction
This document will help me track my features and changes I have made to the source code throughout the development cycle.

## Feature Checklist
- [x] Part 1: Fetch and Format stock Data
  - [x] Fetch stock data using yfinance
  - [x] Format using pandas
  - [x] Calculate daily return using pandas
  - [x] Format dataframe to csv

- [x] Part 2: Predictive Analysis Engine
  - [x] Implement CSV parsing loop
  - [x] Get lag order
  - [x] Build up autocorrelation and target matrices from lag order
  - [x] Implement matrix multiplication and transposition functions
  - [x] Implement OLS solver to get coefficients     

- [x] Part 3: Final Touches and UI
  - [x] Build user input side of UI
  - [x] Build graphical side of UI
  - [x] Implement 5 day prediction loop
  - [x] Convert predicted prices back to stock prices
  - [x] Plot prediction on graph
     
## Developer Log
This will allow me to store quick notes on design choices, errors, bugs and tweaks made during the coding phase.

### Date: 11/07/2026 - Project Start
* Focus - finish most of part 1 and maybe start a bit of part 2
* Notes - changed validation for pct change calculations: instead of attempting to fix the div by zero error, I allow pandas to handle it and delete the row with a "NaN" value. created all of part one, including validation.
* I also need to make sure that when I supply the C++ engine with parameters, I give it (lagOrder, dataCSVPath)
* I finished the whole of part 2. Part 3 will be tomorrow where I will hopefully finish everything

### Date: 12/07/2026 - Finishing the C++ part off
* Focus - get the loop working to predict next 5 days
* Notes - reworked some of the functions around but correct values are now predicted

### Date: 14/07/2026 - Push to finish project
* Focus - finish UI and get everything integrated together
* Notes - ui totally finished, no errors anywhere when using standard inputs. testing still to do
