package sentenceCluster;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

//author: James Burgess

public class SimClusterMain {

	//this program reads in sentences from stdin until EOF then clusters all the sentences and outputs the clusters to stdout ending with an EOF
	//It is assumed that all lines will have at least 1 word not on the stoplist within them
	//clusters are output in a 2d list. Each line is a comma seperated list of integers specifying an index of a sentence belonging to that cluster (indexed from 0).
	public static void main(String[] args) {
		List<String> inputSents = new ArrayList<String>();
		BufferedReader r = new BufferedReader(new InputStreamReader(System.in));
		try {
			String line = r.readLine();
			while(line != null) {
				inputSents.add(line);
			}
			r.close();
		}
		catch(IOException e) {
			//just stop reading and assume we have as many sentences as we're going to get.
		}
		
		//clean up the sents in preperation to cluster
		//it is assumed that the stoplist is in the same directory as the executable
		Set<String> stoplist = SimilarityClusterer.loadStoplist("data/stoplist");
		List<List<String>> clusterSents = new ArrayList<List<String>>();
		for(String s : inputSents) clusterSents.add(SimilarityClusterer.sanitize(s,stoplist));

		//and cluster them
		SimilarityClusterer c = new SimilarityClusterer(clusterSents);
		//this is as coarse as it can really go. note that some sentences are in clusters of size 1 (but not many)
		c.setThresh(0.01);
		c.setWidth(10);
		List<List<Integer>> clusters = c.cluster();
		for(List<Integer> i : clusters) {
			for(int j = 0; j < i.size(); j++) {
				System.out.print(i.get(j));
				if(j+1 < i.size()) {
				System.out.print(',');
				} else {
					System.out.print('\n');
				}
			}
		}
	}
}
