# Empowering Machine Learning Models with Contextual Knowledge for Enhancing the Detection of Eating Disorders in Social Media Posts

## Table of contents


## Authors

* José Alberto Benítez-Andrades - jbena@unileon.es - <a href="https://orcid.org/0000-0002-4450-349X" rel="nofollow" target="_blank">0000-0002-4450-349X</a>
* María Teresa García-Ordás - mgaro@unileon.es - <a href="https://orcid.org/0000-0002-3796-3949" target="_blank">0000-0002-3796-3949</a>
* Mayra Russo - mrusso@l3s.de - <a href="https://orcid.org/0000-0001-7080-6331" rel="nofollow" target="_blank">0000-0001-7080-6331</a>
* Ahmad Sakor - Ahmad.Sakor@tib.eu - <a href="https://orcid.org/0000-0001-8007-7021" rel="nofollow" target="_blank">0000-0001-8007-7021</a>
* Luis Daniel Fernandes Rotger - luis@bakkenbaeck.no - 
* Maria-Esther Vidal - maria.vidal@tib.eu - <a href="https://orcid.org/0000-0003-1160-8727" rel="nofollow" target="_blank">0000-0003-1160-8727</a> 

## Hypothesis and workflow

Our hypothesis is based on the assumption that making use of semantic information obtained through the exploitation of knowledge graphs improves the prediction of machine learning and deep learning models in text classification.

<img src="https://jabenitez.com/kge/motivating-example-v2.png" width="800px" />

Starting from a set of textual data, it is possible to obtain the entities contained in them (thanks to FALCON 2.0 tool [[1]](https://doi.org/10.1145/3340531.3412777) the identifier of these entities in Wikidata and the corresponding embeddings using RDF2Vec).

<img src="https://jabenitez.com/kge/architecture.png" width="800px" />

In this research is presented the accession of semantic data enrichment obtained by knowledge graphs exploitation (KGE) to a set of texts on Eating Disorders (EDs) to obtain text classification models by applying machine learning and deep learning techniques. We make use of a proprietary dataset composed of 2,000 texts obtained from Twitter related to EDs. 

Subsequently, a manual labelling of the data into 4 different binary categories was performed: (i) texts written by people with ED, (ii) texts promoting having ED, (iii) texts of an informative nature and (iv) texts of a scientific nature . Using the FALCON 2.0 tool [[1]](https://doi.org/10.1145/3340531.3412777) , the entities of each of the 2,000 texts and the resources related to these concepts in the Wikidata knowledge graph are obtained. After this, Wikidata is consulted to obtain the embeddings using RDF2Vec [[2]](https://madoc.bib.uni-mannheim.de/41307/1/Ristoski_RDF2Vec.pdf) and they are combined using SIF-Embedding (Smooth Inverse Frequency) [[3]](https://openreview.net/pdf?id=SyK00v5xx), obtaining an embedding for each of the texts in the dataset. After these steps, different machine learning and deep learning models are trained only with the textual content and also adding the information provided by the 2,000 embeddings (Knowledge Graph Exploitation, KGE). 



## Results

<img src="https://jabenitez.com/kge/results-v2.png" width="800px" />

Results obtained in the 10 different models applied to the textual data and to the data with knowledge graph exploitation (KGE) in the 4 labelled categories.

This image shows all the results obtained after train ten different machine learning and deep learning models to categorize four different categories using two different datasets: 2,000 Tweets and the same data adding knowledge graph exploitation (KGE).

The highest percentage improvement in the  F<sub>1</sub> metric occurred in Category I in the RF model and in the $acc$ metric occurred in the same category and model.

The biggest difference in performance between the model trained with the texts and the model trained with the addition of knowledge graph mining in the F<sub>1</sub>  metric was in the RF model in category I with an improvement of 11.11% in the model with KGE and in the acc metric in the RF model in category III with an improvement of 15.01%. 

There are only two cases in which the F<sub>1</sub> metric applied to the KGE data is the same or worsens with respect to that obtained in the text data, in Category III in the CamemBERT and TweetBERT models.






