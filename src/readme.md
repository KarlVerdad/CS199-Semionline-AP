# Online Assignment Problem with ML Advice
Kasilag, Clarence Gabriel  
Rey, Pollux  
Algorithms and Complexity Laboratory  
University of the Philippines Diliman  

This is the repository companion of the researcher's undergraduate thesis entitled __"Solving the Online Assignment Problem with Machile Learned Advice"__

How to use: 
1. clone the repository using `git clone`
```git clone https://github.com/polluxrey/CS-198.git```  
2. navigate to the source path. (if cloned in home)  
```cd CS198/src```  
3. install using pip the current path.   
```pip install .```
4. Access the function below by importing their locations.   
```import oapmla.OAPMLA```  
```import oapmla.graph_operations as go```  
```import oapmla.data_generate as dg```  

_Please do note that this is a very early iteration of the package for the accomplishment of the undergraduate thesis requirements for UP Diliman DCS. Further improvements may be done by the authors or other researchers in the future._

## Functions. 

The usable functions for this are grouped into different files. 

> OAPMLA

> graph_operations

> data_generate

### OAPMLA

The OAPMLA file includes the two algorithms discussed in the manuscript. 
___
`algorithm_1(A, A_prime)`  

Implementation for ALG in the manuscript, takes the actual input A and predictions A_prime and returns the matching using ML Advice   
*input:* numpy array **A**, numpy array **A_prime**  
*output:* numpy array **M**, integer **sum**  
___  
`algorithm_2(A, epsilon, k, seed=0)`  

Implementation for algorithm 2 in the manuscript, perturbs the input matrix A  
*input:* numpy array **A**, float **epsilon**, integer **k**, (optional) integer **seed**  
*output:* numpy array **A_prime**, list **rmsd**
___
___
### graph_operations
Includes operations with graphs and its numpy array representation
___
`create_graph_from_text(file_name)`

Creates a networkx bipartite graph from input text file  
*input:* string **file_name**  
*output:* numpy array **A**, networkx graph **G**  
___
`create_graph_from_numpy(array)`

Creates a networkx bipartite graph from numpy array  
*input:* numpy array **array**  
*output:* networkx graph **G**  
___
```compute_from_numpy(array)```

Used in conjuction with `compute_sum_with_matching` to compute the cost of computed matching via networkx optimal Karp Algorithm.  
*input:* numpy array **array**  
*output:* a call to `compute_sum_from_matching`  
___
`compute_sum_from_matching(A, M)`

Takes an array representation of bipartite graph and an optimal matching and returns the sum and the matching matrix.  
*input:* numpy array **A**, dictionary **M**  
*output:* integer *sum*, numpy array **zeros**  
___
`run_projection(arr, epsilon, k)`  

Projects a prediction using perturbation or arr with epsilon and k to the actual matrix arr

*input:* numpy array **arr**, float **epsilon**, integer **k**
*output:* integer **sol**, list **rmsd_list**
___
The following are helper functions for plotting and testing used by the researchers. 

`iterate_for_increasing_n_graph(file_name, err_list, k)`  
`iterate_for_different_error(file_name_list, epsilon, k)`  
`iterate_get_rmsd(file_name_list, epsilon_list, k_list)`  
___
___
### data_generate
An experimental file which includes future data generation and perturbation

```def perturb_choice(arr_inp, epsilon, k, seed=0):```  

Takes in the actual matrix A and perturbs using the epsilon and k parameters to imitate a ML Model's output of A_prime

*input:* numpy array **arr_inp**, float **epsilon**, integer **k**, (optional) integer **seed**  
*output:* numpy array **arr**, list **rmsd_list**