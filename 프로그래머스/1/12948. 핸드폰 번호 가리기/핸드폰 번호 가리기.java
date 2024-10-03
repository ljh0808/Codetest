class Solution {
    public String solution(String phone_number) {
        String answer = "";
        char[] ch = phone_number.toCharArray();
        for(int i=0;i<ch.length-4;i++){
            ch[i] = '*';
        }
        return String.valueOf(ch);
    }
    
}