# db-auto-scale

Representing an optimal solution for Auto-Scaling VM clusters.

This project focuses on introducing an efficient, light weighted, and fast model for learning and predicting the system's usage even with low resources.

The output will be used to Auto-Scale the VM cluster according to the predicted system usage.

## the idea

For Auto-Scaling purposes, a resource manager does not need all the detailed information of VM's usage. 
For example, the exact data usage pattern down to seconds, or how exactly the usage behaves within a 5 minute period are excessive and unimportant data for predicting the required resources.
Therefore, we only need to work with the most vital information that can be extracted from the original VM usage to predict the system's future.
This approach removes the need of complex neural networks that are both heavy weighted and slow, and can be performed with a rather lighter weighted and faster neural network.

This idea has two main parts:
- Normalize and process data: removing excess information without altering any vital information for resource prediction purposes.
- Develop the neural network: A light weighted and fast neural network optimized to learn from the processed dataset and predict the future of the system's usage.

Here we introduce both parts in this project.

Also, another optimized neural network for predicting raw datasets is also introduced, that can be used as both an efficient timeseries predictor, and to benchmark the original solution.

### the solution

The aforementioned idea is implemented and can be found in the notebooks folder.
Step by step guide to run the project is contained in the same folder as another readme.

## data generator

This project is to be used with real data, but for developing and benchmarking purposes we also introduce a data generator:
A smart data generator that generates system usage mimiking real world usage patterns and rules.
A set of rules should be explained to the model representing the effect of each variable.
i.e 
- usage is lower during the day rather than night
- usage is higher during the weekends
- usage gradually increases over time by a specific pattern due to the business development.
- ...

The default (explained) generated data is a multivariate dataset with the following variables:
`seconds_passed`, `second`, `minute`, `hour`, `day_of_week`, `day_of_month`, `month`, `season`, `year`,

The model is highly flexible to any rules and patterns of data.

This is to be used for developing and benchmarking means.






