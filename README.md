# Combining-Knowledge-Graphs-and-Deep-Learning-for-categorizing-Tweets
Combining Knowledge Graphs and Deep Learning for categorizing Tweets

### Authors

* José Alberto Benítez Andrades - jbena@unileon.es - <a href="https://orcid.org/0000-0002-4450-349X" rel="nofollow" target="_blank">0000-0002-4450-349X</a>
* Ahmad Sakor - Ahmad.Sakor@tib.eu - <a href="https://orcid.org/0000-0001-8007-7021" rel="nofollow" target="_blank">0000-0001-8007-7021</a>
* Luis Daniel Fernandes Rotger - luis@bakkenbaeck.no - 
* Mayra Russo Botero - mrusso@l3s.de - <a href="https://orcid.org/0000-0001-7080-6331" rel="nofollow" target="_blank">0000-0001-7080-6331</a>
* Maria-Esther Vidal - maria.vidal@tib.eu - <a href="https://orcid.org/0000-0003-1160-8727" rel="nofollow" target="_blank">0000-0003-1160-8727</a> 


### 1. Problem statement

We address the problem of adding, detecting and using semantic content by making use of existing knowledge in public knowledge graphs in order to generate text classification models that make use of text semantics.

There are some studies that make use of semantic content contained in ontologies within some domains to improve some automatic classification methods.

However, there is a lack of studies that make a recognition of the entities and then a linking with these entities in knowledge graphs such as Wikidata to end up obtaining the embeddings of these entities as semantic content of these texts.

### 2. Our Proposed Solution

In this research is presented the accession of semantic data enrichment obtained by knowledge graphs exploitation (KGE) to a set of texts on EDs to obtain text classification models by applying machine learning and deep learning techniques. We make use of a proprietary dataset composed of 2,000 texts obtained from Twitter related to EDs. 

Subsequently, a manual labelling of the data into 4 different binary categories was performed: (i) texts written by people with ED, (ii) texts promoting having ED, (iii) texts of an informative nature and (iv) texts of a scientific nature . Using the FALCON 2.0 tool [[1]](https://doi.org/10.1145/3340531.3412777) , the entities of each of the 2,000 texts and the resources related to these concepts in the Wikidata knowledge graph are obtained. After this, Wikidata is consulted to obtain the embeddings using RDF2Vec [[2]](https://madoc.bib.uni-mannheim.de/41307/1/Ristoski_RDF2Vec.pdf) and they are combined using SIF-Embedding (Smooth Inverse Frequency) [[3]](https://openreview.net/pdf?id=SyK00v5xx), obtaining an embedding for each of the texts in the dataset. After these steps, different machine learning and deep learning models are trained only with the textual content and also adding the information provided by the 2,000 embeddings. 

### 3. Our hypothesis

![Motivating example](https://jabenitez.com/kge/motivating-example.png)

### 4. Workflow

![Workflow](https://jabenitez.com/kge/workflow.png)

Workflow of the experiments carried out in the research: (i) collection of Tweets, (ii) tagging of a subset of 2,000 tweets, (iii) obtaining entities from the Wikidata knowledge graph (1,358 unique entities), (iv) obtaining embeddings through RDF2Vec making use of Wikidata’s public SPARQL endpoint, (v) combining the entity embeddings into a single embedding for each Tweet and (vi) training and validation of predictive models using the textual dataset and the dataset with semantic information leveraging knowledge graph exploitation (KGE).

### 5. Results

<img src="https://jabenitez.com/kge/results.png" width="600px" />

Results obtained in the 10 different models applied to the textual data and to the data with knowledge graph exploitation (KGE) in the 4 labelled categories.

This image shows all the results obtained after train ten different machine learning and deep learning models to categorize four different categories using two different datasets: 2,000 Tweets and the same data adding knowledge graph exploitation (KGE).

The highest percentage improvement in the  F<sub>1</sub> metric occurred in Category I in the RF model and in the $acc$ metric occurred in the same category and model.

The biggest difference in performance between the model trained with the texts and the model trained with the addition of knowledge graph mining in the F<sub>1</sub>  metric was in the RF model in category I with an improvement of 11.11% in the model with KGE and in the acc metric in the RF model in category III with an improvement of 15.01%. 

There are only two cases in which the F<sub>1</sub> metric applied to the KGE data is the same or worsens with respect to that obtained in the text data, in Category III in the CamemBERT and TweetBERT models.

