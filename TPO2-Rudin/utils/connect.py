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
    return sep + str(arg) if arg else ''



def connect(server_name, username=None, password=None, port=None, database=''):
    """ connect to mongodb instance

    :param server_name: string
        database server name or ip address
    :param username (optional): string
        database username
    :param password (optional): string
        database password
    :param port (optional): int
        database port
    :param database (optional): string
        database name

    :return: pymongo.mongo_client.MongoClient
    """

    # username and passowrd must be provided or both must be missing
    if None in [username, password] and (username is not None
                                         or password is not None):
        raise Exception('username & password must be specified together')

    uri = "mongodb://%s%s%s%s%s/%s" % (_optional_arg(username, ''),
                                       _optional_arg(password),
                                       '@' if username else '',
                                      server_name,
                                       _optional_arg(port),
                                       database)
    return mgo.MongoClient(uri)


