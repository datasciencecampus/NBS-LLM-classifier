# Demo

We will demonstrate how to use the [NBS LLM classifier](https://github.com/datasciencecampus/NBS-LLM-classifier) pipeline by classifying free-text survey responses in the Nigeria Labour Force Survey to [ISCO](https://ilostat.ilo.org/methods/concepts-and-definitions/classification-occupation/) occupational groups and [ISIC](https://ilostat.ilo.org/methods/concepts-and-definitions/classification-economic-activities/) economic activities.

## Data
The following datasets will be used in this example:

|Name |Source |URL |Type |
|:-----|:-----|:-----|:-----|
| International Standard Classification of Occupations (ISCO) | International Labour Organization | [Link](https://www.ilo.org/ilostat-files/Documents/ISCO.xlsx) | .xlsx (81KB) |
| International Standard Classification of Economic Activities (ISIC) | International Labour Organization | [Link](http://www.ilo.org/ilostat-files/Documents/ISIC.xlsx) | .xlsx (108KB) |
| Nigeria Labour Force Survey Q1 2024 | Nigeria National Bureau of Statistics | [Link](https://microdata.nigerianstat.gov.ng/index.php/catalog/151) | .sav (294MB) |
| Nigeria Labour Force Survey Q2 2024 | Nigeria National Bureau of Statistics | [Link](https://microdata.nigerianstat.gov.ng/index.php/catalog/152) | .sav (296MB) |

The quarterly data from the Nigeria Labour Force Survey are a subset of those published on the [Microdata Catalog](https://microdata.nigerianstat.gov.ng/index.php/home). Only the columns `['interview_id,'id7_hhnumber','hhroster_id,'mjj1','mjj2a','mjj2b','mjj2cclean','sjj1a','sjj1b','sjj1cclean']` which refer to ISCO main and secondary jobs were retained. The data were restructured and stored in `.csv` files.

## Workflow

1. *Build knowledgebases*: Two separate knowledgebases are created. One contains the ISCO statistical coding scheme with labelled examples from the Q1 2024 Nigeria Labour Force Survey. The other knowledgebase is based on the ISIC coding scheme. The 4-digit code is stored as `id` and the text descriptions are concatenated under `text`. Duplicate entries from amongst the labelled examples are removed. Each knowledgebase is saved as a `.csv` file in the `data/knowledgebase` subfolder.
2. *Create vector store*: Each knowledgebase is vectorised using the chosen embedding model and stored as a vector store. Essentially, this converts the knowledgebase entries into vectors of numbers.
3. *Build query files*: The Q2 2024 Nigeria Labour Force Survey data is pre-processed to three columns: [`id`,`query`,`prevalidated`]. The `id` column is a joining variable, `query` contains the free text, and `prevalidated` is the enumerator's 4-digit ISIC or ISCO code. **NB** The joining variable concatenates ['interview_id,'hhnumber','hhroster_id,'jobnumber'].
4. *Search vector store*: The input query (Q2 2024 NLFS) is vectorised and searched against the knowledgebase entries (ISCO/ISIC + Q1 2024 NLFS) in the vector store.
5. *Evaluation*: The accuracy of matching between the pre-validated and predicted 4-digit codes is calculated. This serves as the threshold for semi-automation.

## Setup

### Open a workspace in VS Code
1. Open up Visual Studio Code (VS Code) and select `File > Open Folder...` from the menu.
2. Either create a **New folder** or select an existing one with **Select folder**.
3. VS Code will now recognise your project folder as the workspace and list its subfolders and files in the **Explorer** pane.

### Clone NBS LLM classifier
Execute the following code into the Terminal console:

```bash
git clone https://github.com/datasciencecampus/NBS-LLM-classifier.git
```

This will install a copy of the NBS LLM classifier GitHub repo onto your local machine. Now select `File > Close Folder` from the menu and open the new folder in VS Code.

### Create a virtual environment
Open the Terminal in VS Code and create a *virtual environment*. A virtual environment allows you to manage the installation and updating of Python packages that are needed for your project without interfering with packages used by the system or by other projects.

```bash
python -m venv venv
venv\Scripts\activate.bat
```

If you are using a Mac you will need to run:

```bash
python -m venv venv
source venv/bin/activate
```

A folder called `venv` will be created that includes subfolders containing Python and installed packages.

### Install dependencies
Next we need to install the classifAI package and other dependencies.

```bash
pip install -r requirements.txt
```

### Check datasets path
The `config.json` file contains all of the file paths to the datasets needed in the demonstration.

```
├── demo/
|   └── input
│       ├── ISCO.xlsx
│       ├── ISIC.xlsx
|       └── NLFS_2024Q1.csv
|       └── NLFS_2024Q2.csv     
```

It is good practice to check that the file paths in the `config.json` file are correct before running the code.

## Choose vectoriser
The classifAI packages allows you to download vectorisers from GCP, Ollama and Hugging Face. We will pick a vectoriser from Hugging Face called [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). This model is lightweight and can be downloaded locally. To download this model we need to add its full name including the framework (i.e. sentence-transformers) to the `model_name` parameter in the `config.json` file.

## Run `main.py`
The next step is to run the main Python script in the Terminal. Just enter and execute the following:

```bash
python src/main.py all
```

If you want to run a particular stage of the pipeline you can choose amonsgst: `knowledgebase`, `vectorstore`, `query`, `search`, and `evaluate`.

The Python script will pre-process the knowledgebase and input query, vectorise, and generate semantic similarity scores between them.

## Evaluation
When complete the accuracy of the model will be printed in the console.

$$Accuracy = \frac{Number of correct predictions}{Total number of predictions}$$

Accuracy is the percentage of correctly classified cases or specifically the percentage of predicted ISCO/ISIC codes that match the pre-validated ones. Those cases that match can be automatically classified. The remaining cases can be manually classified using the 3 predicted ISCO/ISIC codes.

An additional plot comparing accuracy against coverage is also drawn.

## Search results
The search results generated by the pipeline will be saved in the `/outputs` folder with the name of the coding scheme appended to the filename e.g. `search_results_isic.csv`. 

## Optional: Add manually coded cases to the knowledgebase
The cases where `[isco/isic]_match_top_1` == FALSE can be manually coded using the 4-digit ISCO/ISIC candidate codes predicted by the tool. When completed these labelled examples can be added to the original knowledgebase. To do this you must update the `config.json` with the path to the manually coded cases and run:

```bash
python src/main.py knowledgebase
```
