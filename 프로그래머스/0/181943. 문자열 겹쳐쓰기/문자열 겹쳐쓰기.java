class Solution {
    public String solution(String my_string, String overwrite_string, int s) {
        String answer = "";
        String result2 = my_string.substring(0,s)+overwrite_string;
        String result1 = my_string.substring(s+overwrite_string.length());
        answer = result2 + result1;
        return answer;
    }
}