import java.util.Arrays;

class Solution {
    public long solution(long n) {
        long answer = 0;
        String[] result = (n+"").split("");
		Arrays.sort(result);
		for(int i=0;i<result.length;i++) {
			answer = answer*10+Long.parseLong(result[result.length-1-i]);
		}
		return answer;
    }
}