import logging
import json
import os
import time
import re
from nltk.corpus import wordnet
from api.utils.file_utils import get_project_base_directory


class Dealer:
    def __init__(self, redis=None):

        self.lookup_num = 100000000
        self.load_tm = time.time() - 1000000
        self.dictionary = None
        path = os.path.join(get_project_base_directory(), "rag/res", "synonym.json")
        try:
            self.dictionary = json.load(open(path, 'r'))
        except Exception:
            logging.warning("Missing synonym.json")
            self.dictionary = {}

        if not redis:
            logging.warning(
                "Realtime synonym is disabled, since no redis connection.")
        if not len(self.dictionary.keys()):
            logging.warning("Fail to load synonym")

        self.redis = redis
        self.load()

    def load(self):
        if not self.redis:
            return

        if self.lookup_num < 100:
            return
        tm = time.time()
        if tm - self.load_tm < 3600:
            return

        self.load_tm = time.time()
        self.lookup_num = 0
        d = self.redis.get("kevin_synonyms")
        if not d:
            return
        try:
            d = json.loads(d)
            self.dictionary = d
        except Exception as e:
            logging.error("Fail to load synonym!" + str(e))

    def lookup(self, tk, topn=8):
        if re.match(r"[a-z]+$", tk):
            res = list(set([re.sub("_", " ", syn.name().split(".")[0]) for syn in wordnet.synsets(tk)]) - set([tk]))
            return [t for t in res if t]

        self.lookup_num += 1
        self.load()
        res = self.dictionary.get(re.sub(r"[ \t]+", " ", tk.lower()), [])
        if isinstance(res, str):
            res = [res]
        return res[:topn]


if __name__ == '__main__':
    dl = Dealer()
    print(dl.dictionary)
