import java.util.*;

public class Solution {
    public int solution(int n) {
        int answer = 0;
	        String str = String.valueOf(n);
	        String[] result=str.split("");
	        for(int i=0;i<result.length;i++) {
	        	answer += Integer.parseInt(result[i]);
	        }

	        return answer;
    }
}