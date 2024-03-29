# Arbitrum Data Ingestion Framework

## Tl;dr 

This repo contains scripts for scraping on and off-chain data relevant for understanding the Arbitrum ecosystem.

<img width="932" alt="Screenshot 2024-03-03 at 12 37 55 PM" src="https://github.com/jchanolm/arbitrum-data/assets/160365885/c90054de-498b-4094-aaa3-7cdd4333d8c2">


Some examples: grant awardees and Github profiles, DAO proposals and voters, forum posts and posters...

The code is organized into two three modules:
- `scraping`: scripts to scrape data
- `ingestion` scripts to ingest data into a Neo4J, a graph database
- `post-processing` scripts to enrich data in Neo4J with additional attributes

## Judges
- Ignore Snapshot Ingestor + Tally Scraper, they were submitted after deadline.


## Design strategy
---- 
The repository structure allows you to call commands using a Python module approach. 
For example, run `python3 -m pipelines.scraping.discourse.scrape` 
to scrape posts and post authors from Arbitrum DAO's Discourse forum.

## Data

Scrapers store data in S3 by default (filesizes get quite large when you run multiple times a day for testing.)
I will add the option to store data locally/on IPFS shortly.
Links to the full datafiles are included in each scraper's `README.md`.
- Snapshot/Voting: ipfs://bafybeihu23kfmowefwj2ztolc42ajyx7gqd7i5wfvwnypvqhmel5hwrorm/
- Discourse/Forum: https://arb-grants-data-arbitrum-discourse.s3.us-east-2.amazonaws.com/data_2024-3-7_.json

Scrapers store data in S3 by default.
I will add the option to store data locally/on IPFS shortly.
Links to the full datafiles are included in each scraper's `README.md`.

Ingestors connect data from different scrapers with a common ontology which enables queries across different data sources.
For instance, you can query for wallets who voted on proposals (Snapshot) that funded Grants focused on data (Discourse, Gitcoin).

## Install
---- 
Create a virtual environment using **Python 3.10. 
After that, install requirements w/ `pip3 install -r requirements.txt`


## Docker Image
-----
Package the module into a Docker image for cloud deployment or local use. 
To build the image, run 
`docker build . -t arbitrum-pipelines`
 
Then, execute the modules directly through the Docker image 
by replacing "module", "service", and "action" with the desired pipeline module. 

I.e.  `docker run --env-file .env arbitrum-pipelines python3 -m pipelines.[module].[service].[action]`

Remember to have a `.env file` containing all the necessary environment variables. 
For your convenience, the repo also contains a `Docker Compose` file. 









