__author__ = 'ashishgagneja'

import pymongo as mgo


def _optional_arg(arg, sep=':'):
    """ If optional argument is present expand with separator

    :param arg: string or string-castable
        user argument
    :param sep: string
        argument separator
    :return: string
    """
    return sep + arg if arg else '',



def connect(server_name, username, port=None, password=None, pem_file=None, database=''):
    """ connect to mongodb instance

    :param server_name: string
        database server name or ip address
    :param username: string
        database username
    :param port (optional): int
        database port
    :param password (optional): string
        database password
    :param pem_file (optional): string
        path to file with private key
    :param database (optional): string
        database name

    :return: pymongo.mongo_client.MongoClient
    """

    return mgo.MongoClient('mongodb://%s%s@%s%s/%s' % (username, _optional_arg(password), server_name,
                        _optional_arg(port), database), ssl=True, ssl_keyfile=pem_file)



