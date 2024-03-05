# Overview
`SnapshotScraper` retrieves governance proposals and their corresponding votes from the Arbitrum DAO Snapshot space.
It runs GraphQL queries against the Snapshot API, parses and refines the returned proposals/votes, and stores the results in `/data`


# Data

The script returns **Proposals** and **Votes** as keys in `data.json`.

## Proposals: 

```
{
  "proposals": [
    {
      "id": "string",
      "title": "string",
      "body": "string",
      "choices": ["string"],
      "start": "timestamp",
      "end": "timestamp",
      "state": "string",
      "author": "string"
    }
  ]
}
```


## Votes
```
{
  "votes": [
    {
      "proposalId": "string",
      "voter": "string",
      "choice": "number",
      "id": "dict"
    }
  ]
}
```