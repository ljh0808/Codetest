class Solution {
    public String solution(String s, int n) {
        StringBuilder sb = new StringBuilder();
        char[] ch = s.toCharArray();
        for(char a : ch){
            if(a==' '){
                sb.append(" ");
            } else if(a>='a'&&a<='z'){
                if(a+n>'z'){
                    sb.append((char)(a-26+n));
                } else{
                    sb.append((char)(a+n));
                }
            }
            else if(a>='A' && a<='Z'){
                if(a+n > 'Z'){
                    sb.append((char)(a-26+n));
                }else{
                    sb.append((char)(a+n));
                }
            }
        }
        
        return sb.toString();
    }
}