from pipelines.ingestion.helpers.ingestor import Ingestor
from .cyphers import DiscourseCyphers

import json
import pandas as pd
import datetime
import re 

class DiscourseIngestor(Ingestor):
    def __init__(self):        
        self.cyphers = DiscourseCyphers()
        super().__init__(bucket_name="arbitrum-discourse")
    

    def process_posts(self):
        posts_df = pd.DataFrame(self.scraper_data['posts'])
        # ## create posts
        post_urls = self.save_df_as_csv(posts_df, f"ingestor_posts_{self.asOf}")
        self.cyphers.create_posts(post_urls)
        self.cyphers.connect_posts_replies()
        # create authors
        authors_df = posts_df[['author', 'authorId', 'postUuid']].iloc[1:]
        authors_df.drop_duplicates(inplace=True)
        authors_df['authorId'] = authors_df['authorId'].astype(int)
        authors_urls = self.save_df_as_csv(authors_df, f"data_authors_discourse_{self.asOf}")
        self.cyphers.create_authors(authors_urls)
        self.cyphers.connect_authors(authors_urls)
    

    def run(self):
        self.process_posts()

if __name__ == '__main__':
    ingestor = DiscourseIngestor()
    ingestor.run()
