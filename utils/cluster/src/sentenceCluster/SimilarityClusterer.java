package sentenceCluster;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

//author: James Burgess


public class SimilarityClusterer {
	List<List<String>> sents;//data to cluster
	Map<String,Double> idf;//inverse document frequency
	double thresh;//similarity threshhold
	int width;//centroid width
	public void setWidth(int w) {width = w;}
	public void setThresh(double d) {thresh = d;}
	
	public SimilarityClusterer(List<List<String>> sents) {
		this.sents = sents;
		width = 5;//arbitrary default
		thresh = 0.2;//arbitrary default
		idf = new HashMap<String,Double>();
		Set<String> wordlist = new HashSet<String>();
		for(List<String> sent : sents) {
			for(String s : sent) {
				if(idf.containsKey(s)) idf.put(s,idf.get(s) + 1);
				else {
					idf.put(s, (double) 1);
					wordlist.add(s);
				}
			}
		}
		double logUtterances = Math.log(sents.size());
		for(String s : wordlist) {
			idf.put(s, 1 + logUtterances - Math.log(idf.get(s)));
		}
	}
	
	
	void updateCluster(List<Integer> clstr, List<String> cntrd, Map<String,Integer> tf, List<String> sent) {
		//update tf
		for(String w : sent) {
			if(tf.containsKey(w)) tf.put(w, tf.get(w) + 1);
			else tf.put(w, 1);
		}
		//recalc centroid
		for(String w : sent) {
			if(cntrd.size() < width) cntrd.add(w);
			else {
				double candidate = tf.get(w) * idf.get(w);
				for(int i = 0; i < width; i++) {
					String old = cntrd.get(i);
					if(candidate > tf.get(old) * idf.get(old)) {
						cntrd.set(i, w);
						break;
					}
				}
			}
		}
	}
	
	//in theory there are other viable similarity functions (cosine similarity) but this one's simplest
	double overlapSimilarity(List<String> a, List<String> b) {
		int overlap = 0;
		for(String s : b) if(a.contains(s)) overlap++;
		return ((double) overlap)/(a.size() + b.size());
	}
	
	public List<List<Integer>> cluster() {
		List<List<Integer>> clusters = new ArrayList<List<Integer>>();
		List<List<String>> centroids = new ArrayList<List<String>>();
		List<Map<String,Integer>> clusterTF = new ArrayList<Map<String,Integer>>();
		clusters.add(new ArrayList<Integer>());
		centroids.add(new ArrayList<String>());
		clusterTF.add(new HashMap<String,Integer>());
		clusters.get(0).add(0);
		updateCluster(clusters.get(0),centroids.get(0),clusterTF.get(0),sents.get(0));
		for(int i = 1; i < sents.size(); i++) {
			List<String> sent = sents.get(i);
			int simCluster = 0;
			double clusterSim = overlapSimilarity(sent,centroids.get(0));
			for(int j = 1; j < clusters.size(); j++) {
				double newSim = overlapSimilarity(sent,centroids.get(j));
				if(newSim > clusterSim) {
					simCluster = j;
					clusterSim = newSim;
				}
			}
			if(clusterSim < thresh) {
				simCluster = clusters.size();
				clusters.add(new ArrayList<Integer>());
				centroids.add(new ArrayList<String>());
				clusterTF.add(new HashMap<String,Integer>());
			}
			updateCluster(clusters.get(simCluster),centroids.get(simCluster),clusterTF.get(simCluster),sent);
		}
		return clusters;
	}
}
