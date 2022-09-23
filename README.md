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

### Problem Statement and Objectives
This paper addresses the problem of effectively classifying short posts referring to EDs. Our main research objective is to generate vector-embedding representations that encode contextual knowledge reported in structured data structures from knowledge graphs and unstructured corpora (e.g., scientific publications or social media posts). Concretely, we aim at encoding richer contextual knowledge as depicted in Figure 1c. As a result, our goal is to generate vector-embeddings obtained from structured and unstructured data. The result is called contextual-based embeddings (CBEs). We hypothesize that CBEs will empower machine learning models in a way that the accuracy of pattern detection from social media posts is enhanced.

<img src="https://jabenitez.com/kge/intro-1.png" width="800px" />

### Proposed Solution

We propose a hybrid framework that combines vector embeddings generated from methods that extract contextual knowledge from various types of data sources (Figure 1c). As a proof of concept, we show the benefits of the proposed approach while combining word embeddings from pre-trained BERT models and  knowledge graph embedding methods learned from Wikidata. Although our approach is domain-agnostic, we will illustrate its performance in the problem of classifying Tweets according to mentions of eating disorders

<img src="https://jabenitez.com/kge/approach-architecture.png" width="800px" />

### Proposed Approach
#### Component 1: Context-Based Embeddings Encoding. 

This component has three main objectives: (i) to obtain contextual knowledge through unstructured data (sentence embeddings), (ii) to obtain contextual knowledge through structured data (knowledge graph embeddings), and (iii) to combine this textual knowledge into a single vector structure through the combination of both (context-based embeddings). Objectives (i) and (ii) are obtained through modules that are executed in parallel. Objective (iii) is executed once the two previous modules have been executed. The properties of the three modules that compose this component are detailed below.

<b>Unstructured based data.</b> This module generates a vector-embedding for each word within a post. This vector represents the similarity of the terms within the corpus of posts. For example, the term ``anorexia'' within the sentence \emph{``higher-calorie diets patients anorexia nervosa shorten hospital stays via''} is contextually related to the terms around it. A word-embedding encodes the similarity values of the terms within the corpus of posts. 
Once all the word-embeddings of a sentence are computed, a vector-embedding is generated; it represents the complete sentence, combining all the vectors of a sentence. This vector-embedding contains contextual knowledge of the posts. Thus, the closeness between terms is encoded, e.g., ``anorexia'' and ``diets''. These vectors can be obtained using, e.g., Tokenisers, Word2Vec or BERT. Although this combined vector represents the words of a sentence, it does not include knowledge modeled in structured data.

<b>Knowledge Graph-based data.</b> The main objective of this module is to obtain knowledge graph embeddings for each post; these vectors will enrich the ones generated from the unstructured data. Three steps are performed:

<i>(I) Entity recognition and linking over a Knowledge Graph</i>. The first step consists of recognizing the entities contained in the short texts used as input and linking the recognized entities to a knowledge graph; these engines are known as named entity recognizers and linkers (e.g., Falcon 2.0 and EntityLinker in the spaCy Python literature). In the current version of this module, the recognized entities are linked to  Wikidata. The Falcon 2.0 API extracts the entities of a sentence, as well as the resources that correspond to these entities in Wikidata and DBpedia. The following example illustrates the tasks of entity recognition and linking over the following sentence:

<i>higher-calorie diets patients anorexia nervosa shorten hospital stays via</i>

The recognized entities are:
[`kilocalorie',`diet',`patient',`anorexia',`nervosa']

And the identifiers of these entities in Wikidata are:

[`Q26708069', `Q474191', `Q181600', `Q254327', `Q131749']


<i>(II) Curation based on human in the loop for linking disambiguation</i>. Entity recognizers and linkers may be inaccurate. For example, the word ``Help'' can represent the action of help or support to someone, or it could be a music album called ``Help''.  
The framework resorts to a list of tabu types to decide whenever the linked resource needs to be manually validated and curated. This list includes the following types Album, Book, Streets, Organization, Song, and Movie.
 This checking enhances the quality of the description of a post in terms of entities in a knowledge graph.

<i>(III) KGE - Embeddings Extraction and Combination</i>. Knowledge graphs contain contextual knowledge of entities about concepts. In this step, knowledge graph embeddings are obtained for each entity of each post present. For example, the concept ``anorexia'' is represented in Wikidata as resource Q254327, which is a ``symtom'' and ``physical condition'' with ``decreased appetite''. The symbolic representation of anorexia in Wikidata is encoded in a subsymbolic representation or knowledge graph embedding. RDF2Vec or SDM-RDF2Vec can generate these vectors.
After obtaining each knowledge graph embedding for a post's entities, a combination of these vectors, which have the same size, is generated. As a result, a knowledge graph embedding for each post is generated. 

<b>Combining Context-Based Embeddings.</b> Once the contextual knowledge has been obtained from the unstructured based data and knowledge graphs data modules, this third module is in charge of combining both vectors. Combining these two vectors allows the complete contextual knowledge of each concept to be represented by a single vector. For example, in the initial sentence, we used ``highercalorie diets patients anorexia nervosa shorten hospital stays via'' we would have a single vector called context-based embedding. This vector would contain the information of the post obtained from its context as unstructured data, but it would also contain knowledge of the neighborhood of the words that compose it. The vector would represent the similarity between each post in the corpus from two different contextual knowledge. This combined vector contains the complete contextual information of each post.

<b>Component 2: Context-Based Embeddings Decoding.</b>

This component aims at using the information contained in the context-based embeddings generated by the first component by decoding them. According to the hypothesis put forward in this study, the complete contextual knowledge contained in these vectors should provide predictive models with a higher degree of accuracy. This knowledge allows the vectors to contain a more accurate inter-post similarity function than vectors generated from unstructured data alone or from unstructured data. In the running example, ``anorexia'' was close to ``nervosa'' in the vector obtained from the unstructured data, but not close to ``symtom''. The combination of both types of embeddings encodes different contextual knowledge; it offers a contextual-based enhanced vector.

<b>Predictive models.</b> In this module, different machine learning models are trained. The result is accurate models that provide more accurate label predictions on a corpus of text than traditional models. This decoding methodology can be applied not only to text classification problems, but also to other supervised and unsupervised learning problems.


## Validation and Results

<img src="https://jabenitez.com/kge/results-v3.png" width="800px" />

Results obtained in the 12 different models applied to the textual data and to the data with knowledge graph exploitation (KGE) in the 4 labelled categories.

This image shows all the results obtained after train ten different machine learning and deep learning models to categorize four different categories using two different datasets: 2,000 Tweets and the same data adding knowledge graph exploitation (KGE).

The highest percentage improvement in the  F<sub>1</sub> metric occurred in Category I in the RF model and in the $acc$ metric occurred in the same category and model.

The biggest difference in performance between the model trained with the texts and the model trained with the addition of knowledge graph mining in the F<sub>1</sub>  metric was in the RF model in category I with an improvement of 11.11% in the model with KGE and in the acc metric in the RF model in category III with an improvement of 15.01%. 

There are only two cases in which the F<sub>1</sub> metric applied to the KGE data is the same or worsens with respect to that obtained in the text data, in Category III in the CamemBERT and TweetBERT models.






