class Solution {
    public String solution(String s) {
        StringBuilder answer = new StringBuilder();
        String[] result = s.split("");
        int index = 0;
		for(int i=0;i<result.length;i++) {
			if(result[i].equals(" ")) {
				index = 0;
			} else if(index%2==0){
                result[i]= result[i].toUpperCase(); 
                index++;}
              else if(index%2!=0){
                result[i]= result[i].toLowerCase();
                index++;}
                answer.append(result[i]);
		}
        return answer.toString();
    }
}