<img src="https://github.com/datasciencecampus/awesome-campus/blob/master/ons_logo.png">

# NBS LLM Classifier

# Introduction
## About
This is an implementation of the [ClassifAI](https://github.com/datasciencecampus/classifai) Python package that supports the semi-automatic classification of free text fields in the [NBS](https://nigerianstat.gov.ng/) Labour Force Survey to [ISCO](https://ilostat.ilo.org/methods/concepts-and-definitions/classification-occupation/) and [ISIC](https://ilostat.ilo.org/methods/concepts-and-definitions/classification-economic-activities/) coding schemes.

## Installation
Install the ClassifAI package directly from GitHub into your Python environment:

```bash
pip install "git+https://github.com/datasciencecampus/classifAI"
pip install "classifAI[huggingface]"
```

### Pre-commit actions
This repository contains a configuration of pre-commit hooks. These are language agnostic and focussed on repository security (such as detection of passwords and API keys). If approaching this project as a developer, you are encouraged to install and enable `pre-commits` by running the following in your shell:
   1. Install `pre-commit`:

      ```
      pip install pre-commit
      ```
   2. Enable `pre-commit`:

      ```
      pre-commit install
      ```
Once pre-commits are activated, whenever you commit to this repository a series of checks will be executed. The pre-commits include checking for security keys, large files and unresolved merge conflict headers. The use of active pre-commits are highly encouraged and the given hooks can be expanded with Python or R specific hooks that can automate the code style and linting. For example, the `flake8` and `black` hooks are useful for maintaining consistent Python code formatting.

**NOTE:** Pre-commit hooks execute Python, so it expects a working Python build.

## Usage
*Explain how to use the things in the repo.*

### Workflow

```mermaid
flowchart TB
    A[Labelled examples] --> B[Embedding model]
    A1[Query data] --> B
    B --> C[Vector data]
    C --> |Stored in| D[(VectorStore)]
    B --> C1[Vector data]
    C1 --> |Searched against| D
    D -.-> E[Cosine similarity scores ranked]
```

# License

<!-- Unless stated otherwise, the codebase is released under [the MIT Licence][mit]. -->

The code, unless otherwise stated, is released under [the MIT Licence][mit].

The documentation for this work is subject to [© Crown copyright][copyright] and is available under the terms of the [Open Government 3.0][ogl] licence.

[mit]: LICENCE
[copyright]: http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/uk-government-licensing-framework/crown-copyright/
[ogl]: http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
