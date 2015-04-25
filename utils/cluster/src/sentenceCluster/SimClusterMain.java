package sentenceCluster;

import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.Set;

//author: James Burgess


public class SimClusterMain {

	public static void main(String[] args) throws IOException {
		List<String> inputSents = Files.readAllLines(new File(args[0]).toPath(), Charset.defaultCharset() );
		//clean up the sents in preperation to cluster
		//it is assumed that the stoplist is in the same directory as the executable
		Set<String> stoplist = SimilarityClusterer.loadStoplist(args[1]);
		List<List<String>> clusterSents = new ArrayList<List<String>>();
		for(String s : inputSents) {
			clusterSents.add(SimilarityClusterer.sanitize(s,stoplist,false));
		}
		//discourage articles from self-grouping
		Collections.shuffle(clusterSents, new Random(0));
		
		//and cluster them
		
		SimilarityClusterer c = new SimilarityClusterer(clusterSents);
		int width = 9;
		double thresh = 0.01;
		if(args.length > 3) {
			width = Integer.parseInt(args[2]);
			thresh = Double.parseDouble(args[3]);
		}
		c.setThresh(thresh);
		c.setWidth(width);
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