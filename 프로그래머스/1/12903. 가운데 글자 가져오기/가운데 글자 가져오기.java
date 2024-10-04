class Solution {
    public String solution(String s) {
        int len = s.length();
        int mid = len / 2;
        
        if (len % 2 == 0) {
            return s.substring(mid - 1, mid + 1);
        }
        
        return String.valueOf(s.charAt(mid));
    }
}