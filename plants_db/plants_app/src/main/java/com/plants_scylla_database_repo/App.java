package com.plants_scylla_database_repo;
import com.datastax.Driver.core.Cluster;
import com.cassandra

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {

	    self.cluster = Cluster(contact_points["mms_scylla-node1_1", "mms_scylla-node1_2", "mms_scylla-node1_3"])
	    self.session = self.cluster.connect(keyspace='catalog')
	    self.session.default_consistency_level = ConsistencyLevel.QUORUM



	
    }
}
