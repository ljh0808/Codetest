class Solution {
    public int[] solution(int numer1, int denom1, int numer2, int denom2) {
        int topnum = numer1*denom2 + numer2 * denom1;
        int botnum = denom1 * denom2;
        int num = 1;
        
          
	        for(int i=1; i<=botnum; i++){
	            if(topnum%i==0&&botnum%i==0){
	              num = i;  
	            }
	        }
	        int[] result = {topnum/num,botnum/num}; 
	        return result;
	    
    }
}