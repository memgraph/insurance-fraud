<h1 align="center">
 Insurance Fraud Detection Demo
</h1>

<p align="center">
  <a href="https://github.com/memgraph/insurance-fraud/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/g-despot/card-fraud" alt="license" title="license"/>
  </a>
  <a href="https://github.com/memgraph/insurance-fraud">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="build" title="build"/>
  </a>
</p>

<p align="center">
  <a href="https://twitter.com/intent/follow?screen_name=memgraphdb">
    <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Follow @memgraphdb"/>
  </a>
  <a href="https://memgr.ph/join-discord">
    <img src="https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"/>
  </a>
</p>

A demo modeling Insurance data, individuals along with their policies, claims, and incidents. Using Memgraph, utilizes the power of graphs to model the data and detect fraudulent claims. Extracts features using graph algorithms and uses machine learning to evaluate insurance claims.

## Data model
<p align="left">
  <img width="1000px" src="img/lab_graph_schema.png" alt="memgraph-tutorial-credit-card-fraud-data-model">
</p>


## Running the demo

You can set up the project with poetry:
```
poetry install
```

Or, if you don't want to use poetry, simply:
```
pip install -r requirements.txt
```

The demo is located in `./fraud_detection_demo.ipynb`. 

Recommended Python version is 3.9, since `sklearn` package doesn't yet support Python 3.10.

## Using the dataset only

If you want to just use the dataset, try running:
```
python dataset/data_generator.py 1000 300
```
And to import it into Memgraph, first start Memgraph, and then run the load script:
```
docker run -it -p 7687:7687 -p 3000:3000 memgraph/memgraph-platform

python load_demo_dataset.py 
```
