import java.util.Arrays;

class Solution {
    public String solution(String str) {
       char[] result = str.toCharArray();
			Arrays.sort(result);
			System.out.println(new String(result));
			
			for(int i=0;i<str.length()/2;i++) {
				char temp = result[i];
				result[i] = result[str.length()-i-1];
				result[str.length()-i-1] = temp;
			}
        return new String(result);
    }
}