package sentenceCluster;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.HashSet;
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
		Set<String> stoplist = loadStoplist("data/stoplist");
		List<List<String>> clusterSents = new ArrayList<List<String>>();
		for(String s : inputSents) clusterSents.add(sanitize(s,stoplist));

		//and cluster them
		SimilarityClusterer c = new SimilarityClusterer(clusterSents);
		c.setThresh(0.2);
		c.setWidth(5);
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

	//it is assumed that the stoplist is a newline delimited list of single words
	private static Set<String> loadStoplist(String filename) {
		try {
			return new HashSet<String>(Files.readAllLines(FileSystems.getDefault().getPath(filename),StandardCharsets.UTF_8));			
		}
		catch(Exception e) {
			return null;
		}
	}
	//some of this is extraneous if the passed in strings to program are already somewhat clean
	private static List<String> sanitize(String sent,Set<String> stoplist){
		sent = sent.toLowerCase();//drop caps
		sent = sent.replaceAll("(.|!|?)", "");//drop end of sentence (and acronyms)
		sent = sent.replaceAll("(-|:)"," ");//swap out non whitespace word seperators
		sent = sent.replaceAll("\\s+", " ").trim();//drop excess whitespace
		List<String> output = new ArrayList<String>();
		for(String s : sent.split(" "))//naive segment 
		{
			if(stoplist.contains(s)) continue;
			Stemmer stemmer = new Stemmer();
			stemmer.add(s.toCharArray(),s.length());
			output.add(stemmer.toString());
		}
		return output;
	}
}
