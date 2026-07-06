# Financial Models Research

## Document introduction
This document entails my research into appropriate financial models that I will use for my project. It will contain key definitions, benefits and drawbacks of each model and then at the end I will choose the model that I will take forward to use in the project. The aim of the predictive models is to take in an input (financial history data: i.e. an array of prices over time) then process it using the model that I have chosen and output a prediction of where the price will go.

## Models Evaluation
I will evaluate a few models, they are:
* Monte Carlo simulations
* Linear regression / Multiple Linear Regression
* Autoregressive models
All of these have complex mathematics and definitions and their own pros and cons behind them, I will investigate these further right now.

### Monte Carlo Simulations
#### Definition:
From [Wikipedia (Monte Carlo Method)](https://en.wikipedia.org/wiki/Monte_Carlo_method): a monte carlo simulation is "a broad class of computational algorithms based on repeated random sampling for obtaining numerical results, conceptualized by Polish mathematician Stanisław Ulam. The underlying concept is to use randomness to solve deterministic problems." Put simply, a Monte Carlo simmulation runs multiple random predictions to obtain concrete results.

#### Benefits:
* Quantifies risk as it provides a complete probability distribution
* Can handle multiple variables to model complex problems

#### Drawbacks:
* Garbage in means garbage out: the model must be provided with accurate, precise data to return an accurate, precise result
* Computationally intense: models that run a lot of simulations or predict over a longer timespan will use lots of system resources

### Linear Regression
#### Definition:
From [Wikipedia (Linear regression)](https://en.wikipedia.org/wiki/Linear_regression): linear regression is "a model that estimates the relationship between a scalar response (dependent variable) and one or more explanatory variables (regressor or independent variable). A model with exactly one explanatory variable is a simple linear regression; a model with two or more explanatory variables is a multiple linear regression." Put simply, a linear regression model will come up with a line/curve of best fit by optimising parameters around the dataset to reduce the error between the actual data and the model.

#### Benefits:
* Easier to implement than some of the other models
* Produces a transparent, readable mathematical function that is easy to extrapolate/intrapolate values from
* Uses very little system resources

#### Drawbacks:
* Very oversimplified model: almost all market data will not follow a linear trend
* Sensitive to outliers such as big jumps in the price due to a temporary event

### Autoregressive Models
#### Definition:
From [Wikipedia (Autoregressive Model)](https://en.wikipedia.org/wiki/Autoregressive_model): an AR model is "a modelled representation of a type of random process. It can be used to describe time-varying processes from many natural and artificial sources. The model specifies output variables that are dependent linearly on their own previous values on a stochastic basis. The model is in the form of a stochastic difference equation (or recurrence relation)." Put simply, an autoregressive model uses statistics and machine learning along with previous data to produce a recurrence relation that can be used to model future prices.

#### Benefits:
* Generation of highly realistic, intricate predictions
* They allow for the prediction of a price at any point

#### Drawbacks:
* Model relies on accurate inputs to produce an accurate output
* Model must be trained first before looking at data which can take a while due to computational intensity

## Summary
All 3 models have their own strengths and weaknesses.
* Monte Carlo simulations model a lot of outcomes but is computationally intense
* Linear regression is easy to implement but is very oversimplified
* Autoregressive models are the most accurate but rely on training a model beforehand

## Final Verdict
I was originally going to go with a Monte Carlo simulation because of it's relative simplicity, however autoregressive models are not only more accurate in their predictions but developing an autoregressive model is useful as the knowledge can be applied to other regions such as machine learning and artificial intelligence

### Reducing the drawbacks of an autoregressive model
* Model's reliance on accurate inputs: fetch up to date financial data
* Computational intensity: program model in C++ to speed up training

