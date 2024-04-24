# Wooly Tongue - Demo of various LLM/ML efforts
<!-- TOC -->
* [Wooly Tongue - Demo of various LLM/ML efforts](#wooly-tongue---demo-of-various-llmml-efforts)
  * [Overview](#overview)
  * [Basics:](#basics-)
    * [Preprocess (get text/paras/sentences)](#preprocess-get-textparassentences)
    * [Embedding](#embedding)
    * [Quanitzation](#quanitzation-)
    * [Context Size](#context-size)
  * [Notes:](#notes)
  * [Implementations and Samples](#implementations-and-samples)
    * [Pytorch](#pytorch)
    * [Haystack](#haystack)
    * [Llamaindex](#llamaindex)
    * [Interesting (to me) links/pages:](#interesting-to-me-linkspages)
  * [WTH: wooly tongue??1?](#wth-wooly-tongue1)
<!-- TOC -->

## Overview

This is a demo repo with some basic machine learning actions and samples. These examples are aimed at local development and exploration. 

We assume most projects will benefit from hosted/scalable solutions for many of these components. 

[Pinecone](https://www.pinecone.io/) is our preferred solution for hosting vectors and performing search/analysis. They have a great mix of price/performance, and the documentation is helpful and robust. They have many benefits, but here are a few that stand out:
* https://docs.pinecone.io/guides/data/understanding-hybrid-search
* https://docs.pinecone.io/guides/data/filtering-with-metadata
* ECommerce hybrid [example](https://github.com/pinecone-io/examples/blob/master/learn/search/hybrid-search/ecommerce-search/ecommerce-search.ipynb)

This repo is python only, and focuses on three basic approaches:
* pytorch _(no advanced framework)_
* LlamaIndex _(was built on langchain, now mostly independant)_
* Haystack _(Deepset.ai & Andrew Ng framework, developer friendly)_

## Basics: 
### Preprocess (get text/paras/sentences)
* Use any number of tools to extract text from "office" type documents (docx, xlsx, ppt, pdf, html,...)
* Decide on use case:
  * chat
  * RAG
  * summarization
  * Q&A
  * semantic search
  * _others..._
* split text accordingly
  * word-level (word2vec, CBOW,...)
  * sentence-level (sbert,...)
  * paragraph/passage-level (presuming paragraphs contain multiple sentences with same 'though')
  * section level (e.g. for 10k analysis)
    * perhaps page level?? somewhat easier/quicker for pdf splitting??
  * document level 
    * less common? 
    * perhaps doc classification??
* Embedding
  * Choose an embedding model _(focusing on [sentence transformers](https://huggingface.co/sentence-transformers))_
    * Hosted/subscription
      * OpenAi
      * ...??...
    * Local/open-source _(~free)_
      * sources:
        * [HuggingFace via llamaindex](https://docs.llamaindex.ai/en/stable/examples/embeddings/huggingface/) (llamaindex) [Optimum ONNX Embeddings](https://docs.llamaindex.ai/en/stable/module_guides/models/embeddings/#huggingface-optimum-onnx-embeddings)
        * [HuggingFace Hub](https://huggingface.co/models?library=sentence-transformers)
        * [sbert pretrained](https://www.sbert.net/docs/pretrained_models.html) models
      * Popular models
        * BAAI/bge-small-en-v1.5
        * sentence-transformers/all-MiniLM-L6-v2
  * source/document embedding
    * 
  * query/user-input embedding  (**Note**: use the same model as source embedding)
    * 

### Embedding
_more to come..._


### Quanitzation 
**(fitting 20lbs of model in a 10lb bag...)**

* https://huggingface.co/TheBloke  _(well regarded "source" of many quantizations)_
* [GGUF vs GPTQ vs AWQ](https://www.maartengrootendorst.com/blog/quantization/)

### Context Size
This (afaiu) is the amount tokens a model can handle as input for a query/chat/...

Larger contexts allow 'stuffing' information along with an input to help a model 'understand' better.

Some users find that fine-tuning a model is 'better' but does take a bit more intellectual investment and time/effort.

## Notes:
* larger models with 4 or 5 bit quantization do 'better' than same filesize models without quantization 
  * i.e. 13b model with 4bit quantization is 'better' than 7b model unquant-ed _(full 16bit precision)_
* 8Gb vram is feasible for serving single models locally
* 12Gb vram can serve a couple of small (~4Gb) models for experimentation (and leave room for accelerating desktop/apps)
* Ollama (built on llamacpp??) is convenient for serving models locally
  * can 'pull' and/or 'run' models
  * can accept text file of questions _(for testing/benchmarking models systematically)_
  * caches models in memory (5min default) but also allows explicit control over time-to-live
  * should be able to make 'wise' choices of loading layers of a model into GPU/Vram, and use cpu ram for "overflow"
  * uses Modefile for more control (and quantization)
* llamacpp might be better for advanced model manipulation
* Fine-tuning may be 'better' than RAG (_source??_)
* Pay attention to guard-rail issues (hot topic, especially for public facing work)
  * 'uncensored' models may produce offensive or otherwise unsavory results _(caveat emptor!!1!)_


## Implementations and Samples
### Pytorch
[Pytorch examples folder in this repo](src/pytorch)

### Haystack
* [Haystack examples folder in this repo](src/haystack)
* Haystack sample code: [quickstart](https://haystack.deepset.ai/overview/quick-start)
* Farm-haystack seems outdated, use haystack-ai package, [install instructions here](https://docs.haystack.deepset.ai/docs/installation)
* [Pipeline templates](https://docs.haystack.deepset.ai/docs/pipelines#pipeline-templates) can provide quick & easy starting points


### Llamaindex
* [Llamaindex examples folder in this repo](src/llamaindex)
* Local models [(custom) setup](https://docs.llamaindex.ai/en/stable/getting_started/installation/) _(if you don't want to use default OpenAi resources)_

### Interesting (to me) links/pages:
* https://github.com/ollama/ollama/blob/main/README.md
* https://www.reddit.com/r/LocalLLaMA/comments/18yp9u4/llm_comparisontest_api_edition_gpt4_vs_gemini_vs/
* https://huggingface.co/TheBloke  (ycombinator [thread](https://news.ycombinator.com/item?id=37250926))
* https://ollama.com/blog/run-code-llama-locally
* https://medium.com/@fradin.antoine17/3-ways-to-set-up-llama-2-locally-on-cpu-part-2-ollama-c9d5d71612c9
* Open Orca [visualization](https://atlas.nomic.ai/map/c1b88b47-2d9b-47e0-9002-b80766792582/2560fd25-52fe-42f1-a58f-ff5eccc890d2)
* 

### Jupyter examples
The [jupyter folder](src/jupyter) in this repo contains some trial & error experiments. The notebooks starting with numbers have been successfully copied and run locally. They are messy, and probably best to ignore them. 

## WTH: wooly tongue??1?
this should be a repo of lessons learned from llama/llamaindex/ollama (i.e. the `wooly`), 
and a bit of general qualitative and linuistic (i.e. the `tongue`) insight and work.

_(Note: haystack is a big part of this, as well as huggingface, but I stopped at "wooly-tongue"...)_
