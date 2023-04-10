from api.query_parser import WarlockQuery
from api.main import app

if __name__ == '__main__':
    query = WarlockQuery('math 257, year:2021, semester:fall, is:online, is:open')
    print(query)