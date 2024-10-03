class Solution {
    boolean solution(String s) {
        boolean answer = false;
	  int pCount = 0;
	  int yCount = 0;
      for(int i=0;i<s.length();i++) {
       char result = s.toUpperCase().charAt(i);
       if(result=='P') pCount++;
       if(result=='Y') yCount++;
      }
      if(pCount==yCount) answer=true;
	  return answer;
    }
}