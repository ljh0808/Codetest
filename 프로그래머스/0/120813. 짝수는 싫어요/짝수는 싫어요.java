class Solution {
    public int[] solution(int n) {
       	 int array[] = {};
		 if(n%2==0) {
			 array = new int[n/2];
		 } else {
			 array = new int[n/2+1];
		 }
		 
		 for(int i=0; i<array.length; i++) {
			 array[i] = (i*2)+1;
		 }
		 return array;
    }
}