from ..helpers import Scraper
import logging 
import time
import json
import os 
import requests as requests


class TallyScraper(Scraper):
    def __init__(self, bucket_name="arbitrum-tally", load_data=False):
        super().__init__(bucket_name=bucket_name, load_data=load_data)
        self.base_url = "https://tally.xyz/gov/arbitrum"
        self.base_api_endpoint = "https://api.tally.xyz/query"
        self.headers = {
            'Content-Type': 'application/json',
            'Api-Key': os.getenv('TALLY_API_KEY')
        }


    def send_api_request(self, query, variables=None, retry_count=0):
        max_retries = 0  # Adjusted max_retries to allow for retries
        while retry_count <= max_retries:
            try:
                payload = {"query": query, "variables": variables}  # Include variables in the payload
                response = requests.post(self.base_api_endpoint, json=payload, headers=self.headers)
                response.raise_for_status()  # Raises exception for 4XX or 5XX errors
                data = response.json()
                if "errors" in data:
                    error_message = json.dumps(data['errors'], indent=4)  # Formatting the error for better readability
                    raise Exception(f"API response error: {error_message}")
                return data["data"]
            except requests.RequestException as e:
                logging.error(f"Request error: {e}, Response: {e.response.text}")
                time.sleep(2 ** retry_count)  # Implementing exponential backoff
                retry_count += 1
                if retry_count > max_retries:
                    logging.error("Max retries exceeded. Giving up.")
                    return None
            except Exception as e:
                logging.error(f"Unhandled exception: {e}")
                return None

    def governor(self):
        query = """
        query Proposals($chainId: ChainID!, $governorIds: Address!) {
          proposals(chainId: $chainId, governors: [$governorIds]) {
            id
            title
            description
            eta
            governor {
              name
              id
            }
            votes {
                voter {
                    address 
                    ens 
                    twitter 
                    name 
                    bio    
                }
                id
                support
                weight
            }
          }
        }
        """
        variables = {"chainId": "eip155:42161", "governorIds": "0xf07DeD9dC292157749B6Fd268E37DF6EA38395B9"}
        results = self.send_api_request(query, variables=variables)

        with open("results.json", 'w') as f:
            json.dump(results, f, indent=4)

    def run(self):
        self.governor()
        # self.save_data()
        # self.save_metadata()


if __name__ == "__main__":
    S = TallyScraper()
    S.run()