class Solution {
    public boolean solution(String s) {
        boolean answer = true;
        char[]  result = new char[s.length()];
        if(s.length()!=6&&s.length()!=4) answer = false;
         for (int i = 0; i < s.length(); i++) {
            if (!Character.isDigit(s.charAt(i))) {
                answer = false;
            }
        }
        return answer;
    }
}