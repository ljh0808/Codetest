class Solution {
    public String Odd(int num){
        String answer ="Odd";
        if(num%2==0 || num==0) answer="Even";
        return answer;
    }
    
    public String solution(int num) {
        Solution solution = new Solution();
        return solution.Odd(num);
    }
}