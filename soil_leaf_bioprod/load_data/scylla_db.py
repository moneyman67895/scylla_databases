from cassandra.cluster import Cluster
import os
import sys
import csv
from cassandra import ConsistencyLevel

def datestr(year, month, day):
    return year + "-" + month + "-" + day

class scylla_db_manager:

    def __init__(self,nodes,keyspace= ''):
        print(nodes,keyspace)
        self.nodes = nodes

        self.cluster = Cluster(contact_points=nodes)
        self.session = self.cluster.connect(keyspace=keyspace)
        self.keyspace = keyspace
        self.session.default_consistency_level = ConsistencyLevel.QUORUM

    def showTables(self):
        query = "SELECT table_name FROM system_auth.tables where keyspace_name = {0}".format(self.keyspace)
        res = self.session.execute(query=query)
        for r in res:
            print(",".join([r_i +"\t" for r_i in r]))

    def createTable(self, table_name,CMAP, columns, column_types, keys):

        for (c,t) in CMAP["ADD"].items():
            create_columns.append(c + " " + t)
        if CMAP["DATE_TS"] is not None:
            create_columns.append("DATE_TS timestamp")
        for c in columns:
            if c[1] not in CMAP["DROP"]:
                create_columns.append(c[1] + " " + c[2])

            
        create_columns = [str(c[1]) + " " + str(c[2]) for ( c,v) in zip(columns,column_types)]
        create_keys = ",".join(keys)
        create = "CREATE TABLE {0} ({1}, primary key ({2}))".format(table_name,create_columns,create_keys)
        print(create)
        result = self.session.execute(query=create)


    def insertInto(self, table_name, columns, values):
        insert = "INSERT INTO {0} ({1}) VALUES ({2})".format(table, ",".join(columns), ",".join(["?" for c in columns]))

        insert_ps = self.session.prepare(query=insert)
        self.session.cluster.execute(query=insert_ps,parameters=values)

    def updateTable(self, table_name, columns, where, values):
        update = "UPDATE {0} set {1} WHERE {2}".join(table_name, ",".join([c + "=?" for c in columns]), where)
        update_ps = self.session.prepare(query=update_ps)
        self.session.cluster.execute(query=update_ps)

    def deleteFrom(self, table, where):
        delete = "DELETE FROM {0} WHERE {1}".format(table, where)
        delete_ps = self.session.prepare(query=delete)
        self.session.cluster.execute(query=delete_ps)
