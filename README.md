# Arbitrum Data Ingestion Framework

## Tl;dr 

This repo contains scripts for scraping on and off-chain data relevant for understanding the Arbitrum ecosystem.

Some examples: grant awardees and Github profiles, DAO proposals and voters, forum posts and posters...

The code is organized into two three modules:
- `scraping`: scripts to scrape data
- `ingestion` scripts to ingest data into a Neo4J, a graph database
- `post-processing` scripts to enrich data in Neo4J with additional attributes

<img width="932" alt="Screenshot 2024-03-03 at 12 37 55 PM" src="https://github.com/jchanolm/arbitrum-data/assets/160365885/c90054de-498b-4094-aaa3-7cdd4333d8c2">


## Design strategy
---- 
The repository structure allows you to call commands using a Python module approach. 
For example, run `python3 -m pipelines.scraping.discourse.scrape` 
to scrape posts and post authors from Arbitrum DAO's Discourse forum.

## Install
---- 
Create a virtual environment using **Python 3.10. 
After that, install requirements w/ `pip3 install -r requirements.txt`


## Docker Image
-----
Package the module into a Docker image for cloud deployment or local use. 
To build the image, run docker build . -t arbitrum-pipelines. 
Then, execute the modules directly through the Docker image 
by replacing "module", "service", and "action" with the desired pipeline module. 

I.e.  `docker run --env-file .env arbitrum-pipeline python3 -m pipelines.[module].[service].[action]`

Remember to have a `.env file` containing all the necessary environment variables. 
For your convenience, the repo also contains a `Docker Compose` file. 



# Modules

## Scraping
-----
The scraping module can be imported or run as a package using python -m.
It includes internal packages, each dedicated to a specific service 
and containing a scrape.py file to execute the scraping process for that service. 

Each service is initiated by running its `scrape.py` file.

```
scraping_module/
│
├── __init__.py
├── discourse/
│   ├── __init__.py
│   └── scrape.py
├── snapshot/
│   ├── __init__.py
│   └── scrape.py
└── ...
```

## Planned scrapers
---- 
- `discourse` [x]
- `snapshot` *in progress*
- `github` []
- `multisigs` []
- `gitcoin-grants-donors` []
- `dune-contributors` []
...
## Design strategy
------ 
- Each scraper inherits from `Scraper` class defined in `helpers/scraper.py`
- Each scraper must live in its own folder
- Each service must have a README.me file that defines the scraper's usage arguments
- Each service must explain how the scraper works and what data the scraper collects in its README.md file
- Each service must have an `__init__.py` file exporting the scraper and all other defined classes for use in the module
- Each scraper  a `scrape.py` file as its main executable
- Each scraper must save its data in its  `data/` subdirectory as a `.json`
- Each service must read and save its necessary metadata, such as last item scraped, in `data/scraper_metadata.json`







## TODO 

<!-- ## ENV Variables
----
Refer to the `dotenv.txt` file for required ENV variables.
 -->






### Step 2 - Snapshot Data Pipeline

Next I built a pipeline that scrapes all Snapshot voters and proprosals. 

`notebooks/snapshot`

I also linked Grantees to the Snapshot proprosals which approved their funding, which enables queries like
`give me every wallet that voted to approve funding for multiple (passing) STIP grant proprosals`

## Step 3 - Discourse pipeline

I built a pipeline to scrape all posts from the Arbitrum Foundation Discourse.

View code and data in `notebooks/arb-governance-data/discourse/`


## Todos 

**1. Publish dashboard to make the graph more accessible**

**2. Build pipelines to programatically expand and enrich the graph**
- Ingest all Arbitrum Foundation forum/Discourse posts
- Ingest all Tally proprosals/votes
- Ingest all contributors to grantee Githubs
- Ingest all Arbitrum delegation data
- Ingest Gitcoin grants funded by wallets that have voted on grant-related Arbitrum Snapshot proprosals
- Extract entities/links/etc from documents to identify grantee affiliates

3. Build dashboard with NeoDash (https://github.com/neo4j-labs/neodash) to make graph more accessible

4. Identify additional Arbitrum ecosystem grants and grantees
   - Gitcoin grantees who received Arbitrum matching fund
   - Grantees who received grants from other ecosystems
